from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from services.google_auth import get_google_auth_url, exchange_code_for_token
from services.get_current_user import get_current_user
from models import User
import logging
import jwt
from services.access_token import create_access_token
from services.google_calender_get_events import get_google_calendar_events


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
                    google_token=credentials.token,
                    refresh_token=credentials.refresh_token)
        db.add(user)
        db.commit()
    else:
        user.google_token = credentials.token
        user.refresh_token = credentials.refresh_token
        db.add(user)
        db.commit()

    user_data = {"email": user.email, "name": user.name, "google_token":user.google_token, "refresh_token": user.refresh_token}
    access_token = create_access_token(data=user_data)

    return {"status": "success", "user": user_data , "access_token": access_token, "token_type": "bearer"}

@router.get("/protected-route")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user.name}!"}

@router.post("/logout")
async def logout():
    return {"message": "Logged out. Remove token on frontend."}

@router.get("/calendar/events") # need to pass token through frontend
def fetch_calendar_events(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    events = get_google_calendar_events(user, db)
    if "error" in events:
        raise HTTPException(status_code=403, detail=events["error"])
    return {"events": events}

    # if not user.google_token:
    #     raise HTTPException(status_code=403, detail="User is not authenticated with Google")

    # # Fetch events using the stored token
    # events = get_google_calendar_events(user, db)

    # return {"events": events}