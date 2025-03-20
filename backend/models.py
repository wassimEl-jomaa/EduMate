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

    arskurs_id = Column(Integer, ForeignKey('arskurs.id'), default=0)  # Foreign key referencing the Arskurs table
    role_id = Column(Integer, ForeignKey('role.id'), default=0)  # Foreign key referencing the Role table
    membership_id = Column(Integer, ForeignKey('membership.id'))  # Foreign key referencing the Role table
    membership = relationship("Membership")
    role = relationship("Role")
    arskurs = relationship("Arskurs")
    tokens = relationship("Token", back_populates="user")
class Token(Base):
    __tablename__ = "token"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)  # Token expiration time
    user = relationship("User", back_populates="tokens")

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


