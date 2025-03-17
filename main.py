from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Annotated
import models 
from database import engine, SessionLocal
from sqlalchemy.orm import session

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


@app.get("/")
async def root():
    return {"message": "Hello World"}