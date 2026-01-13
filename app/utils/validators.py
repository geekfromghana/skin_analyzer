
import os
from typing import Tuple
from ..config import settings

ALLOWED_EXTS = set(settings.ALLOWED_EXTS)
ALLOWED_CT = set(settings.ALLOWED_CONTENT_TYPES)


def get_ext(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()


def validate_file_type(filename: str, content_type: str) -> Tuple[bool, str]:
    ext = get_ext(filename)
    if ext not in ALLOWED_EXTS:
        return False, f"Unsupported file extension '{ext}'. Allowed: {', '.join(ALLOWED_EXTS)}"
    if content_type not in ALLOWED_CT:
        return False, f"Unsupported content type '{content_type}'. Allowed: {', '.join(ALLOWED_CT)}"
    return True, ""
