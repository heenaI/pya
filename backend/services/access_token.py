from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError
import jwt
from fastapi import HTTPException, status
from config.settings import settings
import time



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate a JWT token with expiration time."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.fromtimestamp(time.time()) + expires_delta 
    else:
        print(f"Token Expiry Days: {settings.ACCESS_TOKEN_EXPIRE_DAYS}")
        expire_days = int(settings.ACCESS_TOKEN_EXPIRE_DAYS)
        expire =  datetime.fromtimestamp(time.time()) + timedelta(days=expire_days)
    
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
