
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from ..utils.auth import verify_api_key
from ..services.storage import path_for
from ..services.analysis import analyze_image

router = APIRouter(tags=["analyze"])


class AnalyzeRequest(BaseModel):
    image_id: str


class AnalyzeResponse(BaseModel):
    image_id: str
    skin_type: str
    issues: list[str]
    confidence: float
    metrics: dict


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest, _=Depends(verify_api_key)):
    path = path_for(req.image_id)
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unknown image_id")
    result = analyze_image(path)
    return {"image_id": req.image_id, **result}
