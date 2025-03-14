from datetime import datetime, time, timedelta
from typing import Optional
from jose import JWTError
import jwt
from fastapi import HTTPException, status
from config.settings import settings



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate a JWT token with expiration time."""
    to_encode = data.copy()
    expire = datetime.fromtimestamp(time.time()) + (expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY_JWT, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY_JWT, algorithms=[settings.ALGORITHM])
        return payload  # Returns decoded user data if valid
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
