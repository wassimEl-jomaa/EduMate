from datetime import date
from typing import List
from sqlalchemy.orm import Session

from schemas import BetygCreate, BetygUpdate, FiluppladdningCreate, HomeworkCreate, MeddelandeCreate, MembershipCreate, MembershipOut, MembershipUpdate, RecommendedResourceCreate, SubjectCreate
from models import Betyg, Filuppladdning, Meddelande, Membership, RecommendedResource, Subject, User, Role,Homework
from fastapi import Depends, HTTPException
from sqlalchemy.orm.exc import NoResultFound
from models import Membership, User

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
        homework = Homework(**homework_data.model_dump())
        database.add(homework)
        database.commit()
        database.refresh(homework)
        return homework
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
        resource = RecommendedResource(**resource_data.model_dump())
        database.add(resource)
        database.commit()
        database.refresh(resource)
        return resource
    except Exception as e:
        database.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while creating recommended resource: {str(e)}")

def get_recommended_resources(database: Session, subject_id: int):
    try:
        return database.query(RecommendedResource).filter(RecommendedResource.subject_id == subject_id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching recommended resources: {str(e)}")
def update_membership(database: Session, membership_id: int, membership_data: MembershipUpdate):
    membership = database.query(Membership).filter(Membership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    
    for key, value in membership_data.model_dump().items():
        setattr(membership, key, value)
    
    database.commit()
    database.refresh(membership)
    return membership

def delete_user(database: Session, user_id: int):
    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    database.delete(user)
    database.commit()
    return {"message": "User deleted successfully"}

def delete_membership(database: Session, membership_id: int):
    membership = database.query(Membership).filter(Membership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    
    database.delete(membership)
    database.commit()
    return {"message": "Membership deleted successfully"}

def get_all_memberships(database: Session):
    try:
        return database.query(Membership).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching memberships: {str(e)}")
    
def get_all_betyg(database: Session):
    try:
        return database.query(Betyg).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching betyg: {str(e)}")
def create_betyg(database: Session, betyg_data: BetygCreate):
    try:
        betyg = Betyg(**betyg_data.model_dump())
        database.add(betyg)
        database.commit()
        database.refresh(betyg)
        return betyg
    except Exception as e:
        database.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while creating betyg: {str(e)}")
def update_betyg(database: Session, betyg_id: int, betyg_data: BetygUpdate):
    betyg = database.query(Betyg).filter(Betyg.id == betyg_id).first()
    if not betyg:
        raise HTTPException(status_code=404, detail="Betyg not found")
    
    for key, value in betyg_data.model_dump(exclude_unset=True).items():
        setattr(betyg, key, value)
    
    database.commit()
    database.refresh(betyg)
    return betyg  
def get_meddelanden_by_user(database: Session, user_id: int):
    try:
        return database.query(Meddelande).join(Homework).filter(Homework.user_id == user_id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching meddelanden: {str(e)}")
def create_meddelande(database: Session, meddelande_data: MeddelandeCreate):
    try:
        meddelande = Meddelande(**meddelande_data.model_dump())
        database.add(meddelande)
        database.commit()
        database.refresh(meddelande)
        return meddelande
    except Exception as e:
        database.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while creating meddelande: {str(e)}")    
def get_all_filuppladdningar(database: Session):
    try:
        return database.query(Filuppladdning).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching filuppladdningar: {str(e)}") 
def create_filuppladdning(database: Session, filuppladdning_data: FiluppladdningCreate):
    try:
        filuppladdning = Filuppladdning(**filuppladdning_data.model_dump())
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

def create_membership(database: Session, membership_type:str):
        membership = Membership(name=membership_type)
        database.add(membership)
        database.commit()
        database.refresh(membership)
        return membership
    
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
