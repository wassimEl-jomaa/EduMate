from datetime import date
from typing import List
from sqlalchemy.orm import Session

from schemas import GradeCreate, GradeUpdate, FiluppladdningCreate, HomeworkCreate, MeddelandeCreate,  RecommendedResourceCreate, SubjectCreate
from models import Grade, File_Attachment, Message, Recommended_Resource, Subject, User, Role, Homework
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
# Add a new role to the database
def add_role(database: Session, role_name: str):
    role = Role(name=role_name)
    database.add(role)
    database.commit()
    database.refresh(role)
    return role

# Add a role to a user
def add_role_to_user(database: Session, user_id: int, role_id: int):
    user = database.query(User).filter(User.id == user_id).first()
    role = database.query(Role).filter(Role.id == role_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    user.roles.append(role)  # Append role to the user
    database.commit()
    database.refresh(user)
    return user

# Get all roles
def get_all_roles(database: Session):
    return database.query(Role).all()

# Get all users with a specific role
def get_users_by_role(database: Session, role_name: str):
    role = database.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role.users

def get_user_by_email_and_password(database: Session, email: str, password: str):
    try:
        user = database.query(User).filter(User.email == email, User.password == password).first()
        if user:
            return user
        return None  # Or raise an exception if you prefer
    except NoResultFound:
        return None
    
# Create a new homework entry
def create_homework(database: Session, homework_data: HomeworkCreate):
    try:
        # Validate the input data
        validate(homework_data.model_dump())  # Use model_dump instead of dict

        # Create the homework entry
        homework = Homework(**homework_data.model_dump())  # Use model_dump instead of dict
        database.add(homework)
        database.commit()
        database.refresh(homework)
        return homework
    except HTTPException as e:
        raise e
    except Exception as e:
        database.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while creating homework: {str(e)}")

# Get all homework assignments
def get_homeworks(database: Session):
    try:
        return database.query(Homework).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching homeworks: {str(e)}")

# Get homework by user id
def get_homework_by_user(database: Session, user_id: int):
    try:
        return database.query(Homework).filter(Homework.user_id == user_id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching homework for user {user_id}: {str(e)}")
def get_homework_by_subject(database: Session, subject_id: int):
    try:
        return database.query(Homework).filter(Homework.subject_id == subject_id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching homework for subject {subject_id}: {str(e)}")    
def create_recommended_resource(database: Session, resource_data: RecommendedResourceCreate):
    try:
        resource = Recommended_Resource(**resource_data.model_dump())
        database.add(resource)
        database.commit()
        database.refresh(resource)
        return resource
    except Exception as e:
        database.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while creating recommended resource: {str(e)}")

def get_recommended_resources(database: Session, subject_id: int):
    try:
        return database.query(Recommended_Resource).filter(Recommended_Resource.subject_id == subject_id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching recommended resources: {str(e)}")


def delete_user(database: Session, user_id: int):
    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    database.delete(user)
    database.commit()
    return {"message": "User deleted successfully"}




    
def get_all_betyg(database: Session):
    try:
        return database.query(Grade).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching betyg: {str(e)}")
def create_betyg(database: Session, betyg_data: GradeCreate):
    try:
        betyg = Grade(**betyg_data.model_dump())
        database.add(betyg)
        database.commit()
        database.refresh(betyg)
        return betyg
    except Exception as e:
        database.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while creating betyg: {str(e)}")
def update_betyg(database: Session, betyg_id: int, betyg_data: GradeUpdate):
    betyg = database.query(Grade).filter(Grade.id == betyg_id).first()
    if not betyg:
        raise HTTPException(status_code=404, detail="Betyg not found")
    
    for key, value in betyg_data.model_dump(exclude_unset=True).items():
        setattr(betyg, key, value)
    
    database.commit()
    database.refresh(betyg)
    return betyg  
def get_meddelanden_by_user(database: Session, user_id: int):
    try:
        return database.query(Message).join(Homework).filter(Homework.user_id == user_id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching meddelanden: {str(e)}")
def create_meddelande(database: Session, meddelande_data: MeddelandeCreate):
    try:
        meddelande = Message(**meddelande_data.model_dump())
        database.add(meddelande)
        database.commit()
        database.refresh(meddelande)
        return meddelande
    except Exception as e:
        database.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while creating meddelande: {str(e)}")    
def get_all_filuppladdningar(database: Session):
    try:
        return database.query(File_Attachment).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching filuppladdningar: {str(e)}") 
def create_filuppladdning(database: Session, filuppladdning_data: FiluppladdningCreate):
    try:
        filuppladdning = File_Attachment(**filuppladdning_data.model_dump())
        database.add(filuppladdning)
        database.commit()
        database.refresh(filuppladdning)
        return filuppladdning
    except Exception as e:
        database.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while creating filuppladdning: {str(e)}")    

def ArskursSchema(database: Session):
    try:
        return database.query(ArskursSchema).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching Arskurschema: {str(e)}")  
def create_subject(database: Session, subject: SubjectCreate):
    db_subject = Subject(name=subject.name)
    database.add(db_subject)
    database.commit()
    database.refresh(db_subject)
    return db_subject    


def add_role(database: Session, role_name: str):
    role = Role(name=role_name)
    database.add(role)
    database.commit()
    database.refresh(role)
    return role

def add_subject(database: Session, subject_data: SubjectCreate):
    try:
        subject = Subject(**subject_data.model_dump())
        database.add(subject)
        database.commit()
        database.refresh(subject)
        return subject
    except Exception as e:
        database.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while adding subject: {str(e)}")
