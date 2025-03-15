from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone_number = Column(Integer, index=True)