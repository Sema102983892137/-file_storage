import os
from config import STORAGE_DIR
from typing import Optional


def get_file_path(file_hash: str) -> Optional[str]:
    if len(file_hash) < 2:
        return None
    subdir = file_hash[:2]
    return os.path.join(STORAGE_DIR, subdir, file_hash)
