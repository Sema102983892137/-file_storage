import hashlib


def file_hash(file):
    sha256 = hashlib.sha256()
    file.seek(0)
    while chunk := file.read(8192):
        sha256.update(chunk)
    file.seek(0)
    return sha256.hexdigest()
