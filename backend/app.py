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
from models import Teacher, User, Token
from auth import create_database_token, generate_token, get_current_user, get_password_hash, token_expiry
from passlib.context import CryptContext
from db_setup import get_db
import crud
import uvicorn
from schemas import ArskursCreate, Arskurs as ArskursSchema, BetygCreate, BetygOut, BetygUpdate, FiluppladdningCreate, FiluppladdningOut, HomeworkCreate, HomeworkInUpdate, MeddelandeCreate, MeddelandeOut, MembershipUpdate, RecommendedResourceCreate, RecommendedResourceOut, SubjectCreate, SubjectOut, TeacherCreate, UserInUpdate
from schemas import GetUser, HomeworkBase, HomeworkOut, UserIn, UserOut, MembershipOut
from models import Arskurs, Betyg, Filuppladdning, Homework, Meddelande, RecommendedResource, Role, Subject, User, Membership
from schemas import MembershipCreate
from schemas import UserOut, RoleOut

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

    # Create or retrieve a token for the user
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
        role=role_instance  # Default role for new users
    )
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user
    
@app.post("/get_user_by_email_and_password")
def get_user_by_email_and_password(
    user: GetUser,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    db: Session = Depends(get_db)
):
    """
    Fetch a user by email and password, ensuring the request is authenticated.
    """
    # Fetch the user by email
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
    Delete a user from the database.
    """
    # Check if the user exists
    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Perform the deletion
    database.delete(user)
    database.commit()
    return {"message": f"User with ID {user_id} has been deleted successfully"}
@app.patch("/users/{user_id}", response_model=UserOut)
def update_user_by_id(
    user_id: int,
    user_params: UserInUpdate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Update a user by ID in the database.
    """
    # Check if the user exists
    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user with the provided fields
    database.execute(
        update(User)
        .where(User.id == user_id)
        .values(user_params.model_dump(exclude_none=True))  # Exclude None values
    )
    database.commit()

    # Retrieve the updated user
    updated_user = database.query(User).filter(User.id == user_id).first()
    return updated_user
@app.post("/teachers/", response_model=dict)
def add_teacher(
    teacher_params: TeacherCreate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    db: Session = Depends(get_db)
):
    """
    Create a new teacher in the database.
    """
    existing_teacher = db.query(Teacher).filter(Teacher.user_id == teacher_params.user_id).first()
    if existing_teacher:
        raise HTTPException(status_code=400, detail="Teacher profile already exists for this user")

    new_teacher = Teacher(
        user_id=teacher_params.user_id,
        subject_id=teacher_params.subject_id,
        qualifications=teacher_params.qualifications,
    )
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return {"message": "Teacher created successfully", "teacher_id": new_teacher.id}


@app.get("/teachers/", response_model=List[TeacherCreate])
def get_all_teachers(
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    db: Session = Depends(get_db)
):
    """
    Retrieve all teachers from the database.
    """
    teachers = db.query(Teacher).all()
    if not teachers:
        raise HTTPException(status_code=404, detail="No teachers found")
    return teachers

@app.post("/memberships/", response_model=MembershipOut)
def create_membership(
    membership: MembershipCreate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Create a new membership in the database.
    """
    new_membership = Membership(
        membership_type=membership.membership_type,
        start_date=membership.start_date,
        end_date=membership.end_date,
    )
    database.add(new_membership)
    database.commit()
    database.refresh(new_membership)
    return new_membership


@app.get("/memberships/", response_model=List[MembershipOut])
def read_memberships(
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Retrieve all memberships from the database.
    """
    memberships = crud.get_all_memberships(database)
    if not memberships:
        raise HTTPException(status_code=404, detail="No memberships found")
    return memberships


@app.put("/memberships/{membership_id}", response_model=MembershipOut)
def replace_membership(
    membership_id: int,
    membership: MembershipCreate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Replace an existing membership.
    """
    db_membership = database.query(Membership).filter(Membership.id == membership_id).first()
    if not db_membership:
        raise HTTPException(status_code=404, detail="Membership not found")

    db_membership.membership_type = membership.membership_type
    db_membership.start_date = membership.start_date
    db_membership.end_date = membership.end_date

    database.commit()
    database.refresh(db_membership)
    return db_membership


@app.delete("/memberships/{membership_id}")
def delete_membership_view(
    membership_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Delete a membership from the database.
    """
    return crud.delete_membership(database, membership_id)

# Endpoint to create a new role
@app.post("/roles/", response_model=RoleOut)
def create_role(role_name: str, database: Session = Depends(get_db)):
    """
    Create a new role in the database.
    """
    role = crud.add_role(database, role_name)
    return role

# Endpoint to assign a role to a user
@app.post("/roles/", response_model=RoleOut)
def create_role(
    role_name: str,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Create a new role in the database.
    """
    role = crud.add_role(database, role_name)
    return role


@app.post("/users/{user_id}/roles/{role_id}")
def assign_role_to_user(
    user_id: int,
    role_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Assign a role to a user.
    """
    user = crud.add_role_to_user(database, user_id, role_id)
    return user


@app.get("/roles/", response_model=List[RoleOut])
def get_roles(
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Retrieve all roles from the database.
    """
    roles = crud.get_all_roles(database)
    return roles


@app.get("/roles/{role_name}/users", response_model=List[UserOut])
def get_users_by_role(
    role_name: str,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Retrieve all users with a specific role.
    """
    users = crud.get_users_by_role(database, role_name)
    return users

@app.patch("/roles/{role_id}", response_model=RoleOut)
def update_role(
    role_id: int,
    role_name: str,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Update an existing role's name.
    """
    db_role = database.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")

    db_role.name = role_name  # Update the role's name
    database.commit()
    database.refresh(db_role)
    return db_role


@app.delete("/roles/{role_id}", response_model=RoleOut)
def delete_role(
    role_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Delete a role from the database.
    """
    db_role = database.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")

    database.delete(db_role)
    database.commit()
    return db_role
# Create homework
@app.post("/homeworks/", response_model=HomeworkOut)
def create_homework_view(
    homework: HomeworkCreate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Create a new homework in the database.
    """
    user = database.query(User).filter(User.id == homework.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_homework = Homework(
        title=homework.title,
        description=homework.description,
        due_date=homework.due_date,
        user_id=homework.user_id,
        subject_id=homework.subject_id
    )

    database.add(new_homework)
    database.commit()
    database.refresh(new_homework)
    return new_homework


@app.get("/homeworks/", response_model=List[HomeworkOut])
def get_homeworks_view(
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Retrieve all homeworks from the database.
    """
    homeworks = database.query(Homework).all()
    if not homeworks:
        raise HTTPException(status_code=404, detail="No homeworks found")
    return homeworks


@app.get("/homeworks/{user_id}", response_model=List[HomeworkOut])
def get_homework_by_user_view(
    user_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Retrieve all homeworks for a specific user.
    """
    homeworks = crud.get_homework_by_user(database, user_id)
    if not homeworks:
        raise HTTPException(status_code=404, detail="No homeworks found for this user")
    return homeworks


@app.patch("/homeworks/{homework_id}", response_model=HomeworkOut)
def update_homework_by_id(
    homework_id: int,
    homework: HomeworkInUpdate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Update a homework by ID in the database.
    """
    db_homework = database.query(Homework).filter(Homework.id == homework_id).first()
    if not db_homework:
        raise HTTPException(status_code=404, detail="Homework not found")

    for key, value in homework.dict(exclude_unset=True).items():
        setattr(db_homework, key, value)

    database.commit()
    database.refresh(db_homework)
    return db_homework


@app.delete("/homeworks/{homework_id}/")
def delete_homework(
    homework_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Delete a homework from the database.
    """
    homework = database.query(Homework).filter(Homework.id == homework_id).first()
    if not homework:
        raise HTTPException(status_code=404, detail="Homework not found")

    database.delete(homework)
    database.commit()
    return {"message": "Homework deleted successfully"}

# Create recommended resource
@app.post("/recommended_resources/", response_model=RecommendedResourceOut)
def create_recommended_resource_view(
    resource: RecommendedResourceCreate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Create a new recommended resource in the database.
    """
    return crud.create_recommended_resource(database, resource)


@app.get("/recommended_resources/", response_model=List[RecommendedResourceOut])
def read_all_recommended_resources(
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Retrieve all recommended resources from the database.
    """
    resources = database.query(RecommendedResource).all()
    if not resources:
        raise HTTPException(status_code=404, detail="No recommended resources found")
    return resources


@app.delete("/recommended_resources/{resource_id}", response_model=RecommendedResourceOut)
def delete_recommended_resource(
    resource_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Delete a recommended resource from the database.
    """
    db_resource = database.query(RecommendedResource).filter(RecommendedResource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Recommended resource not found")

    database.delete(db_resource)
    database.commit()
    return db_resource


@app.patch("/recommended_resources/{resource_id}", response_model=RecommendedResourceOut)
def update_recommended_resource(
    resource_id: int,
    resource: RecommendedResourceCreate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Update an existing recommended resource in the database.
    """
    db_resource = database.query(RecommendedResource).filter(RecommendedResource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Recommended resource not found")

    if resource.title is not None:
        db_resource.title = resource.title
    if resource.url is not None:
        db_resource.url = resource.url
    if resource.description is not None:
        db_resource.description = resource.description
    if resource.homework_id is not None:
        db_resource.homework_id = resource.homework_id

    database.commit()
    database.refresh(db_resource)
    return db_resource

@app.get("/betyg/", response_model=List[BetygOut])
def read_betyg(
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Retrieve all betyg from the database.
    """
    betyg = crud.get_all_betyg(database)
    if not betyg:
        raise HTTPException(status_code=404, detail="No betyg found")
    return betyg


@app.get("/betyg/user/{user_id}")
def get_betyg_by_user(
    user_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    db: Session = Depends(get_db)
):
    """
    Retrieve all grades for a specific user.
    """
    betyg = db.query(Betyg).filter(Betyg.user_id == user_id).all()
    if not betyg:
        raise HTTPException(status_code=404, detail="No grades found for this user")
    return betyg


@app.post("/betyg/", response_model=BetygOut)
def create_betyg_view(
    betyg: BetygCreate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Create a new betyg.
    """
    new_betyg = Betyg(
        grade=betyg.grade,
        comments=betyg.comments,
        feedback=betyg.feedback,
        homework_id=betyg.homework_id,
        user_id=betyg.user_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    database.add(new_betyg)
    database.commit()
    database.refresh(new_betyg)
    return new_betyg


@app.put("/betyg/{betyg_id}", response_model=BetygOut)
def update_betyg_view(
    betyg_id: int,
    betyg: BetygUpdate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Update an existing betyg.
    """
    updated_betyg = crud.update_betyg(database, betyg_id, betyg)
    return updated_betyg


@app.delete("/betyg/{betyg_id}", response_model=BetygOut)
def delete_betyg(
    betyg_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Delete a betyg from the database.
    """
    db_betyg = database.query(Betyg).filter(Betyg.id == betyg_id).first()
    if not db_betyg:
        raise HTTPException(status_code=404, detail="Betyg not found")

    database.delete(db_betyg)
    database.commit()
    return db_betyg

@app.get("/meddelanden/user/{user_id}", response_model=List[MeddelandeOut])
def get_meddelanden_for_user(
    user_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    db: Session = Depends(get_db)
):
    """
    Fetch all Meddelanden for a specific user.
    """
    meddelanden = (
        db.query(Meddelande)
        .join(Homework)
        .filter(Homework.user_id == user_id)
        .all()
    )
    if not meddelanden:
        raise HTTPException(status_code=404, detail="No messages found for this user")
    return meddelanden


@app.post("/meddelanden/", response_model=MeddelandeOut)
def create_meddelande_view(
    meddelande: MeddelandeCreate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Create a new meddelande.
    """
    return crud.create_meddelande(database, meddelande)


@app.delete("/meddelanden/{meddelande_id}", response_model=MeddelandeOut)
def delete_meddelande(
    meddelande_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Delete a meddelande from the database.
    """
    db_meddelande = database.query(Meddelande).filter(Meddelande.id == meddelande_id).first()
    if not db_meddelande:
        raise HTTPException(status_code=404, detail="Meddelande not found")

    database.delete(db_meddelande)
    database.commit()
    return db_meddelande


@app.put("/meddelanden/{meddelande_id}/", response_model=MeddelandeOut)
def update_or_mark_as_read(
    meddelande_id: int,
    meddelande: MeddelandeCreate = None,  # Optional payload for full update
    mark_as_read: bool = False,  # Query parameter to mark as read
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Update an existing meddelande or mark it as read.
    """
    db_meddelande = database.query(Meddelande).filter(Meddelande.id == meddelande_id).first()
    if not db_meddelande:
        raise HTTPException(status_code=404, detail="Meddelande not found")

    if mark_as_read:
        # Mark the meddelande as read
        db_meddelande.read_status = "Read"
    elif meddelande:
        # Update fields if payload is provided
        db_meddelande.message = meddelande.message
        db_meddelande.description = meddelande.description
        db_meddelande.read_status = meddelande.read_status
        db_meddelande.homework_id = meddelande.homework_id

    database.commit()
    database.refresh(db_meddelande)
    return db_meddelande
@app.get("/filuppladdningar/", response_model=List[FiluppladdningOut])
def read_filuppladdningar(
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Retrieve all filuppladdningar from the database.
    """
    filuppladdningar = crud.get_all_filuppladdningar(database)
    if not filuppladdningar:
        raise HTTPException(status_code=404, detail="No filuppladdningar found")
    return filuppladdningar


@app.post("/filuppladdningar/", response_model=FiluppladdningOut)
def create_filuppladdning_view(
    filuppladdning: FiluppladdningCreate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Create a new filuppladdning.
    """
    return crud.create_filuppladdning(database, filuppladdning)


@app.delete("/filuppladdningar/{filuppladdning_id}", response_model=FiluppladdningOut)
def delete_filuppladdning(
    filuppladdning_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Delete a filuppladdning from the database.
    """
    db_filuppladdning = database.query(Filuppladdning).filter(Filuppladdning.id == filuppladdning_id).first()
    if not db_filuppladdning:
        raise HTTPException(status_code=404, detail="Filuppladdning not found")

    database.delete(db_filuppladdning)
    database.commit()
    return db_filuppladdning


@app.patch("/filuppladdningar/{filuppladdning_id}", response_model=FiluppladdningOut)
def update_filuppladdning(
    filuppladdning_id: int,
    filuppladdning: FiluppladdningCreate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Update an existing filuppladdning in the database.
    """
    db_filuppladdning = database.query(Filuppladdning).filter(Filuppladdning.id == filuppladdning_id).first()
    if not db_filuppladdning:
        raise HTTPException(status_code=404, detail="Filuppladdning not found")

    # Update fields
    db_filuppladdning.filename = filuppladdning.filename
    db_filuppladdning.filepath = filuppladdning.filepath
    db_filuppladdning.description = filuppladdning.description

    database.commit()
    database.refresh(db_filuppladdning)
    return db_filuppladdning


@app.post("/arskurs/", response_model=ArskursSchema)
def create_arskurs(
    arskurs: ArskursCreate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    db: Session = Depends(get_db)
):
    """
    Create a new Årskurs in the database.
    """
    get_class = db.query(Arskurs).filter(Arskurs.name == arskurs.name).first()
    if get_class:
        raise HTTPException(status_code=400, detail="Class already exists")
    db_arskurs = Arskurs(name=arskurs.name, description=arskurs.description, skola=arskurs.skola, klass=arskurs.klass)
    db.add(db_arskurs)
    db.commit()
    db.refresh(db_arskurs)
    return db_arskurs


@app.get("/arskurs/", response_model=List[ArskursSchema])
def get_all_arskurs(
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Retrieve all Årskurs from the database.
    """
    arskurs_list = database.query(Arskurs).all()
    if not arskurs_list:
        raise HTTPException(status_code=404, detail="No Årskurs found")
    return arskurs_list


@app.patch("/arskurs/{arskurs_id}", response_model=ArskursSchema)
def update_arskurs(
    arskurs_id: int,
    arskurs: ArskursCreate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Update an existing Årskurs in the database.
    """
    db_arskurs = database.query(Arskurs).filter(Arskurs.id == arskurs_id).first()
    if not db_arskurs:
        raise HTTPException(status_code=404, detail="Årskurs not found")

    # Update fields
    db_arskurs.name = arskurs.name
    db_arskurs.description = arskurs.description
    db_arskurs.skola = arskurs.skola
    db_arskurs.klass = arskurs.klass

    database.commit()
    database.refresh(db_arskurs)
    return db_arskurs


@app.delete("/arskurs/{arskurs_id}", response_model=ArskursSchema)
def delete_arskurs(
    arskurs_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Delete an Årskurs from the database.
    """
    db_arskurs = database.query(Arskurs).filter(Arskurs.id == arskurs_id).first()
    if not db_arskurs:
        raise HTTPException(status_code=404, detail="Årskurs not found")

    database.delete(db_arskurs)
    database.commit()
    return db_arskurs


@app.get("/subjects/{subject_id}", response_model=SubjectOut)
def get_subject_by_id(
    subject_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Retrieve a subject by ID from the database.
    """
    subject = database.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


@app.get("/subjects/", response_model=List[SubjectOut])
def get_all_subjects(
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Retrieve all subjects from the database.
    """
    subjects = database.query(Subject).all()
    if not subjects:
        raise HTTPException(status_code=404, detail="No subjects found")
    return subjects


@app.post("/subjects/", response_model=SubjectOut)
def create_subject(
    subject: SubjectCreate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Create a new subject in the database.
    """
    existing_subject = database.query(Subject).filter(Subject.name == subject.name).first()
    if existing_subject:
        raise HTTPException(status_code=400, detail="Subject already exists")

    new_subject = Subject(name=subject.name)
    database.add(new_subject)
    database.commit()
    database.refresh(new_subject)
    return new_subject


@app.delete("/subjects/{subject_id}", response_model=SubjectOut)
def delete_subject(
    subject_id: int,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Delete a subject from the database.
    """
    db_subject = database.query(Subject).filter(Subject.id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    database.delete(db_subject)
    database.commit()
    return db_subject


@app.patch("/subjects/{subject_id}", response_model=SubjectOut)
def update_subject(
    subject_id: int,
    subject: SubjectCreate,
    current_user: User = Depends(get_current_user),  # Validate token and authenticate user
    database: Session = Depends(get_db)
):
    """
    Update an existing subject in the database.
    """
    db_subject = database.query(Subject).filter(Subject.id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    # Update fields
    db_subject.name = subject.name
    database.commit()
    database.refresh(db_subject)
    return db_subject
if __name__ == '__main__':
    uvicorn.run(app)