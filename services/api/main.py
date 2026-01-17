# BUDGOAPPV2 main.py
# CREATED BY PICSOU
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Budgo API", version="0.1.0")

origins = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", "").split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from auth.router import router as auth_router
app.include_router(auth_router)

@app.get("/ping")
def ping():
    return {"status": "ok"}
