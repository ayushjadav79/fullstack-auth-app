from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import Settings

settings = Settings()
if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file!")

# This creates the actual connection to Postgres
engine = create_engine(settings.DATABASE_URL)

# This is a 'Session Factory' - it creates a new connection for every request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()