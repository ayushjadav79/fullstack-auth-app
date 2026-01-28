from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config.security import SECRET_KEY, ALGORITHM, create_access_token
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.domain.schemas import UserCreate
from app.infrastructure_db.file_storage import save_photo_to_s3
from app.infrastructure_db.database import get_db
from app.application import auth_service
import json
from app.config.hobbies import hobbies as get_hobbies_list
from app.domain import models

router = APIRouter()

# Tells Swagger/FastAPI where the login route is
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Login to verify the token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Please login using valid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not isinstance(email, str):
            raise credentials_exception
        return email
    except JWTError:
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
    user = auth_service.authenticate_user(email, password, db)
    
    # If the service returns None (wrong email or password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT Token
    access_token = create_access_token(data={"sub": user.email})

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
    user = db.query(models.Client).filter(models.Client.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    db.delete(user)
    db.commit()
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