import os
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from config.settings import settings
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET_FILE = os.path.abspath(os.path.join(BASE_DIR, "..", "config", "client_sec.json"))
REDIRECT_URI = "http://localhost:8000/auth/callback"
# print(f"CLIENT_SECRET_FILE: {CLIENT_SECRET_FILE}")

try:
    with open(CLIENT_SECRET_FILE, "r") as file:
        client_secrets = json.load(file)
        print("✅ Successfully loaded JSON file:")
except Exception as e:
    print(f"❌ ERROR: Failed to load JSON file: {e}")

flow = Flow.from_client_secrets_file(
    CLIENT_SECRET_FILE,
    scopes=["https://www.googleapis.com/auth/calendar.readonly", 
            "openid", 
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_uri=REDIRECT_URI,
)

def get_google_auth_url():
    auth_url, _ = flow.authorization_url(prompt="consent", access_type='offline', include_granted_scopes='true')
    return auth_url

def exchange_code_for_token(code):
    try:
        flow.fetch_token(code=code)
        return flow.credentials

    except Exception as e:
        print(f"Error exchanging code for token: {e}")
        return None