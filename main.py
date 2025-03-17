from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated, Optional, List
import models 
from database import engine, sessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine) #will create all tables and columns in postgres

class User(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone_number: str
    
    
class updateUser(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    
    
def getDb():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# db_dependency = Annotated(Session, Depends(getDb))

#creating users
@app.post("/users/")
async def create_User(user: User, db: Session = Depends(getDb)):
    current_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if current_user:
        raise HTTPException(status_code=400, detail="user already exitsts in the database")
    
    db_user = models.Users(name=user.firstName, lastName=user.lastName, email=user.email, phone_number=user.phone_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"user created successfully, user: ": db_user}

#getting users with the id 
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(getDb)):
    result = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="user is not found")
    return result

#getting users with the email
@app.get("/users/{user_email}")
async def get_user_by_email(user_email: str, db: Session = Depends(getDb)):
    result = db.query(models.Users).filter(models.Users.email == user_email).first()
    if not result:
        raise HTTPException(status_code=404, detail="user is not found")
    return result

#updating user with user id
@app.post("/user/{user_id}")
async def update_existing_user(user_id: int, user: updateUser, db: Session = Depends(getDb)):
    db_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="user is not found")
    
    if user.firstName:
        db_user.firstName = user.firstName
    if user.lastName:
        db_user.lastName = user.lastName
    if user.email:
        db_user.email = user.email
    if user.phone_number:
        db_user.phone_number = user.phone_number
        
    db.commit()
    db.refresh(db_user)
    
    return {"user updated successfully, user ": db_user}

#updating user with email
@app.post("/user/{user_email}")
async def update_existing_user(user_email: str, user: updateUser, db: Session = Depends(getDb)):
    db_user = db.query(models.Users).filter(models.Users.email == user_email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="user is not found")
    
    if user.firstName:
        db_user.firstName = user.firstName
    if user.lastName:
        db_user.lastName = user.lastName
    if user.email:
        db_user.email = user.email
    if user.phone_number:
        db_user.phone_number = user.phone_number
        
    db.commit()
    db.refresh(db_user)
    
    return {"user updated successfully, user ": db_user}

#deleting user with email
@app.delete("/users/{user_email}")
async def delete_user(user_email: str, user: User, db: Session = Depends(getDb)):
    db_user = db.query(models.Users).filter(models.Users.email == user_email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="user is not found")
    
    db.delete(db_user)
    db.commit()
    return {"user with email "}

#deleting user with email
@app.delete("/users/{user_id}")
async def delete_user(user_id: str, user: User, db: Session = Depends(getDb)):
    db_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="user is not found")
    
    db.delete(db_user)
    db.commit()
    
#get all users 
@app.get("/users/", response_model = List[User])
async def get_all_users(db: Session = Depends(getDb)):
    users = db.query(models.Users).all()
    return users
    
@app.get("/")
async def root():
    return {"message": "Hello World"}