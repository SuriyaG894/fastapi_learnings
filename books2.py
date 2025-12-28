
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel,Field

app = FastAPI()

class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int

    def __init__(self,id,title,author,description,rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

# Creating BookRequest Class which extends BaseModel of Pydantic Framework
# Adding Field Validation and making id field to be optional
class BookRequest(BaseModel):
    id:Optional[int] = None
    title:str = Field(min_length=3)
    author:str = Field(min_length=1)
    description:str = Field(min_length=3,max_length=100)
    rating:int = Field(gt=0,lt=6)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title":"Basics of Pydantic",
                "author":"Suriya",
                "description":"Pydantic stuff",
                "rating":5
            }
        }
    }



BOOKS = [
    Book(1,"C Programming","Balasubramani","Fundamendals of C Programming",5),
    Book(2,"Data Communication","John wick","Networking Stuff",4),
    Book(3,"Design and analysis of Algorithm","Iyyapa Perumal","Algorthim Stuff",4),
    Book(4,"HP1","Author One","Book Description",3),
    Book(5,"HP2","Author Two","Book Description",3),
    Book(6,"HP3","Author Three","Book Description",1)
]

@app.get("/books")
def read_all_books():
    return BOOKS

@app.post("/books")
def add_new_book(book_request:BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(update_id(new_book))

def update_id(book:Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id +1
    return book


