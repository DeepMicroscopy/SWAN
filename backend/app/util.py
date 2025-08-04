import random
import tarfile
import zipfile

import qrcode
import qrcode.image.svg
import qrcode.image.styles.moduledrawers.svg

def extract_file_names(file_path):
    result = []

    if zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, 'r') as zipf:
            result = zipf.namelist()
    elif tarfile.is_tarfile(file_path):
        with tarfile.open(file_path, 'r:*') as tarf:
            result = tarf.getnames()

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

def seed_from(user, session, study):
    if user.username == "anonymous":
        return f"{session.session_key}--{study}"
    else:
        return f"{user.id}--{study}"

def deterministic_shuffle(items: list[str], seed):
    result = items.copy()

    rng = random.Random(seed)
    rng.shuffle(result)

    return result

def create_qr(data):
    # ERROR_CORRECT_L: About 7% or less errors can be corrected.
    # ERROR_CORRECT_M: About 15% or less errors can be corrected.
    # ERROR_CORRECT_Q: About 25% or less errors can be corrected.
    # ERROR_CORRECT_H: About 30% or less errors can be corrected
    qr = qrcode.QRCode(
        version = None,
        error_correction = qrcode.ERROR_CORRECT_M,
        box_size = 32,
        border = 4,
        image_factory = qrcode.image.svg.SvgPathImage,
        mask_pattern = None,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(
        back_color='white',
        fill_color='black',
        # unavailable for svg
        #color_mask=None,
        module_drawer=qrcode.image.styles.moduledrawers.svg.SvgPathSquareDrawer(),
        # unavailable for svg
        #embeded_image_path=None,
    )

    return img.to_string(encoding="unicode")