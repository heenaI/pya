from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DATABASE_URL_env = os.getenv("DATABASE_URL")

DATABASE_URL = DATABASE_URL_env

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")