import secrets
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db_setup import get_db
from models import Token, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash a plain text password."""
    return pwd_context.hash(password)

# Generate a random token
def generate_token():
    """Generate a random token."""
    return secrets.token_hex(32)  # Generates a 64-character random token

# Token expiry utility
def token_expiry(hours=1):
    """Set token expiration time."""
    return datetime.now(timezone.utc) + timedelta(hours=hours)

# Create a token and save it in the database
def create_database_token(user: User, db: Session, hours=1):
    """Create a token for a user and save it in the database."""
    token = generate_token()
    expires_at = token_expiry(hours)
    db_token = Token(token=token, user_id=user.id, expires_at=expires_at)
    db.add(db_token)
    db.commit()
    return {"token": token, "expires_at": expires_at}

# Validate a token from the database
def validate_database_token(token: str, db: Session):
    """Validate a token by checking the database."""
    db_token = db.query(Token).filter(Token.token == token).first()
    if not db_token or db_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return db_token.user

# Dependency to get the current user based on the token
def get_current_user(token: str, db: Session = Depends(get_db)):
    """Get the current user from the token."""
    return validate_database_token(token, db)