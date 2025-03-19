from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta, timezone

from sqlalchemy import null
from config.settings import settings
from sqlalchemy.orm import Session
from database import get_db  # Function to get a database session
from google.auth.transport.requests import Request
from models import User

def get_google_calendar_events(user: User, db: Session):

    if not user.google_token:
        return {"error": "User has no Google token"}
    
    creds = Credentials(token=user.google_token, 
                        refresh_token=user.refresh_token,
                        token_uri="https://oauth2.googleapis.com/token", 
                        client_id=settings.GOOGLE_CLIENT_ID, 
                        client_secret=settings.GOOGLE_CLIENT_SECRET, 
                        scopes=["https://www.googleapis.com/auth/calendar.readonly", 
                                "openid", 
                                "https://www.googleapis.com/auth/userinfo.email", 
                                "https://www.googleapis.com/auth/userinfo.profile"])
    print(f"User token: {creds.refresh_token}")

    if creds.expired and creds.refresh_token is None:
        try:
            creds.refresh(Request())
            user.google_token = creds.token
            user.refresh_token = creds.refresh_token
            db.add(user)
            db.commit()
        except Exception as e:
            print(f"An error occurred while refreshing the token: {e}")
            return {"error": "Failed to refresh token"}
    
    print(f"User token  updated: {creds.refresh_token}")



    try:
        # Refresh the token if expired
        """Fetch Google Calendar events using stored token."""
        # Convert stored token into credentials
        # Retrieve credentials from user (assumes refresh_token is stored)
        # creds = Credentials(
        #     token=user.google_token,  # Stored access token
        #     refresh_token=user.refresh_token,  # Stored refresh token
        #     token_uri="https://oauth2.googleapis.com/token",
        #     client_id=settings.GOOGLE_CLIENT_ID,
        #     client_secret=settings.GOOGLE_CLIENT_SECRET,
        #     scopes=["https://www.googleapis.com/auth/calendar.readonly", 
        #             "openid", 
        #             "https://www.googleapis.com/auth/userinfo.email",
        #             "https://www.googleapis.com/auth/userinfo.profile"],)

        # Refresh the token if expired
        
    
            # Build the Calendar API service
        service = build("calendar", "v3", credentials=creds)

        # Set the time range (next 7 days)
        now = datetime.now(timezone.utc).isoformat()  # Use built-in timezone.utc
        end_time = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

        # Call the Google Calendar API
        events_result = service.events().list(
            calendarId="primary", 
            timeMin=now, 
            timeMax=end_time,
            maxResults=30, 
            singleEvents=True, 
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        print("Upcoming events:", [event["summary"] for event in events])
        return events


    except HttpError as error:
        print(f"An error occurred: {error}")
        return {"error": str(error)}
        