from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from fastapi.security import APIKeyHeader
from app.config.security import SECRET_KEY, ALGORITHM, create_access_token
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.domain.schemas import UserCreate
from app.infrastructure_db.file_storage import save_photo_to_s3, delete_photo_from_s3
from app.infrastructure_db.database import get_db
from app.application import auth_service
from app.config.hobbies import hobbies as get_hobbies_list
from app.domain import models
from typing import cast, Optional
from app.config.logger_config import logger

router = APIRouter()

# Tells Swagger/FastAPI where the login route is
oauth2_scheme = APIKeyHeader(name="Authorization")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Login to verify the token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Please login using valid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Add a log to see if the token is even arriving at your EC2 now
    logger.info(f"Incoming Header: {token}") 

    if not token:
        logger.error("No token received in headers")
        raise credentials_exception
    
    try:
        logger.info(f"Token validation attempt for token starting with: {token[:10]}...")
        actual_token = token.replace("Bearer ", "") if "Bearer " in token else token
        payload = jwt.decode(actual_token, str(SECRET_KEY), algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not isinstance(email, str):
            logger.warning("Token decoded but email 'sub' field is missing or invalid.")
            raise credentials_exception
        logger.info(f"User {email} successfully authenticated via token.")
        return email
    
    except JWTError as e:
        logger.error(f"JWT Validation Failed: {str(e)} | Token provided: {token}")
        raise credentials_exception

@router.post("/register")
def register_user(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    dob: str = Form(...),
    gender: str = Form(...),
    hobbies: list[str] = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Delegate file saving to infrastructure
    photo_path = save_photo_to_s3(file)

    if not photo_path:
        raise HTTPException(status_code=500, detail="Failed to upload image to S3")

    # 2. Package everything into your new UserCreate class
    # This significantly improves readability as requested
    new_user_data = UserCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        dob=dob,
        gender=gender,
        hobbies=hobbies,
        photo_url=photo_path
    )

    # 3. Call the service with the single object
    return auth_service.register_new_user(user_data=new_user_data, db=db)

@router.post("/login")
def login_user(
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    logger.info(f"Login attempt received for email: {email}")
    user = auth_service.authenticate_user(email, password, db)
    
    # If the service returns None (wrong email or password)
    if not user:
        logger.warning(f"Failed login attempt: Invalid credentials for {email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT Token
    access_token = create_access_token(data={"sub": user.email})
    logger.info(f"Login successful for {email}. Token generated.")

    # If successful return the user info
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "email": user.email
        }
    }

@router.get("/hobbies")
def get_hobbies():
    # Returns the list of hobbies from hobbies.py to frontend
    return get_hobbies_list()

@router.get("/users")
def get_users(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Endpoint for the React frontend to fetch the list of users.
    return auth_service.get_all_users(db)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # 1. Find the user
    user = db.query(models.Client).filter(models.Client.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    
    # 2. Store the photo URL before the user is deleted
    photo_url_to_delete = cast(Optional[str], user.photo_url)

    # 3. Delete from Database
    db.delete(user)
    db.commit()

    # 4. Delete photo from S3 bucket
    if photo_url_to_delete:
        delete_photo_from_s3(photo_url_to_delete)
        
    return {"message": "User deleted successfully"}

@router.put("/users/{user_id}")
def update_user(
    user_id: int, 
    updated_data: dict, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)):

    # Find the existing user in db
    db_user = db.query(models.Client).filter(models.Client.id == user_id).first()
    
    if not db_user:
        return {"error": "User not found"}
    
    # Update the fields with data sent from React
    db_user.first_name = updated_data.get("first_name", db_user.first_name)
    db_user.last_name = updated_data.get("last_name", db_user.last_name)
    db_user.email = updated_data.get("email", db_user.email)
    db_user.dob = updated_data.get("dob", db_user.dob)
    db_user.gender = updated_data.get("gender", db_user.gender)
    db_user.hobbies = updated_data.get("hobbies", db_user.hobbies)

    # Save the changes
    db.commit()
    db.refresh(db_user)
    return db_user