from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from services.google_auth import get_google_auth_url, exchange_code_for_token
from models import User
import logging
import jwt

router = APIRouter()

@router.get("/")
async def start():
    return {"message": "AI Task & Schedule Optimizer Backend Running"}


@router.get("/auth/login")
async def login():
    return RedirectResponse(get_google_auth_url())

@router.get("/auth/callback")
async def callback(request: Request, code: str, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    credentials = exchange_code_for_token(code)
    # print(f"Credentials: {credentials.id_token if credentials else None}") 
    if credentials is None or credentials.id_token is None:
        logging.error("Failed to exchange code for token")
        raise HTTPException(status_code=400, detail="Failed to exchange code for token")
    
    id_token = jwt.decode(credentials.id_token, options={"verify_signature": False})
    user_email = id_token["email"]
    # print(f"id_token: {id_token}, type: {type(id_token)}")
    # print(f"name: {id_token['name']}, email: {user_email}, {credentials.token}")
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        user = User(email=user_email, 
                    name=id_token["name"], 
                    password_hash=None,  # need to chnage this later based on logging in method
                    role="parent",  # Need to change this after front end completed 
                    google_token=credentials.token)
        db.add(user)
        db.commit()

    return {"status": "success", "message": "User logged in successfully"}