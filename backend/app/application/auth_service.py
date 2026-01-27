from app.config.security import hash_password
from app.domain.schemas import UserCreate
from app.domain.models import Client
from sqlalchemy.orm import Session
from app.domain import models
import json
import bcrypt
import boto3

def hash_password(password: str) -> str:
    # Securely hash the password using bcrypt

    # Convert the string password to bytes
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password (bcrypt handles the 72-byte limit automatically now)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Convert back to string before returning
    return hashed.decode('utf-8')

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

def authenticate_user(email, password, db):
    # 1. Find user by email
    user = db.query(models.Client).filter(models.Client.email == email).first()

    if not user:
        return None

    # 2. Compare the plain password with the hashed one in db
    # We must encode both to bytes for bcrypt to work
    if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return user

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