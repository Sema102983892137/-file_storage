import os
from config import STORAGE_DIR


def get_file_path(file_hash):
    if len(file_hash) < 2:
        return None
    subdir = file_hash[:2]
    return os.path.join(STORAGE_DIR, subdir, file_hash)
