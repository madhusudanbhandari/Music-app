from fastapi import HTTPException
import uuid
from database import db
from models.user import User
from pydantic_schemas.user_create import UserCreate
import bcrypt
from fastapi import APIRouter

router=APIRouter()


@router.post('/signup')
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

