from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import LargeBinary, TEXT,VARCHAR, Column, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid
import bcrypt

app=FastAPI()

DATABASE_URL="postgresql://postgres:Password%40123@localhost:5432/Music-app"

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

db=SessionLocal()


class UserCreate(BaseModel):
    name:str
    email:str
    password:str 

Base=declarative_base()

class User(Base):
    __tablename__='users'

    id=Column (TEXT,primary_key=True)
    name=Column(VARCHAR(100))
    email=Column(VARCHAR(100))
    password=Column(LargeBinary)




@app.post('/signup')
def signup_user(user: UserCreate):
    #extract the data thats comming from req
    print(user.name)
    print(user.email)
    print(user.password)
    #check if the user already exist in db
    user_db=db.query(User).filter(User.email==user.email).first()

    if user_db:
        raise HTTPException(400,'User with the same email already exist ')
      
    
    hashed_pw=bcrypt.hashpw(user.password.encode(),bcrypt.gensalt()) 
    user_db=User(id=str(uuid.uuid4()),name=user.name,email=user.email,password=hashed_pw)

    #add the user to db
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db


Base.metadata.create_all(engine)