from fastapi import Depends, HTTPException
import uuid
from models.user import User
from database import get_db
from pydantic_schemas.user_create import UserCreate
from pydantic_schemas.user_login import  UserLogin
import bcrypt
from fastapi import APIRouter
from sqlalchemy.orm import Session

router=APIRouter()


@router.post('/signup',status_code=201)
def signup_user(user: UserCreate,db: Session=Depends(get_db)):
    #extract the data thats comming from req
    print(user.name)
    print(user.email)
    print(user.password)
    #check if the user already exist in db
    user_db=db.query(User).filter(User.email==user.email).first()

    if user_db:
        raise HTTPException(400,'User with the same email already exist ')
      
    
    hashed_pw=bcrypt.hashpw(user.password.encode('utf-8'),bcrypt.gensalt()) 
    user_db=User(id=str(uuid.uuid4()),name=user.name,email=user.email,password=hashed_pw)

    #add the user to db
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db

@router.post('/login')
def login_user(user: UserLogin,db:Session=Depends(get_db)):
    #check if a user with same email exist already
    user_db=db.query(User).filter(User.email==user.email).first()
    
    if not user_db:
        raise HTTPException(400,'User with this email does not exist!')
    
    #password matching or not
    is_match=bcrypt.checkpw(user.password.encode(),user_db.password)
    
    if not is_match:
        raise HTTPException(400,'Password not matching')
    
    return user_db