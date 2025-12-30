from typing import Annotated

from fastapi import APIRouter, Depends,HTTPException
from pydantic import BaseModel
from models import Users
from database import engine, SessionLocal
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.util import deprecated
from starlette.status import HTTP_201_CREATED

router = APIRouter()
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]

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
