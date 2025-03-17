from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import date, datetime

class MembershipOut(BaseModel):
    id: int
    membership_type: str
    start_date: date
    end_date: date

    class Config:
        orm_mode: True
        from_attributes = True  # Allow the Pydantic model to read data from SQLAlchemy models

class UserBase(BaseModel):
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    phone_number: Optional[str]

class UserIn(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str

class Arskurs(BaseModel):
    name: str
    description: str
    skola: str
    klass: str

class ArskursOut(Arskurs):
    id: int
    name: str
    description: str
    skola: str
    klass: str

    class Config:
        orm_mode: True
        from_attributes = True  # Allows Pydantic to read data from SQLAlchemy models

class Role(BaseModel):
    name: str

class RoleOut(Role):
    id: int

    class Config:
        from_attributes = True  # Allows Pydantic to read data from SQLAlchemy models

class UserInUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    arskurs_id: Optional[int] = None
    role_id: Optional[int] = None
    membership_id: Optional[int] = None

class MembershipCreate(BaseModel):
    membership_type: str
    start_date: date
    end_date: date
    user_id: int  # Add user_id field

    class Config:
        orm_mode: True

class UserOut(UserBase):
    id: int
    arskurs: Optional[ArskursOut] = None
    role: Optional[RoleOut] = None
    membership: Optional[MembershipOut] = None

    class Config:
        orm_mode: True
        from_attributes = True

class MembershipUpdate(BaseModel):
    membership_type: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    class Config:
        orm_mode: True

class LoginRequest(BaseModel):
    email: str
    password: str

class GetUser(BaseModel):
    email: str
    password: str

class BetygOut(BaseModel):
    id: int
    grade: str
    comments: Optional[str]
    feedback: Optional[str]
    created_at: datetime
    updated_at: datetime
    homework_id: int
    class Config:
        from_attributes = True  # Allows Pydantic to read data from SQLAlchemy models

class BetygCreate(BaseModel):
    grade: str
    comments: Optional[str]
    feedback: Optional[str]
    homework_id: int

class BetygUpdate(BaseModel):
    grade: Optional[str]
    comments: Optional[str]
    feedback: Optional[str]

    class Config:
        from_attributes = True  # Allow the Pydantic model to read data from SQLAlchemy models

class FiluppladdningOut(BaseModel):
    id: int
    filename: str
    filepath: str
    description: str 
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode: True
        from_attributes = True 

class MeddelandeOut(BaseModel):
    id: int
    message: str
    description: Optional[str]
    read_status: str
    created_at: datetime
    updated_at: datetime
    homework_id: int
     
    class Config:
        orm_mode: True
        from_attributes = True  # Allow the Pydantic model to read data from SQLAlchemy models

class SubjectBase(BaseModel):
    name: str

class SubjectOut(SubjectBase):
    id: int

    class Config:
        orm_mode: True
        from_attributes = True  # Allow the Pydantic model to read data from SQLAlchemy models

class MeddelandeCreate(BaseModel):
    message: str
    description: Optional[str]
    read_status: Optional[str] = "Unread"
    homework_id: int

class RecommendedResourceBase(BaseModel):
    title: str
    url: str
    description: Optional[str] = None

class RecommendedResourceCreate(RecommendedResourceBase):
    title: str
    url:Optional[str]
    description:Optional[str]
    homework_id: int

class RecommendedResourceOut(RecommendedResourceBase):
    id: int
    subject_id: int
    title: str
    url: str
    description:str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode: True
        from_attributes = True

class HomeworkBase(BaseModel):
    title: str
    description: str
    due_date: date
    status: str = "Pending"
    priority: str = "Normal"

class HomeworkCreate(HomeworkBase):
    user_id: int  # Added user_id field
    subject_id: int  # Added subject_id field

class HomeworkOut(HomeworkBase):
    id: int
    user_id: int
    subject_id: int
    user: Optional[UserOut] = None
    subject: Optional[SubjectOut] = None
    betyg: Optional[BetygOut] = None
    meddelande: Optional[MeddelandeOut] = None
    filuppladdning: Optional[FiluppladdningOut] = None
    recommended_resources: Optional[RecommendedResourceOut] = None

    class Config:
        orm_mode: True
        from_attributes = True

class HomeworkInUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    user_id: Optional[int] = None
    subject_id: Optional[int] = None

    class Config:
        orm_mode: True

class FiluppladdningCreate(BaseModel):
    filename: str
    filepath: str
    description: Optional[str]
    homework_id: int

class ArskursBase(BaseModel):
    name: str
    description: str
    skola: str
    klass: str

class ArskursCreate(ArskursBase):
    pass

class Arskurs(ArskursBase):
    id: int

    class Config:
        orm_mode: True

class SubjectCreate(BaseModel):
    name: str

    class Config:
        orm_mode: True