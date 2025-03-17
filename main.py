from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models 
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine) #will create all tables and columns in postgres

class User(BaseModel):
    firstName: str
    lastName: str
    email: str
    

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated(Session, Depends(getDb))

#creating users
@app.post("/users/")
async def create_User(user: User, db: db_dependency):
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
async def get_user(user_id: int, db: db_dependency):
    result = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="user is not found")
    return result

#getting users with the email
@app.get("/users/{user_email}")
async def get_user_by_email(user_email: str, db: db_dependency):
    result = db.query(models.Users).filter(models.Users.email == user_email.email).first()
    if not result:
        raise HTTPException(status_code=404, detail="user is not found")
    return result

    

@app.get("/")
async def root():
    return {"message": "Hello World"}