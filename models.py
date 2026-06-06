from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Item(Base):
    __tablename__ = "employeedetails"

    employeeid = Column(Integer, primary_key=True, index=True, nullable=False)
    employeename = Column(String(100), nullable=False)
    emailid = Column(String(100), nullable=True)

class User(Base):
    __tablename__= "users"
    id= Column(Integer,primary_key=True,index=True)
    username=Column(String(100),nullable=False)
    email=Column(String(100),unique=True,nullable=False)
    password=Column(String(256),nullable=False)
    is_active=Column(Boolean,default=True)