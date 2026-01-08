
from fastapi import Header, HTTPException, status
from ..config import settings


async def verify_api_key(x_api_key: str | None = Header(None)):
    """
    Optional API key check. If API_KEY is set in .env, require matching x-api-key header.
    If API_KEY is not set, allow requests without auth.
    """
    if settings.API_KEY is None:
        return  # auth disabled
    if x_api_key is None or x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
