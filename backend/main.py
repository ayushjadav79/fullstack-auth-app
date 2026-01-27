from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.routes import router
from app.infrastructure_db.database import engine
from app.domain.models import Base

# This creates the tables in Postgres if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# # This makes the files in /static accessible at http://127.0.0.1:8000/static/...
# app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:5173",
    "http://13.200.253.108"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Backend is running and connected to S3"}