import base64
import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db_setup import get_db
from models import Token, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_SALT = "wassim"

def get_password_hash(password: str) -> str:
    """Hash a plain text password."""
    return pwd_context.hash(password)

# Generate a token with user information and salt, then encode it
def generate_token(user: User) -> str:
    """Generate a token containing user information with added salt and encode it."""
    # Generate a random component (this can be any random value or nonce)
    random_component = os.urandom(16).hex()  # 16 bytes of random data
    # Combine payload and timestamp
    message = f"{user.id}|{user.role.name}|{random_component}"

    # Hash the message using HMAC with SHA256 and the secret salt
    signature = hmac.new(SECRET_SALT.encode(), message.encode(), hashlib.sha256).hexdigest()

    # Combine the message with the signature and base64 encode it for transmission
    token = f"{message}|{signature}"
    token_encoded = base64.urlsafe_b64encode(token.encode()).decode()
    return token_encoded

def decode_token(encoded_token):
    """
    Decode the token and verify its authenticity using the salt.
    :param encoded_token: The base64-encoded token string
    :return: Decoded user information or an error message
    """
    # Decode the token from base64
    decoded_token = base64.urlsafe_b64decode(encoded_token.encode()).decode()

    # Split the token into message and signature
    message, signature = decoded_token.rsplit("|", 1)

    # Generate the expected signature by hashing the message with the secret salt
    expected_signature = hmac.new(SECRET_SALT.encode(), message.encode(), hashlib.sha256).hexdigest()

    # If the signature matches, decode the message (JSON)
    if hmac.compare_digest(signature, expected_signature):
        user_info = json.loads(message)

        return user_info  # Return user info and timestamp
    else:
        return "Invalid token", None

# Token expiry utility
def token_expiry(hours=1):
    """Set token expiration time."""
    return datetime.now(timezone.utc) + timedelta(hours=hours)

# Create a token and save it in the database
def create_database_token(user: User, db: Session, hours=1):
    """Create a token for a user and save it in the database."""
    db_token = db_token = db.query(Token).filter(user.id == Token.user_id).first()
    if not db_token or db_token.expires_at < datetime.now():
        if db_token:
            db.delete(db_token)
            db.commit() # Delete the existing token if it has expired
        token = generate_token(user)
        expires_at = token_expiry(hours)
        db_token = Token(token=token, user_id=user.id, expires_at=expires_at)
        
        db.add(db_token)
        db.commit()
    return {"token": db_token.token, "expires_at": db_token.expires_at}

# Validate a token from the database
def validate_database_token(token: str, db: Session):
    """Validate a token by checking the database."""
    db_token = db.query(Token).filter(Token.token == token).first()
    if not db_token or db_token.expires_at < datetime.now():
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return db_token.user

# Dependency to get the current user based on the token
def get_current_user(token: str, db: Session = Depends(get_db)):
    """Get the current user from the token."""
    return validate_database_token(token, db)