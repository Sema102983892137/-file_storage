import hashlib
from werkzeug.datastructures import FileStorage


def file_hash(file: FileStorage) -> str:
    sha256 = hashlib.sha256()
    file.seek(0)
    while chunk := file.read(8192):
        sha256.update(chunk)
    file.seek(0)
    return sha256.hexdigest()
