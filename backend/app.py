from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import update
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from db_setup import get_db, create_databases
import crud
import uvicorn
from schemas import ArskursCreate, Arskurs as ArskursSchema, BetygCreate, BetygOut, BetygUpdate, FiluppladdningCreate, FiluppladdningOut, HomeworkCreate, HomeworkInUpdate, MeddelandeCreate, MeddelandeOut, MembershipUpdate, RecommendedResourceCreate, RecommendedResourceOut, SubjectCreate, SubjectOut, UserInUpdate
from schemas import GetUser, HomeworkBase, HomeworkOut, UserIn, UserOut, MembershipOut
from models import Arskurs, Betyg, Filuppladdning, Homework, Meddelande, RecommendedResource, Role, Subject, User, Membership
from schemas import MembershipCreate
from schemas import UserOut, RoleOut

# Initialize the FastAPI app
app = FastAPI()
app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
create_databases()

@app.get("/users/", response_model=List[UserOut])
def read_users(database: Session = Depends(get_db)):
    """
     Hämtar alla användare från databasen.
    """
    users = database.query(User).all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    return users
@app.get("/users/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int, database: Session = Depends(get_db)):
    """
    Retrieve a user by ID from the database.
    """
    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=UserOut)  # Use UserOut for response model
def add_users(
    user_params: UserIn,  # Accept UserOut for validation (not SQLAlchemy User)
    database: Session = Depends(get_db)
):
    """
    Create a new user in the database.
    """
    # Convert Pydantic model to SQLAlchemy model and add to the database
    new_user = User(**user_params.model_dump())  # Use model_dump instead of dict
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user  # Return SQLAlchemy model, but response model will be UserOut
@app.post("/get_user_by_email_and_password")
def get_user_by_email(user: GetUser, database: Session = Depends(get_db)):
    user = crud.get_user_by_email_and_password(database, user.email, user.password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or incorrect password")
    return user
@app.delete("/users/{user_id}")
def delete_user_view(user_id: int, database: Session = Depends(get_db)):
    """
    Delete a user from the database.
    """
    return crud.delete_user(database, user_id)
@app.patch("/users/{user_id}", response_model=UserOut)
def update_user_by_id(user_id: int, user_params: UserInUpdate, database: Session = Depends(get_db)):
    """
    Update a user by ID in the database.
    """
    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    database.execute(update(User).where(User.id == user_id).values(user_params.model_dump(exclude_none=True)))
    database.commit()
    updated_user = database.query(User).filter(User.id == user_id).first()
    return updated_user

@app.post("/membership/", response_model=MembershipCreate)
def create_membership_endpoint(membership: MembershipCreate, db: Session = Depends(get_db)):
    # Call the crud function to create the membership
    new_membership = crud.create_membership(db, membership)
    
    return new_membership  # Return the created membership object

@app.get("/memberships/", response_model=List[MembershipOut])
def read_memberships(database: Session = Depends(get_db)):
    """
    Retrieve all memberships from the database.
    """
    memberships = crud.get_all_memberships(database)
    if not memberships:
        raise HTTPException(status_code=404, detail="No memberships found")
    return memberships
@app.put("/memberships/{membership_id}", response_model=MembershipOut)
def replace_membership(membership_id: int, membership: MembershipCreate, database: Session = Depends(get_db)):
    """
    Replace an existing membership.
    """
    db_membership = database.query(Membership).filter(Membership.id == membership_id).first()
    if not db_membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    
    # Replace all fields
    db_membership.membership_type = membership.membership_type
    db_membership.start_date = membership.start_date
    db_membership.end_date = membership.end_date
    
    database.commit()
    database.refresh(db_membership)
    return db_membership

@app.delete("/memberships/{membership_id}")
def delete_membership_view(membership_id: int, database: Session = Depends(get_db)):
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
@app.post("/users/{user_id}/roles/{role_id}")
def assign_role_to_user(user_id: int, role_id: int, database: Session = Depends(get_db)):
    """
    Assign a role to a user.
    """
    user = crud.add_role_to_user(database, user_id, role_id)
    return user

# Endpoint to get all roles
@app.get("/roles/", response_model=List[RoleOut])
def get_roles(database: Session = Depends(get_db)):
    """
    Retrieve all roles from the database.
    """
    roles = crud.get_all_roles(database)
    return roles

# Endpoint to get users by role
@app.get("/roles/{role_name}/users", response_model=List[UserOut])
def get_users_by_role(role_name: str, database: Session = Depends(get_db)):
    """
    Retrieve all users with a specific role.
    """
    users = crud.get_users_by_role(database, role_name)
    return users
@app.patch("/roles/{role_id}", response_model=RoleOut)
def update_role(role_id: int, role_name: str, database: Session = Depends(get_db)):
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
def delete_role(role_id: int, database: Session = Depends(get_db)):
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
@app.post("/homework/", response_model=HomeworkOut)
def create_homework_view(homework: HomeworkCreate, database: Session = Depends(get_db)):
    user = database.query(User).filter(User.id == homework.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Ensure correct attributes are used for Homework model
    new_homework = Homework(
        title=homework.title,
        description=homework.description,
        due_date=homework.due_date,
        user_id=homework.user_id,
        subject_id=homework.subject_id  # Ensure this attribute exists in Homework model
    )
    
    database.add(new_homework)
    database.commit()
    database.refresh(new_homework)
    return new_homework

# Get all homeworks
@app.get("/homeworks/", response_model=List[HomeworkOut])
def get_homeworks_view(database: Session = Depends(get_db)):
    homeworks = crud.get_homeworks(database)
    if not homeworks:
        raise HTTPException(status_code=404, detail="No homeworks found")
    return homeworks

# Get homeworks by user ID
@app.get("/homeworks/{user_id}", response_model=List[HomeworkOut])
def get_homework_by_user_view(user_id: int, database: Session = Depends(get_db)):
    homeworks = crud.get_homework_by_user(database, user_id)
    if not homeworks:
        raise HTTPException(status_code=404, detail="No homeworks found for this user")
    return homeworks
@app.patch("/homeworks/{homework_id}", response_model=HomeworkOut)
def update_homework_by_id(homework_id: int, homework: HomeworkInUpdate, database: Session = Depends(get_db)):
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
# Get homeworks by subject ID
@app.get("/homeworks/subject/{subject_id}", response_model=List[HomeworkOut])
def get_homework_by_subject_view(subject_id: int, database: Session = Depends(get_db)):
    homeworks = crud.get_homework_by_subject(database, subject_id)
    if not homeworks:
        raise HTTPException(status_code=404, detail="No homeworks found for this subject")
    
    return homeworks
@app.delete("/homeworks/{homework_id}", response_model=HomeworkOut)
def delete_homework(homework_id: int, database: Session = Depends(get_db)):
    """
    Delete a homework from the database.
    """
    db_homework = (
        database.query(Homework)
        .options(
            joinedload(Homework.user),
            joinedload(Homework.subject),
            joinedload(Homework.betyg),
            joinedload(Homework.meddelande),
            joinedload(Homework.filuppladdning),
            joinedload(Homework.recommended_resource),
        )
        .filter(Homework.id == homework_id)
        .first()
    )
    if not db_homework:
        raise HTTPException(status_code=404, detail="Homework not found")

    database.delete(db_homework)
    database.commit()
    return db_homework
# Create recommended resource
@app.post("/recommended_resources/", response_model=RecommendedResourceOut)
def create_recommended_resource_view(resource: RecommendedResourceCreate, database: Session = Depends(get_db)):
    return crud.create_recommended_resource(database, resource)

@app.get("/recommended_resources/", response_model=List[RecommendedResourceOut])
def read_all_recommended_resources(database: Session = Depends(get_db)):
    """
    Retrieve all recommended resources from the database.
    """
    resources = database.query(RecommendedResource).all()
    if not resources:
        raise HTTPException(status_code=404, detail="No recommended resources found")
    return resources
@app.delete("/recommended_resources/{resource_id}", response_model=RecommendedResourceOut)
def delete_recommended_resource(resource_id: int, database: Session = Depends(get_db)):
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
def update_recommended_resource(resource_id: int, resource: RecommendedResourceCreate, database: Session = Depends(get_db)):
    """
    Update an existing recommended resource in the database.
    """
    db_resource = database.query(RecommendedResource).filter(RecommendedResource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Recommended resource not found")

    # Update fields
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
def read_betyg(database: Session = Depends(get_db)):
    """
    Retrieve all betyg from the database.
    """
    betyg = crud.get_all_betyg(database)
    if not betyg:
        raise HTTPException(status_code=404, detail="No betyg found")
    return betyg
@app.post("/betyg/", response_model=BetygOut)
def create_betyg_view(betyg: BetygCreate, database: Session = Depends(get_db)):
    """
    Create a new betyg.
    """
    new_betyg = Betyg(
        grade=betyg.grade,
        comments=betyg.comments,
        feedback=betyg.feedback,
        homework_id=betyg.homework_id,
    )
    database.add(new_betyg)
    database.commit()
    database.refresh(new_betyg)
    return new_betyg
@app.put("/betyg/{betyg_id}", response_model=BetygOut)
def update_betyg_view(betyg_id: int, betyg: BetygUpdate, database: Session = Depends(get_db)):
    """
    Update an existing betyg.
    """
    updated_betyg = crud.update_betyg(database, betyg_id, betyg)
    return updated_betyg
@app.delete("/betyg/{betyg_id}", response_model=BetygOut)
def delete_betyg(betyg_id: int, database: Session = Depends(get_db)):
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
def get_meddelanden_by_user_view(user_id: int, database: Session = Depends(get_db)):
    """
    Retrieve all meddelanden for a specific user.
    """
    meddelanden = crud.get_meddelanden_by_user(database, user_id)
    if not meddelanden:
        raise HTTPException(status_code=404, detail="No meddelanden found for this user")
    return meddelanden
@app.post("/meddelanden/", response_model=MeddelandeOut)
def create_meddelande_view(meddelande: MeddelandeCreate, database: Session = Depends(get_db)):
    """
    Create a new meddelande.
    """
    return crud.create_meddelande(database, meddelande)
@app.delete("/meddelanden/{meddelande_id}", response_model=MeddelandeOut)
def delete_meddelande(meddelande_id: int, database: Session = Depends(get_db)):
    """
    Delete a meddelande from the database.
    """
    db_meddelande = database.query(Meddelande).filter(Meddelande.id == meddelande_id).first()
    if not db_meddelande:
        raise HTTPException(status_code=404, detail="Meddelande not found")

    database.delete(db_meddelande)
    database.commit()
    return db_meddelande
@app.patch("/meddelanden/{meddelande_id}", response_model=MeddelandeOut)
def update_meddelande(meddelande_id: int, meddelande: MeddelandeCreate, database: Session = Depends(get_db)):
    """
    Update an existing meddelande in the database.
    """
    db_meddelande = database.query(Meddelande).filter(Meddelande.id == meddelande_id).first()
    if not db_meddelande:
        raise HTTPException(status_code=404, detail="Meddelande not found")

    # Update fields
    db_meddelande.message = meddelande.message
    db_meddelande.description = meddelande.description
    db_meddelande.read_status = meddelande.read_status

    database.commit()
    database.refresh(db_meddelande)
    return db_meddelande
@app.get("/filuppladdningar/", response_model=List[FiluppladdningOut])
def read_filuppladdningar(database: Session = Depends(get_db)):
    """
    Retrieve all filuppladdningar from the database.
    """
    filuppladdningar = crud.get_all_filuppladdningar(database)
    if not filuppladdningar:
        raise HTTPException(status_code=404, detail="No filuppladdningar found")
    return filuppladdningar
@app.post("/filuppladdningar/", response_model=FiluppladdningOut)
def create_filuppladdning_view(filuppladdning: FiluppladdningCreate, database: Session = Depends(get_db)):
    """
    Create a new filuppladdning.
    """
    return crud.create_filuppladdning(database, filuppladdning)
@app.delete("/filuppladdningar/{filuppladdning_id}", response_model=FiluppladdningOut)
def delete_filuppladdning(filuppladdning_id: int, database: Session = Depends(get_db)):
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
def update_filuppladdning(filuppladdning_id: int, filuppladdning: FiluppladdningCreate, database: Session = Depends(get_db)):
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
def create_arskurs(arskurs: ArskursCreate, db: Session = Depends(get_db)):
    get_class = db.query(Arskurs).filter(Arskurs.name == arskurs.name).first()
    if get_class:
        raise HTTPException(status_code=400, detail="Class already exists")
    db_arskurs = Arskurs(name=arskurs.name, description=arskurs.description, skola=arskurs.skola, klass=arskurs.klass)
    db.add(db_arskurs)
    db.commit()
    db.refresh(db_arskurs)
    return db_arskurs
@app.get("/arskurs/", response_model=List[ArskursSchema])
def get_all_arskurs(database: Session = Depends(get_db)):
    """
    Retrieve all Årskurs from the database.
    """
    arskurs_list = database.query(Arskurs).all()
    if not arskurs_list:
        raise HTTPException(status_code=404, detail="No Årskurs found")
    return arskurs_list
@app.patch("/arskurs/{arskurs_id}", response_model=ArskursSchema)
def update_arskurs(arskurs_id: int, arskurs: ArskursCreate, database: Session = Depends(get_db)):
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
def delete_arskurs(arskurs_id: int, database: Session = Depends(get_db)):
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
def get_subject_by_id(subject_id: int, database: Session = Depends(get_db)):
    """
    Retrieve a subject by ID from the database.
    """
    subject = database.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject
@app.get("/subjects/", response_model=List[SubjectOut])
def get_all_subjects(database: Session = Depends(get_db)):
    """
    Retrieve all subjects from the database.
    """
    subjects = database.query(Subject).all()
    if not subjects:
        raise HTTPException(status_code=404, detail="No subjects found")
    return subjects
@app.post("/subjects/", response_model=SubjectOut)
def create_subject(subject: SubjectCreate, database: Session = Depends(get_db)):
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
def delete_subject(subject_id: int, database: Session = Depends(get_db)):
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
def update_subject(subject_id: int, subject: SubjectCreate, database: Session = Depends(get_db)):
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