import io
import random
import tarfile
import zipfile


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