import base64
import hashlib
import hmac
import random
import tarfile
import zipfile

import qrcode
import qrcode.image.styles.moduledrawers.svg
import qrcode.image.svg
from rest_framework.renderers import BaseRenderer

from swan import settings


def groups(request):
    return request.user.groups.values_list("id", flat=True)


class SVGRenderer(BaseRenderer):
    media_type = "image/svg+xml"
    format = "svg"
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        return data.encode(self.charset) if isinstance(data, str) else data


class FileRenderer(BaseRenderer):
    media_type = "application/octet-stream"
    format = "bin"
    charset = None  # binary data, no charset

    def render(self, data, media_type=None, renderer_context=None):
        return data


def extract_file_names(file_path):
    result = []

    if zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, 'r') as zipf:
            # Filter out directory entries
            result = [name for name in zipf.namelist() if not name.endswith('/')]
    elif tarfile.is_tarfile(file_path):
        with tarfile.open(file_path, 'r:*') as tarf:
            # Filter only regular files
            result = [m.name for m in tarf.getmembers() if m.isreg()]

    result.sort()

    return result


def extract_file_data(file_path, file_name):
    file_data = None

    if zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, 'r') as zipf:
            file_data = zipf.read(file_name)
    elif tarfile.is_tarfile(file_path):
        with tarfile.open(file_path, 'r:*') as tarf:
            file_data = tarf.extractfile(tarf.getmember(file_name)).read()

    return file_data


def seed_from(user, session: str, study: str):
    if session is None or session == "":
        raise Exception("session must be set to a non-empty string")

    if user.is_authenticated:
        return f"{user.id}--{study}"
    else:
        return f"{session}--{study}"


def deterministic_shuffle(items: list[str], seed):
    result = items.copy()

    rng = random.Random(seed)
    rng.shuffle(result)

    return result


def create_tag(study: str) -> str:
    code = hmac.new(settings.HMAC_KEY, study.encode("utf-8"), lambda: hashlib.blake2b(digest_size=settings.HMAC_SIZE))
    return base64.urlsafe_b64encode(code.digest()).decode("utf-8").rstrip("=")


def check_tag(study: str, code: str) -> bool:
    return create_tag(study) == code


def create_qr(data):
    # ERROR_CORRECT_L: About 7% or fewer errors can be corrected.
    # ERROR_CORRECT_M: About 15% or fewer errors can be corrected.
    # ERROR_CORRECT_Q: About 25% or fewer errors can be corrected.
    # ERROR_CORRECT_H: About 30% or fewer errors can be corrected
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.ERROR_CORRECT_M,
        box_size=32,
        border=4,
        image_factory=qrcode.image.svg.SvgPathImage,
        mask_pattern=None,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(
        back_color='white',
        fill_color='black',
        # unavailable for svg
        # color_mask=None,
        module_drawer=qrcode.image.styles.moduledrawers.svg.SvgPathSquareDrawer(),
        # unavailable for svg
        # embedded_image_path=None,
    )

    xml: str = img.to_string(encoding="unicode")

    if settings.DEBUG:
        xml = xml.replace(
            "</svg>",
            "<text x='10' y='10' font-size='4' fill='black'>" + data[data.index("#") - 1:] + "</text></svg>",
        )

    return xml
