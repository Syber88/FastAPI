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

@app.post("/users/")
async def create_User(user: User, db: db_dependency):
    db_user = models.Users(name=user.name, lastName=user.lastName, email=user.email, phone_number=user.phone_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"user created successfully, user: ": db_user}
    

@app.get("/")
async def root():
    return {"message": "Hello World"}