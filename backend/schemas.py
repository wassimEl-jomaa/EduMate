from pydantic import BaseModel, field_validator, model_validator
from typing import List, Optional, Union
from datetime import date, datetime





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
class SchoolBase(BaseModel):
    id: int
    name: str  # Assuming `School` has a `name` field, adjust as necessary.

    class Config:
       from_attributes = True 
class SchoolCreate(BaseModel):
    name: str
    description: str
    address: str
    phone_number: str
    email: str
   
# Base schema for creating or updating an Arskurs
class ArskursBase(BaseModel):
    name: str
    description: str
    skola_id: Optional[int]  # skola_id is optional, can be None
    klass: str

# Schema for creating Arskurs (can use ArskursBase directly)
class ArskursCreate(BaseModel):
    name: str
    description: str
    skola_id: Optional[int]  # skola_id is optional, can be None
    klass: str

# Schema for reading Arskurs data, including the id field
class ArskursOut(ArskursBase):
    id: int  # Include the id for the output model
    class Config:
        from_attributes = True 
class Role(BaseModel):
    name: str

class RoleOut(Role):
    id: int

    class Config:
        from_attributes = True  # Allows Pydantic to read data from SQLAlchemy models
class RoleCreate(BaseModel):
    role_name: str
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

    class Config:
        from_attributes = True
class MembershipOut(BaseModel):
    id: int
    membership_type: str
    start_date: date
    end_date: date

    class Config:
       
        from_attributes = True  # Allow the Pydantic model to read data from SQLAlchemy models
class UserOut(UserBase):
    id: int
    arskurs: Optional[ArskursOut] = None
    role: Optional[RoleOut] = None
    membership: Optional[MembershipOut] = None

    class Config:
       
        from_attributes = True

class MembershipUpdate(BaseModel):
    membership_type: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    class Config:
        from_attributes = True

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
class BetygOutStudent(BaseModel):
    id: int
    grade: str
    comments: Optional[str]
    feedback: Optional[str]
    created_at: datetime
    updated_at: datetime
    homework_id: int
    homework_title: Optional[str]  # Add homework title
    subject: Optional[str]  # Add subject name

    class Config:
        from_attributes = True  # Allows Pydantic to read data from SQLAlchemy models        
class BetygCreate(BaseModel):
    grade: str
    comments: str
    feedback: str
    homework_id: int
    user_id: int

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
      
        from_attributes = True  # Allow the Pydantic model to read data from SQLAlchemy models
class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True 
class SubjectBase(BaseModel):
    name: str

class SubjectOut(SubjectBase):
    id: int
    name: Optional[str] = None

    class Config:
       
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

class RecommendedResourceOut(BaseModel):
    id: int
    title: str
    url: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    homework_id: int

    class Config:
       
        from_attributes = True
class TeacherOut(BaseModel):
    id: int
    user: UserOut  # Nested User schema
    subject:SubjectOut
    qualifications: Optional[str]
    photo: Optional[str]

    class Config:
        from_attributes = True 
class TeacherCreate(BaseModel):
    user_id: int
    subject_id: Optional[int] = None
    qualifications: Optional[str] = None        

class HomeworkBase(BaseModel):
    title: str
    description: str
    due_date: date
    status: str = "Pending"
    priority: str = "Normal"

class HomeworkCreate(BaseModel):
    title: str
    description: str
    due_date: str
    status: str
    priority: str
    subject_id: int
    teacher_id: Optional[int] = None
    user_id: Optional[int] = None
    arskurs_id: Optional[int] = None

    @model_validator(mode="after")
    def validate_user_or_arskurs(cls, values):
        # Access attributes directly instead of using .get()
        if not values.user_id and not values.arskurs_id:
            raise ValueError("Either user_id or arskurs_id must be provided.")
        if values.user_id and values.arskurs_id:
            raise ValueError("Only one of user_id or arskurs_id can be provided.")
        return values
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
        from_attributes = True  # Updated from orm_mode
      

class HomeworkInUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    user_id: Optional[int] = None
    subject_id: Optional[int] = None

    class Config:
       from_attributes = True

class FiluppladdningCreate(BaseModel):
    filename: str
    filepath: str
    description: Optional[str]
    homework_id: int
class SubjectCreate(BaseModel):
    name: str

    class Config:
       from_attributes = True