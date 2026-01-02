"""
Authentication Module - API Key Authentication
"""
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Optional
import secrets

from config import settings


# API Key Header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def generate_api_key() -> str:
    """Generate a random API key"""
    return secrets.token_urlsafe(32)


async def verify_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """
    Verify API key from request header
    
    Args:
        api_key: API key from X-API-Key header
        
    Returns:
        str: Validated API key
        
    Raises:
        HTTPException: If API key is invalid or missing
    """
    # Nếu không bật xác thực API key, cho phép tất cả requests
    if not settings.ENABLE_API_KEY_AUTH:
        return "public"
    
    # Kiểm tra API key
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    # Kiểm tra API key có hợp lệ không
    if api_key not in settings.api_keys_list:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return api_key


# Optional dependency - không bắt buộc API key
async def optional_verify_api_key(
    api_key: Optional[str] = Security(api_key_header)
) -> Optional[str]:
    """
    Optional API key verification - không throw error nếu missing
    """
    if not settings.ENABLE_API_KEY_AUTH:
        return "public"
    
    if not api_key:
        return None
    
    if api_key in settings.api_keys_list:
        return api_key
    
    return None
