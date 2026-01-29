from app.config.security import hash_password, verify_password
from app.domain.schemas import UserCreate
from app.domain.models import Client
from sqlalchemy.orm import Session
from app.domain import models
import json
import boto3

def send_welcome_email(recipient_email: str):
    client = boto3.client('ses', region_name='ap-south-1') # Mumbai
    client.send_email(
        Source='ayushjadav314@gmail.com',
        Destination={'ToAddresses': [recipient_email]},
        Message={
            'Subject': {'Data': 'Welcome to Ayush\'s App!'},
            'Body': {'Text': {'Data': 'You have successfully registered.'}}
        }
    )

def register_new_user(user_data: UserCreate, db: Session):
    # 1. Hash the password
    hashed_pw = hash_password(user_data.password)

    # 2. Create the Database Model
    db_user = Client(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password_hash=hashed_pw,
        dob=user_data.dob,
        gender=user_data.gender,
        hobbies=user_data.hobbies,
        photo_url=user_data.photo_url
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 3. Send Welcome Email
    send_welcome_email(user_data.email)
    return db_user

def authenticate_user(email, password, db: Session):
    # 1. Find user by email
    user = db.query(models.Client).filter(models.Client.email == email).first()

    if not user:
        return None

    # 2. Verify password
    try:
        if verify_password(password, str(user.password_hash)):
            return user
    except Exception as e:
        print(f"Error during password verification: {e}")
        return None

    return None

def get_all_users(db: Session):
    # Business logic to fetch all users. This is what the /users route calls.
    return db.query(Client).all()

def process_hobbies(hobbies_raw: str):
    # Business logic to handle different hobby formats
    try:
        return json.loads(hobbies_raw)
    except json.JSONDecodeError:
        return [h.strip() for h in hobbies_raw.split(",")]
    
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.Client).filter(models.Client.id == user_id).first()