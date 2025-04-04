from datetime import datetime,timezone
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Date, Table, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from db_setup import Base

# Junction table to link User and Parent
user_parent_association = Table(
    'user_parent_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id', ondelete="CASCADE"), primary_key=True),
    Column('parent_id', Integer, ForeignKey('parent.id', ondelete="CASCADE"), primary_key=True)
)   
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    phone_number = Column(String)
    arskurs_id = Column(Integer, ForeignKey('arskurs.id'), nullable=True)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=True)
    membership_id = Column(Integer, ForeignKey('membership.id'), nullable=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=True)
    parent_id = Column(Integer, ForeignKey("parent.id"), nullable=True)  # Foreign key to Parent table

    # Relationships
    student = relationship("Student", back_populates="user", uselist=False)
    school = relationship("School", back_populates="users")
    role = relationship("Role")
    arskurs = relationship("Arskurs")
    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")
    teacher = relationship("Teacher", back_populates="user", uselist=False)
    betyg = relationship("Betyg", back_populates="user")
    meddelanden = relationship("Meddelande", back_populates="user")
    
    # Many-to-many relationship with Parent using the junction table
    parents = relationship(
        'Parent', 
        secondary=user_parent_association, 
        back_populates='users'
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
 
class Token(Base):
    __tablename__ = "token"

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    # Add the relationship to the User model
    user = relationship("User", back_populates="tokens")
# Association table for many-to-many relationship between Arskurs and Teacher
arskurs_teacher_association = Table(
    "arskurs_teacher",
    Base.metadata,
    Column("arskurs_id", Integer, ForeignKey("arskurs.id", ondelete="CASCADE"), primary_key=True),
    Column("teacher_id", Integer, ForeignKey("teacher.id", ondelete="CASCADE"), primary_key=True)
)
class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)  # ForeignKey to User table
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=True)  # Optional: Subject the teacher teaches
  
    qualifications = Column(Text, nullable=True)  # Teacher's qualifications
    photo = Column(String, nullable=True)
    homeworks = relationship("Homework", back_populates="teacher")  # Use back_populates
    user = relationship("User", back_populates="teacher")  
    subject = relationship("Subject", backref="teachers")  # Optional: Subject table if you want to associate teachers with subjects
   
      # Many-to-many relationship with Arskurs
    arskurser = relationship("Arskurs", secondary=arskurs_teacher_association, back_populates="teachers")
    def __repr__(self):
        return f"<Teacher(id={self.id}, user_id={self.user_id}, qualifications={self.qualifications})>"

    
class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    phone_number = Column(String(15), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationship to User
    arskurser = relationship("Arskurs", back_populates="skola")
    users = relationship("User", back_populates="school")  # One-to-many relationship
class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)  # Foreign key to User table
    arskurs_id = Column(Integer, ForeignKey("arskurs.id", ondelete="SET NULL"), nullable=True)  # Foreign key to Arskurs table
    enrollment_date = Column(Date, nullable=False)  # Date of enrollment
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="student")  # One-to-one relationship with User
    arskurs = relationship("Arskurs", back_populates="students")  # Many-to-one relationship with Arskurs

    # Many-to-many relationship with Parent
    parents = relationship(
        "Parent",
        secondary="parent_student_association",
        back_populates="children"
    )

    def __repr__(self):
        return f"<Student(id={self.id}, user_id={self.user_id}, arskurs_id={self.arskurs_id})>"

class Parent(Base):
    __tablename__ = "parent"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(15), nullable=True)  # Parent's phone number
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    users = relationship(
        'User', 
        secondary=user_parent_association, 
        back_populates='parents'
    )

    children = relationship(
        "Student", 
        secondary="parent_student_association", 
        back_populates="parents"
    )  # Many-to-many relationship with Student

    def __repr__(self):
        return f"<Parent(id={self.id}, phone_number={self.phone_number})>"
parent_student_association = Table(
    "parent_student_association",
    Base.metadata,
    Column("parent_id", Integer, ForeignKey("parent.id", ondelete="CASCADE"), primary_key=True),
    Column("student_id", Integer, ForeignKey("student.id", ondelete="CASCADE"), primary_key=True)
)     
class Role(Base):
    __tablename__ = "role"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)    

class Membership(Base):
    __tablename__ = "membership"

    id = Column(Integer, primary_key=True, index=True)
    membership_type = Column(String, nullable=False)  # Type of membership (e.g., 'Premium', 'Basic')
    start_date = Column(Date, nullable=False)  # Start date of the membership
    end_date = Column(Date, nullable=False)  # End date of the membership
    


class Arskurs(Base):
    __tablename__ = "arskurs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    skola_id = Column(Integer, ForeignKey("schools.id"), nullable=True)  # Foreign key to School table
    klass = Column(String, nullable=True)
    # Define the relationship to the School model
    skola = relationship("School", back_populates="arskurser")
    # Many-to-many relationship with Teacher
    teachers = relationship("Teacher", secondary=arskurs_teacher_association, back_populates="arskurser")

    # One-to-many relationship with Student
    students = relationship("Student", back_populates="arskurs")  # Add this relationship

    __table_args__ = (
        UniqueConstraint("name", "skola_id", "klass", name="unique_name_skola_klass"),
    )

    def __repr__(self):
        return f"<Arskurs(id={self.id}, name={self.name}, skola_id={self.skola_id}, klass={self.klass})>"
class Homework(Base):
    __tablename__ = "homework"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    due_date = Column(Date)
    status = Column(String, default="Pending")
    priority = Column(String, default="Normal")

    # Direct reference to Teacher table
    teacher_id = Column(Integer, ForeignKey("teacher.id"), nullable=True)
    teacher = relationship("Teacher", back_populates="homeworks")  # Use back_populates

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")

    subject_id = Column(Integer, ForeignKey("subject.id"))  # Foreign key referencing the Subject table
    subject = relationship("Subject")
    betyg = relationship("Betyg", back_populates="homework", uselist=False)
    meddelande = relationship("Meddelande", back_populates="homework", uselist=False)
    filuppladdning = relationship("Filuppladdning", back_populates="homework", uselist=False)
    recommended_resource = relationship("RecommendedResource", back_populates="homework", uselist=False)

    def __repr__(self):
        return f"<Homework(id={self.id}, title={self.title}, due_date={self.due_date}, status={self.status})>"
class Subject(Base):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
   

class Betyg(Base):
    __tablename__ = "betyg"

    id = Column(Integer, primary_key=True, index=True)
    grade = Column(String, nullable=False)
    comments = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)  # New column for feedback
    created_at = Column(DateTime,  default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    homework_id = Column(Integer, ForeignKey("homework.id"))
    homework = relationship("Homework")    
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="betyg")

class Filuppladdning(Base):
    __tablename__ = "filuppladdning"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    description = Column(Text, nullable=True)  # New column for description
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    homework_id = Column(Integer, ForeignKey("homework.id"))
    homework = relationship("Homework")

class Meddelande(Base):
    __tablename__ = "meddelande"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    description = Column(Text, nullable=True)  # New column for description
    read_status = Column(String, default="Unread")  # New column for read_status
    type = Column( nullable=False, default="general")  # New ENUM column
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    homework_id = Column(Integer, ForeignKey("homework.id"))
    homework = relationship("Homework")

    # Add user_id as a foreign key
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="meddelanden")  # Relationship to the User model

class RecommendedResource(Base):
    __tablename__ = "recommended_resource"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    homework_id = Column(Integer, ForeignKey("homework.id"))
    homework = relationship("Homework")


