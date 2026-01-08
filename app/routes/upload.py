
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from ..utils.auth import verify_api_key
from ..services.storage import save_upload

router = APIRouter(tags=["upload"])


@router.post("/upload")
async def upload_image(file: UploadFile = File(...), _=Depends(verify_api_key)):
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")
    image_id = save_upload(file)
    return {"image_id": image_id}
