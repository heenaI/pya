from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt
from sqlalchemy.orm import Session
from database import get_db
from models import User
from config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # OAuth2 bearer token scheme

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")

    # print(f"Token received: {token}")  # Debugging - See if the token is being passed

    try:
        payload = jwt.decode(token, settings.SECRET_KEY_JWT, algorithms=[settings.ALGORITHM])
        user_email = payload.get("email")
        if user_email is None:
            raise HTTPException(status_code=401, detail="JWT Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="JWT Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="JWT Invalid token")

    user = db.query(User).filter(User.email == user_email).first()
    
    if not user:
        raise HTTPException(status_code=403, detail="JWT Invalid token")
    
    return user