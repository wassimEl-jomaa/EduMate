from pydantic import BaseModel, field_validator, model_validator
from typing import List, Optional, Union
from datetime import date, datetime


class GetUser(BaseModel):
    email: str
    password: str


class UserBase(BaseModel):
    id: Optional[int]  # To include the user ID if needed in the response
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    phone_number: Optional[str]
    role_id: Optional[int]  # Adding the role_id field
    address: Optional[str]  # New field added to match User model
    postal_code: Optional[str]  # New field added to match User model
    city: Optional[str]  # New field added to match User model
    country: Optional[str]  # New field added to match User model
    class Config:
        from_attributes = True 

class UserIn(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str
    address: Optional[str] = None  # New field added to match User model
    postal_code: Optional[str] = None  # New field added to match User model
    city: Optional[str] = None  # New field added to match User model
    country: Optional[str] = None  # New field added to match User model
class UserOut(UserBase):
    id: int
    role_id: Optional[int] = None  # Optional field for role_id
    
    class Config:
        from_attributes = True  # Allows Pydantic to read data from SQLAlchemy models 
    

class UpdateUser(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

   
    class Config:
        from_attributes = True  # Allows Pydantic to read data from SQLAlchemy models

class RoleBase(BaseModel):
    name: str
    class Config:
        from_attributes = True  
class RoleOut(RoleBase):
    id: int

    class Config:
        from_attributes = True  # Allows Pydantic to read data from SQLAlchemy models
class RoleCreate(BaseModel):
    name: str  # The role name (e.g., "admin", "teacher", "student")
    class Config:
        from_attributes = True  
class RoleUpdate(BaseModel):
    name: str 


class SchoolBase(BaseModel):
    id: int
    name: str
    address: str
    phone_number: Optional[str] = None


    class Config:
       from_attributes = True 
class SchoolCreate(BaseModel):
    name: str
    address: str
    phone_number: Optional[str] = None

class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None    


class ClassLevelBase(BaseModel):
    id: int
    name: str
    school_id: Optional[int]  # Foreign key to School table

    class Config:
        from_attributes = True    # Tells Pydantic to treat the SQLAlchemy model as a dict

class ClassLevelCreate(BaseModel):
    name: str
    school_id: Optional[int]  # Foreign key to School table

class ClassLevelUpdate(BaseModel):
    name: Optional[str] = None
    school_id: Optional[int] = None  

class SubjectBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class SubjectCreate(BaseModel):
    name: str

class SubjectUpdate(BaseModel):
    name: str   
class StudentBase(BaseModel):
    date_of_birth: date
    user_id: int
    class_level_id: Optional[int] = None  # This can be None initially
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    date_of_birth: Optional[date] = None
    user_id: Optional[int] = None
    class_level_id: Optional[int] = None  

class StudentOut(StudentBase):
    id: int
    class_level_id: Optional[int] = None   
    user_id: Optional[int] = None  # Nested UserOut model    
    class Config:
        from_attributes = True 
class TeacherBase(BaseModel):
    user_id: int
    subject_id: Optional[int] = None
    qualifications: Optional[str] = None
    photo: Optional[str] = None
    employment_date: date

    class Config:
        from_attributes = True 

class TeacherCreate(TeacherBase):
    pass

class TeacherUpdate(BaseModel):
    qualifications: Optional[str] = None
    photo: Optional[str] = None
    subject_id: Optional[int] = None
    employment_date: Optional[date] = None        
class ParentBase(BaseModel):
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    OuserOut: Optional[UserOut] = None  # Nested UserOut model
    class Config:
        from_attributes = True 
class ParentOut(BaseModel):
    id: int
   
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    # You can include the UserOut model here if you want to embed user data
    user: Optional["UserOut"] = None  # Assuming you have a UserOut model to represent the user
    class Config:
        from_attributes = True  # Allows Pydantic to read data from SQLAlchemy models
      
class ParentCreate(ParentBase):
    pass

class ParentUpdate(BaseModel):
    user_id: Optional[int] = None  # Optional field to update user_id    


class GuardianCreate(BaseModel):
    parent_id: int
    student_id: int

class GuardianUpdate(BaseModel):
    parent_id: Optional[int] = None
    student_id: Optional[int] = None

class GuardianOut(BaseModel):
    id: int
    parent_id: int
    student_id: int
    user: Optional["UserOut"] = None  # Assuming you have a UserOut model to represent the user
    class Config:
        from_attributes = True 