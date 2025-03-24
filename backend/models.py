from datetime import datetime,timezone
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Date, Text, UniqueConstraint
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
    arskurs_id = Column(Integer, ForeignKey('arskurs.id'), nullable=True)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=True)
    membership_id = Column(Integer, ForeignKey('membership.id'), nullable=True)

    membership = relationship("Membership")
    role = relationship("Role")
    arskurs = relationship("Arskurs")
    tokens = relationship("Token", back_populates="user")
    teacher = relationship("Teacher", back_populates="user", uselist=False)  # One-to-one relationship with Teacher
    betyg = relationship("Betyg", back_populates="user")
class Token(Base):
    __tablename__ = "token"
    user_id = Column(Integer, ForeignKey("user.id"), unique=True, nullable=False, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)  # Token expiration time
    user = relationship("User", back_populates="tokens")

class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # ForeignKey to User table
    subject_id = Column(Integer, ForeignKey('subject.id'), nullable=True)  # Optional: Subject the teacher teaches
    qualifications = Column(Text, nullable=True)  # Teacher's qualifications

    user = relationship("User", back_populates="teacher")  # Use back_populates instead of backref
    subject = relationship("Subject", backref="teachers")  # Optional: Subject table if you want to associate teachers with subjects

    def __repr__(self):
        return f"<Teacher(id={self.id}, user_id={self.user_id}, qualifications={self.qualifications})>"
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
    skola = Column(String)  # Add skola field
    klass = Column(String)  # Add klass field
    __table_args__ = (
        UniqueConstraint("name", "skola", "klass", name="unique_name_skola_klass"),
    )

class Homework(Base):
    __tablename__ = "homework"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    due_date = Column(Date)
    status = Column(String, default="Pending")
    priority = Column(String, default="Normal")

    # Direct reference to Teacher table instead of User
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    teacher = relationship("Teacher", backref="homeworks")

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")

    subject_id = Column(Integer, ForeignKey('subject.id'))  # Foreign key referencing the Subject table
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
    created_at = Column(DateTime,  default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    homework_id = Column(Integer, ForeignKey("homework.id"))
    homework = relationship("Homework")   

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


