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
class HomeworkCreate(BaseModel):
    title: str
    description: str
    due_date: date
    priority: Optional[str] = "Normal"
    status: Optional[str] = "Pending"
    subject_class_level_id: int        

class HomeworkUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[str] = None
    status: Optional[str] = None
class HomeworkOut(BaseModel):
    id: int
    title: str
    description: str
    due_date: date
    priority: str
    status: str
    subject_class_level_id: int

    class Config:
        from_attributes = True    

class SubjectClassLevelBase(BaseModel):
    id: int
    class_level_id: int
    subject_id: int
    teacher_id: int

    class Config:
        from_attributes = True   
class SubjectClassLevelCreate(BaseModel):
    class_level_id: int
    subject_id: int
    teacher_id: int        
class SubjectClassLevelUpdate(BaseModel):
    class_level_id: Optional[int] = None
    subject_id: Optional[int] = None
    teacher_id: Optional[int] = None    

class GradeBase(BaseModel):
    id: int
    grade: str
    description: Optional[str] = None
    feedback: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    student_homework_id: int

    class Config:
        from_attributes = True   
class GradeCreate(BaseModel):
    grade: str
    description: Optional[str] = None
    feedback: Optional[str] = None
    student_homework_id: int        
class GradeUpdate(BaseModel):
    grade: Optional[str] = None
    description: Optional[str] = None
    feedback: Optional[str] = None    
class StudentHomeworkBase(BaseModel):
    id: int
    student_id: int
    homework_id: int
    file_attachement_id: Optional[int] = None  
    class Config:
        from_attributes = True    
class StudentHomeworkCreate(BaseModel):
    student_id: int
    homework_id: int
    file_attachement_id: Optional[int] = None     
class StudentHomeworkUpdate(BaseModel):
    student_id: Optional[int] = None
    homework_id: Optional[int] = None
    file_attachement_id: Optional[int] = None  

class FileAttachmentBase(BaseModel):
    id: int
    file_name: str
    file_path: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime 
    class Config:
        from_attributes = True     
class FileAttachmentCreate(BaseModel):
    file_name: str
    file_path: str
    description: Optional[str] = None      
class FileAttachmentUpdate(BaseModel):
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    description: Optional[str] = None      
class MessageBase(BaseModel):
    id: int
    message: str
    read_status: str
    created_at: datetime
    updated_at: datetime
    recipient_user_id: int
    sender_user_id: int 
    class Config:
        from_attributes = True     
class MessageCreate(BaseModel):
    message: str
    recipient_user_id: int   
class MessageUpdate(BaseModel):
    read_status: Optional[str] = None  
class RecommendedResourceBase(BaseModel):
    id: int
    title: str
    url: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    subject_id: int 
    class Config:
        from_attributes = True  
class RecommendedResourceCreate(BaseModel):
    title: str
    url: str
    description: Optional[str] = None
    subject_id: int
class RecommendedResourceUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None                      