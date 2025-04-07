from datetime import date
from typing import List
from sqlalchemy.orm import Session


from models import  User
from fastapi import Depends, HTTPException
from sqlalchemy.orm.exc import NoResultFound

def validate(data):
    # Ensure either user_id or arskurs_id is provided, but not both
    if not data.get('user_id') and not data.get('arskurs_id'):
        raise HTTPException(status_code=422, detail="Either user_id or arskurs_id must be provided.")
    if data.get('user_id') and data.get('arskurs_id'):
        raise HTTPException(status_code=422, detail="Only one of user_id or arskurs_id can be provided.")
    return data
def get_all_users(database: Session):
    return database.query(User).all() 
def add_user(database: Session, user_params: User):
    user = User(**user_params.dict())  # Convert Pydantic model to SQLAlchemy model
    database.add(user)
    database.commit()
    database.refresh(user)
    return user
