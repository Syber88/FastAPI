from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated, Optional
import models 
from database import engine, SessionLocal
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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated(Session, Depends(getDb))

#creating users
@app.post("/users/")
async def create_User(user: User, db: Session = Depends(getDb)):
    current_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if current_user:
        raise HTTPException(status_code=400, detail="user already exitsts in the database")
    
    db_user = models.Users(name=user.name, lastName=user.lastName, email=user.email, phone_number=user.phone_number)
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
    result = db.query(models.Users).filter(models.Users.email == user_email.email).first()
    if not result:
        raise HTTPException(status_code=404, detail="user is not found")
    return result

#updating user 
@app.post("/user/{user_id}")
async def update_existing_user(user_id: int, user: updateUser, db: Session = Depends(getDb)):
    db_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="user is not found")
    
    if user.firstName:
        db_user.firstName = user.firstName
    if user.lastName:
        db_user.name = user.lastName
    if user.email:
        db_user.name = user.email
    if user.phone_number:
        db_user.name = user.phone_number
        
    db.commit()
    db.refresh(db_user)
    
    return {"user updated successfully, user ": db_user}
    
    
    


    

@app.get("/")
async def root():
    return {"message": "Hello World"}