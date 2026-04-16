from fastapi import FastAPI
from app.routes import auth
import app.models

app = FastAPI()

app.include_router(auth.router)
