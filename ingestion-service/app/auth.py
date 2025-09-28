from fastapi import Depends, Header, HTTPException, status
from .config import settings

HEADER_NAME = "X-API-Key"

def require_api_key(x_api_key: str | None = Header(default=None, alias=HEADER_NAME)):
    if not settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server API key not configured."
        )
    if not x_api_key or x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
    return True

AuthDependency = Depends(require_api_key)
