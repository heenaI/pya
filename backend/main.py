from routes.auth import router as auth_router
from fastapi import FastAPI

app = FastAPI()
# Include the auth routes
app.include_router(auth_router)




