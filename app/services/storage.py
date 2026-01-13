
import os
import uuid
from fastapi import UploadFile, HTTPException, status
from ..config import settings
from ..utils.validators import validate_file_type, get_ext

MAX_SIZE_BYTES = settings.MAX_FILE_MB * 1024 * 1024


def save_upload(file: UploadFile) -> str:
    ok, msg = validate_file_type(file.filename, file.content_type or "")
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

    data = file.file.read() or file.read()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file uploaded")
    if len(data) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail=f"File exceeds {settings.MAX_FILE_MB}MB limit")

    image_id = uuid.uuid4().hex
    ext = get_ext(file.filename)
    fpath = os.path.join(settings.STORAGE_DIR, f"{image_id}{ext}")

    with open(fpath, 'wb') as out:
        out.write(data)

    return image_id


def path_for(image_id: str) -> str | None:
    for ext in settings.ALLOWED_EXTS:
        candidate = os.path.join(settings.STORAGE_DIR, f"{image_id}{ext}")
        if os.path.exists(candidate):
            return candidate
    return None
