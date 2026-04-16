from fastapi import FastAPI
from routes import auth

from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

print("\n\n\n\n\n")
print("RAW:", DATABASE_URL)
print("\nREPR:", repr(DATABASE_URL))
print("\n\n\n\n\n")

app = FastAPI()

app.include_router(auth.router)
