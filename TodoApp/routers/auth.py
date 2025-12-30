from datetime import timedelta, datetime, UTC
from time import timezone
from typing import Annotated
#>pip install "python-jose[cryptography]"
from jose import jwt
from fastapi import APIRouter, Depends,HTTPException
from pydantic import BaseModel
from models import Users
from database import engine, SessionLocal
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.util import deprecated
from starlette.status import HTTP_201_CREATED
from fastapi.security import OAuth2PasswordRequestForm

#openssl rand -hex 32
SECRET_KEY = "dummykeyfornowwearegonnauseit"
Algorithm="HS256"


router = APIRouter()
# for using bcrypt password we need to install passlib and bcrypt=4.0.1
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str

class Token(BaseModel):
    access_token:str
    token_type:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]

def token_generator(username:str,user_id:int,expires_delta:timedelta):
    encode = {
        "sub":username,
        "id":user_id
    }
    expires = str(datetime.now(UTC) + expires_delta)
    encode.update({"exp":expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=Algorithm)

def authenticate_user(username:str,password:str,db):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


@router.post("/token")
def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user = authenticate_user(form_data.username,form_data.password,db)
    token = ""
    if not isinstance(user,bool):
        token = token_generator(user.username,user.id,timedelta(minutes=20))
        return {"access_token":token,"token_type":'Bearer'}

    else:
        return "Authentication Failed"


@router.post("/auth/",status_code=HTTP_201_CREATED)
def create_user(db:db_dependency,create_user_request:CreateUserRequest):

    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        role="Admin"
    )
    if not create_user_model is None:
        db.add(create_user_model)
        db.commit()
    else:
        raise HTTPException(status_code=400,detail="Invalid input")
