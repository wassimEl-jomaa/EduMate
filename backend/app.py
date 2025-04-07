from datetime import datetime, timezone
from typing import List
from fastapi import FastAPI, HTTPException, Depends, Security

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import update
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from db_setup import get_db, create_databases
from models import  User, Token
from auth import create_database_token, generate_token, get_current_user, get_password_hash, token_expiry
from passlib.context import CryptContext
from db_setup import get_db
import crud
import uvicorn
from schemas import RoleBase as RoleSchema
from schemas import UserBase, UserIn, UserOut,GetUser, UpdateUser,RoleBase, RoleOut,RoleCreate,RoleUpdate,SchoolBase
from models import  User
from models import Role ,School, Teacher, Student, Parent,Class_Level,Token,Subject
from schemas import UserOut,SchoolBase,SchoolCreate,SchoolUpdate,ClassLevelBase,ClassLevelCreate,ClassLevelUpdate,SubjectBase,SubjectUpdate,SubjectCreate

# Initialize the FastAPI app
app = FastAPI()
security = HTTPBearer()
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    """
    Get the current user from the token.
    """
    token = credentials.credentials  # Extract the token from the Authorization header
    db_token = db.query(Token).filter(Token.token == token).first()
    if not db_token or db_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return db_token.user
app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
create_databases()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)




@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
   
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
       
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = create_database_token(user, db)
  

    return token_data
@app.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    """
    Logout the user by deleting the token from the database.
    """
    token = credentials.credentials  # Extract the token from the Authorization header
    db_token = db.query(Token).filter(Token.token == token).first()
    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    db.delete(db_token)
    db.commit()
    return {"message": "Logged out successfully"}


# Protected route example
@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    """
    A protected route that requires authentication.
    """
    return {"message": f"Hello, {current_user.username}!"}

@app.get("/users/", response_model=List[UserOut])
def read_users(current_user: User = Depends(get_current_user),
    database: Session = Depends(get_db)):
    """
     Hämtar alla användare från databasen.
    """
    users = database.query(User).all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    return users
@app.get("/user-profile")
def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Retrieve the profile of the currently authenticated user.
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
    }
@app.get("/users/{user_id}", response_model=UserOut)
def get_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Retrieve a user by ID from the database.
    """
    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=UserOut)
def add_users(
    user_params: UserIn,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Create a new user in the database.
    """
    # Check if the email is already registered
    existing_user = database.query(User).filter(User.email == user_params.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Query the Role model
    role_instance = database.query(Role).filter(Role.id == 1).first()
    if not role_instance:
        raise HTTPException(status_code=404, detail="Role not found")

    # Hash the password before saving
    hashed_password = get_password_hash(user_params.password)
    new_user = User(
        username=user_params.username,
        first_name=user_params.first_name,
        last_name=user_params.last_name,
        email=user_params.email,
        password=hashed_password,  # Store the hashed password
        phone_number=user_params.phone_number,
        role=role_instance,  # Default role for new users
        address=user_params.address,
        postal_code=user_params.postal_code,
        city=user_params.city,
        country=user_params.country
    )
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user
    
@app.post("/get_user_by_email_and_password")
def get_user_by_email_and_password(
    user: GetUser,
    db: Session = Depends(get_db)
):
    """
    Authenticate the user and return a token.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return create_database_token(db_user, db)
@app.delete("/users/{user_id}")
def delete_user_view(
    user_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Delete a user from the database, including all related entities like tokens, teachers, and students.
    """
    # Check if the user exists
    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Authorization check: Ensure the current user has the rights to delete another user
    if current_user.role.name != 'Admin':  # Assuming 'admin' role can delete users
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")

    # Delete related tokens (cascade is handled by SQLAlchemy, but ensuring it's explicitly clear)
    database.query(Token).filter(Token.user_id == user_id).delete(synchronize_session=False)

    # If the user is a Teacher, delete related teacher profile
    if user.teacher:
        database.query(Teacher).filter(Teacher.user_id == user_id).delete(synchronize_session=False)

    # If the user is a Student, delete related student profile
    if user.student:
        database.query(Student).filter(Student.user_id == user_id).delete(synchronize_session=False)

    # If the user is a Parent, delete related parent profile
    if user.parent:
        database.query(Parent).filter(Parent.user_id == user_id).delete(synchronize_session=False)

    # Delete the user
    database.delete(user)
    database.commit()

    return {"message": f"User with ID {user_id} has been deleted successfully"}
@app.put("/users/{user_id}", response_model=UserBase)
def update_user_view(
    user_id: int,
    update_data: UpdateUser,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Update a user by ID.
    Only authorized users can update (e.g., the user themselves or an admin).
    """
    # Check if the user exists
    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the current user has permission to update the user
    if current_user.id != user_id and current_user.role.name != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to update this user")

    # Update user fields
    if update_data.username:
        user.username = update_data.username
    if update_data.first_name:
        user.first_name = update_data.first_name
    if update_data.last_name:
        user.last_name = update_data.last_name
    if update_data.email:
        user.email = update_data.email
    if update_data.phone_number:
        user.phone_number = update_data.phone_number
    if update_data.address:
        user.address = update_data.address
    if update_data.postal_code:
        user.postal_code = update_data.postal_code
    if update_data.city:
        user.city = update_data.city
    if update_data.country:
        user.country = update_data.country

    # Commit the changes to the database
    database.commit()
    database.refresh(user)

    return user 
# Get all roles
@app.get("/roles", response_model=List[RoleBase])
def read_all_roles(
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Get all roles from the database.
    """
    # Ensure the user is authenticated or authorized (optional)
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    roles = database.query(Role).all()  # Fetch all roles from the database
    return roles

@app.post("/roles", response_model=RoleBase)
def add_role(role_data: RoleCreate, 
             current_user: User = Depends(get_current_user),  # Validate token and authenticate user
             database: Session = Depends(get_db)):
    """
    Add a new role to the database.
    """
    # Check if the role already exists
    existing_role = database.query(Role).filter(Role.name == role_data.name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    # Create the new role
    new_role = Role(name=role_data.name)
    database.add(new_role)
    database.commit()
    database.refresh(new_role)

    return new_role
@app.delete("/roles/{role_id}")
def delete_role(
    role_id: int,
    current_user: User = Depends(get_current_user),
    database: Session = Depends(get_db)
):
    """
    Delete a role by ID from the database.
    """
    # Check if the user has necessary permissions (e.g., only admins can delete roles)
    if current_user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete roles")

    # Check if the role exists
    role = database.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Delete the role from the database
    database.delete(role)
    try:
        database.commit()
        print(f"Role {role_id} has been deleted.")
    except Exception as e:
        print(f"Error occurred: {e}")
        database.rollback()  # Rollback if there's an error

    return {"message": f"Role with ID {role_id} has been deleted successfully"}
@app.put("/roles/{role_id}", response_model=RoleBase)
def update_role(
    role_id: int, 
    role_update: RoleUpdate, 
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Update the name of a role in the database by role_id.
    """
    # Check if the user has necessary permissions (e.g., only admins can update roles)
    if current_user.role.name != "Admin":  # You can customize this check as per your role structure
        raise HTTPException(status_code=403, detail="Not authorized to update roles")

    # Check if the role exists
    role = database.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Update the role's attributes
    role.name = role_update.name  # Update the role name with the new value

    # Commit the changes to the database
    database.commit()

    # Return the updated role
    return role  # This will automatically be serialized into the RoleBase Pydantic model

@app.get("/schools", response_model=List[SchoolBase])
def read_all_schools(
    current_user: User = Depends(get_current_user),  # Token validation and user authentication
    database: Session = Depends(get_db)
):
    """
    Get all schools from the database. The request will be validated by checking the token.
    """
    schools = database.query(School).all()
    return schools

@app.post("/schools", response_model=SchoolBase)
def add_school(
    school_data: SchoolCreate,
    current_user: User = Depends(get_current_user),  # Token validation and user authentication
    database: Session = Depends(get_db)
):
    """
    Add a new school to the database.
    """
    # Check if a school with the same name already exists
    existing_school = database.query(School).filter(School.name == school_data.name).first()
    if existing_school:
        raise HTTPException(status_code=400, detail="School with this name already exists")

    # Create and add the new school
    new_school = School(
        name=school_data.name,
        address=school_data.address,
        phone_number=school_data.phone_number
    )
    database.add(new_school)
    database.commit()
    database.refresh(new_school)

    return new_school

# Delete a school by ID
@app.delete("/schools/{school_id}", response_model=SchoolBase)
def delete_school(
    school_id: int,
    current_user: User = Depends(get_current_user),  # Token validation and user authentication
    database: Session = Depends(get_db)
):
    """
    Delete a school by its ID.
    """
    school = database.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    # Delete the school
    database.delete(school)
    database.commit()

    return school

# Update a school by ID
@app.put("/schools/{school_id}", response_model=SchoolBase)
def update_school(
    school_id: int,
    school_update: SchoolUpdate,
    current_user: User = Depends(get_current_user),  # Token validation and user authentication
    database: Session = Depends(get_db)
):
    """
    Update a school by ID.
    """
    school = database.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    # Update the school's attributes
    if school_update.name:
        school.name = school_update.name
    if school_update.address:
        school.address = school_update.address
    if school_update.phone_number:
        school.phone_number = school_update.phone_number

    # Commit the changes to the database
    database.commit()
    database.refresh(school)
# Create a new class level
@app.post("/class_levels", response_model=ClassLevelBase)
def add_class_level(
    class_level_data: ClassLevelCreate,
    current_user: User = Depends(get_current_user),  # Token validation and user authentication
    database: Session = Depends(get_db)
):
    """
    Add a new class level to the database.
    """
    # Check if the class level with the same name already exists
    existing_class_level = database.query(Class_Level).filter(Class_Level.name == class_level_data.name).first()
    if existing_class_level:
        raise HTTPException(status_code=400, detail="Class level with this name already exists")

    # Create and add the new class level
    new_class_level = Class_Level(
        name=class_level_data.name,
        school_id=class_level_data.school_id
    )
    database.add(new_class_level)
    database.commit()
    database.refresh(new_class_level)

    return new_class_level

# Get all class levels
@app.get("/class_levels", response_model=List[ClassLevelBase])
def read_all_class_levels(
    current_user: User = Depends(get_current_user),  # Token validation and user authentication
    database: Session = Depends(get_db)
):
    """
    Get all class levels from the database.
    """
    class_levels = database.query(Class_Level).all()
    return class_levels

# Update a class level by ID
@app.put("/class_levels/{class_level_id}", response_model=ClassLevelBase)
def update_class_level(
    class_level_id: int,
    class_level_update: ClassLevelUpdate,
    current_user: User = Depends(get_current_user),  # Token validation and user authentication
    database: Session = Depends(get_db)
):
    """
    Update a class level by its ID.
    """
    class_level = database.query(Class_Level).filter(Class_Level.id == class_level_id).first()
    if not class_level:
        raise HTTPException(status_code=404, detail="Class level not found")

    # Update the class level's attributes
    if class_level_update.name:
        class_level.name = class_level_update.name
    if class_level_update.school_id:
        class_level.school_id = class_level_update.school_id

    # Commit the changes to the database
    database.commit()
    database.refresh(class_level)

    return class_level

# Delete a class level by ID
@app.delete("/class_levels/{class_level_id}", response_model=ClassLevelBase)
def delete_class_level(
    class_level_id: int,
    current_user: User = Depends(get_current_user),  # Token validation and user authentication
    database: Session = Depends(get_db)
):
    """
    Delete a class level by its ID.
    """
    class_level = database.query(Class_Level).filter(Class_Level.id == class_level_id).first()
    if not class_level:
        raise HTTPException(status_code=404, detail="Class level not found")

    # Delete the class level
    database.delete(class_level)
    database.commit()

    return class_level
    return school   


@app.get("/subjects", response_model=List[SubjectBase])
def read_all_subjects(current_user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    """
    Get all subjects from the database.
    """
    subjects = database.query(Subject).all()
    return subjects   
@app.post("/subjects", response_model=SubjectBase)
def add_subject(subject_data: SubjectCreate, current_user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    """
    Add a new subject to the database.
    """
    # Check if the subject already exists
    existing_subject = database.query(Subject).filter(Subject.name == subject_data.name).first()
    if existing_subject:
        raise HTTPException(status_code=400, detail="Subject already exists")

    # Create the new subject
    new_subject = Subject(name=subject_data.name)
    database.add(new_subject)
    database.commit()
    database.refresh(new_subject)

    return new_subject    
@app.put("/subjects/{subject_id}", response_model=SubjectBase)
def update_subject(subject_id: int, subject_update: SubjectUpdate, current_user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    """
    Update the subject by ID.
    """
    # Check if the subject exists
    subject = database.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    # Update the subject's name
    subject.name = subject_update.name

    # Commit the changes to the database
    database.commit()
    database.refresh(subject)

    return subject
@app.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int, current_user: User = Depends(get_current_user), database: Session = Depends(get_db)):
    """
    Delete a subject by ID from the database.
    """
    # Check if the subject exists
    subject = database.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    # Delete the subject
    database.delete(subject)
    database.commit()

    return {"message": f"Subject with ID {subject_id} has been deleted successfully"}
    return subject     
if __name__ == '__main__':
    uvicorn.run(app)