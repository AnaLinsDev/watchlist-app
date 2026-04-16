from fastapi import FastAPI
import app.models

from app.core.error_handlers import (
    app_error_handler,
    global_exception_handler
)
from app.core.errors import AppError
from app.routes import auth
import app.models


app = FastAPI()

app.include_router(auth.router)

# register handlers
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, global_exception_handler)
