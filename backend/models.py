from datetime import datetime,timezone
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Date, Table, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from db_setup import Base

 
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    phone_number = Column(String)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=True)
    address = Column(Text, nullable=True)
    postal_code = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    
    # Relationships
    student = relationship("Student", back_populates="user", uselist=False)
    role = relationship("Role")
    token = relationship("Token", back_populates="user", cascade="all, delete-orphan")
    teacher = relationship("Teacher", back_populates="user", uselist=False)
    parent = relationship("Parent", back_populates="user")

 
class Token(Base):
    __tablename__ = "token"

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    # Add the relationship to the User model
    user = relationship("User", back_populates="token")



 
class Student_Homework(Base):
    __tablename__ = "student_homework"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id", ondelete="CASCADE"))
    homework_id = Column(Integer, ForeignKey("homework.id", ondelete="CASCADE"))
    file_attachement_id = Column(Integer, ForeignKey("file_attachment.id", ondelete="CASCADE"))

    student = relationship("Student", back_populates="student_homework")
    homework = relationship("Homework", back_populates="student_homework")
    file_attachment = relationship("File_Attachment", back_populates="student_homework")  # Use back_populates
    grade = relationship("Grade", back_populates="student_homework")  # Use back_populates

class Guardian(Base):
    __tablename__ = "guardian"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("parent.id", ondelete="CASCADE"))
    student_id = Column(Integer, ForeignKey("student.id", ondelete="CASCADE"))

    parent = relationship("Parent", back_populates="guardian")
    student = relationship("Student", back_populates="guardian")


class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)  # ForeignKey to User table
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=True)  # Optional: Subject the teacher teaches
    qualifications = Column(Text, nullable=True)  # Teacher's qualifications
    photo = Column(String, nullable=True)
    employment_date = Column(Date, nullable=False)  # Date of employment
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    user = relationship("User", back_populates="teacher")  
    subject = relationship("Subject", backref="teacher")  # Optional: Subject table if you want to associate teachers with subjects

    subject_class_level = relationship("Subject_Class_Level", back_populates="teacher")  # Many-to-one relationship with Arskurs
    
class School(Base):
    __tablename__ = "school"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    phone_number = Column(String(15), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    class_level = relationship("Class_Level", back_populates="school")

class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    date_of_birth = Column(Date, nullable=False)  # Student's date of birth
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)  # Foreign key to User table
    class_level_id = Column(Integer, ForeignKey("class_level.id", ondelete="SET NULL"), nullable=True)  # Foreign key to Arskurs table
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="student")  # One-to-one relationship with User
    class_level = relationship("Class_Level", back_populates="student")  # Many-to-one relationship with Arskurs
    homework = relationship("Homework", secondary="student_homework", back_populates="student")  # Many-to-one relationship with Arskurs
    student_homework = relationship("Student_Homework", back_populates="student")  # Many-to-one relationship with Arskurs
    guardian = relationship("Guardian", back_populates="student")  # Many-to-one relationship with Guardian

class Parent(Base):
    __tablename__ = "parent"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)  # Foreign key to User table
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="parent")  # One-to-one relationship with User
    guardian = relationship("Guardian", back_populates="parent")  # Many-to-one relationship with Guardian

    
class Role(Base):
    __tablename__ = "role"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)   
   
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="role")  # One-to-one relationship with User





class Homework(Base):
    __tablename__ = "homework"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    due_date = Column(Date)
    status = Column(String, default="Pending")
    priority = Column(String, default="Normal")
    subject_class_level_id = Column(Integer, ForeignKey("subject_class_level.id"))  # Foreign key referencing the Subject table
    file_attachment_id = Column(Integer, ForeignKey("file_attachment.id"))  # Foreign key referencing the Subject table

    # Direct reference to Teacher table
    subject_class_level = relationship("Subject_Class_Level", back_populates="homework")  # Use back_populates
    student = relationship("Student", secondary="student_homework", back_populates="homework")  # Use back_populates

    file_attachment = relationship("File_Attachment", back_populates="homework", uselist=False)
    student_homework = relationship("Student_Homework", back_populates="homework")  # Use back_populates

class Subject(Base):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Direct reference to Teacher table
    class_level = relationship("Class_Level", secondary="subject_class_level", back_populates="subject")  # Use back_populates
    recommended_resource = relationship("Recommended_Resource", back_populates="subject")  # Use back_populates
class Subject_Class_Level(Base):
    __tablename__ = "subject_class_level"

    id = Column(Integer, primary_key=True, index=True)
    class_level_id = Column(Integer, ForeignKey("class_level.id", ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey("subject.id", ondelete="CASCADE"))
    teacher_id = Column(Integer, ForeignKey("teacher.id", ondelete="CASCADE"))
    
    class_level = relationship('Class_Level', backref='subject_class_level')
    subject = relationship('Subject', backref='subject_class_level')
    teacher = relationship('Teacher', back_populates='subject_class_level')
    homework = relationship("Homework", back_populates="subject_class_level")  # Use back_populates    
class Class_Level(Base):
    __tablename__ = "class_level"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    school_id = Column(Integer, ForeignKey("school.id"), nullable=True)  # Foreign key to School table
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Define the relationship to the School model
    school = relationship("School", back_populates="class_level")
    subject = relationship("Subject", secondary="subject_class_level", back_populates="class_level")  # Many-to-one relationship with Arskurs
    student = relationship("Student", back_populates="class_level")  # Add this relationship   
 
class Grade(Base):
    __tablename__ = "grade"

    id = Column(Integer, primary_key=True, index=True)
    grade = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)  # New column for feedback
    created_at = Column(DateTime,  default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    student_homework_id = Column(Integer, ForeignKey("student_homework.id"))
    student_homework = relationship("Student_Homework" , back_populates="grade")    

class File_Attachment(Base):
    __tablename__ = "file_attachment"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    description = Column(Text, nullable=True)  # New column for description
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    homework = relationship("Homework", back_populates="file_attachment")  # Use back_populates
    student_homework = relationship("Student_Homework", back_populates="file_attachment")  # Use back_populates

class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    read_status = Column(String, default="Unread")  # New column for read_status
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Add user_id as a foreign key
    recipient_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    sender_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    
    # Define separate relationships for recipient and sender
    recipient_user = relationship("User", foreign_keys=[recipient_user_id], backref="received_messages")
    sender_user = relationship("User", foreign_keys=[sender_user_id], backref="sent_messages")

class Recommended_Resource(Base):
    __tablename__ = "recommended_resource"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    subject_id = Column(Integer, ForeignKey("subject.id"))
    subject = relationship("Subject" , back_populates="recommended_resource")  # Use back_populates


