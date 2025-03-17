from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, index=True)
    lastName = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    phone_number = Column(String, index=True)