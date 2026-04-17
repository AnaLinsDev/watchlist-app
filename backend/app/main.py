import os
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.core.error_handlers import (validation_exception_handler, app_error_handler, global_exception_handler)
from app.core.errors import AppError
from app.routes import auth
import app.models

load_dotenv()

CLIENT_URL = os.getenv("CLIENT_URL")

app = FastAPI()

app.include_router(auth.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register handlers
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
