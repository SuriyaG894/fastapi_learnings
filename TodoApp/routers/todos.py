from http.client import HTTPException
from typing import Annotated

from fastapi import APIRouter,Path,HTTPException
from fastapi.params import Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Todos
from database import engine, SessionLocal
from starlette import status
from .auth import get_current_user

router = APIRouter()


class TodoRequest(BaseModel):
    title:str = Field(min_length=3)
    description:str = Field(min_length=3,max_length=100)
    priority:int = Field(gt=0,lt=5)
    complete:bool

    model_config = {
        "json_schema_extra":{
            "example":{
                "title":"Go to Jocking",
                "description":"To reduce weight",
                "priority":5,
                "complete":False
            }
        }
    }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get("/")
def read_all(db:db_dependency):
    return db.query(Todos).all()

@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
def read_todo(db:db_dependency,todo_id:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail='Todo not found')


@router.post("/todo",status_code=status.HTTP_201_CREATED)
def add_todo(user:user_dependency,db:db_dependency,todo_request:TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not authenticate.")
    new_todo = Todos(**todo_request.model_dump(),owner_id=user.get("id"))
    db.add(new_todo)
    db.commit()
    return "Todo added successfully"

@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db:db_dependency,
                todo_request:TodoRequest,
                todo_id:int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model is None:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete
        # db.add(todo_model)
        db.commit()
    else:
        raise HTTPException(status_code=404,detail="Todo not found")


@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db:db_dependency,todo_id:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model is None:
        db.delete(todo_model)
        db.commit()
    else:
        raise HTTPException(status_code=404,detail="todo not found")

