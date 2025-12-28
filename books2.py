
from typing import Optional

from fastapi import FastAPI,Path,Query
from pydantic import BaseModel,Field

app = FastAPI()

class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int
    published_date:int

    def __init__(self,id,title,author,description,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

# Creating BookRequest Class which extends BaseModel of Pydantic Framework
# Adding Field Validation and making id field to be optional
class BookRequest(BaseModel):
    id:Optional[int] = None
    title:str = Field(min_length=3)
    author:str = Field(min_length=1)
    description:str = Field(min_length=3,max_length=100)
    rating:int = Field(gt=0,lt=6)
    published_date:int = Field(gt=999,lt=2031)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title":"Basics of Pydantic",
                "author":"Suriya",
                "description":"Pydantic stuff",
                "rating":5,
                "published_date":2024
            }
        }
    }



BOOKS = [
    Book(1,"C Programming","Balasubramani","Fundamendals of C Programming",5,2011),
    Book(2,"Data Communication","John wick","Networking Stuff",4,2020),
    Book(3,"Design and analysis of Algorithm","Iyyapa Perumal","Algorthim Stuff",4,2008),
    Book(4,"HP1","Author One","Book Description",3,2001),
    Book(5,"HP2","Author Two","Book Description",3,2003),
    Book(6,"HP3","Author Three","Book Description",1,1997)
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

@app.get("/books/{book_id}")
def fetch_book_by_id(book_id:int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            return BOOKS[i]
    return {"message":"Book not found"}


@app.get("/books/")
def fetch_book_by_ratings(rating:int = Query(gt=0,lt=6)):
    books_by_rating =[]
    for i in range(len(BOOKS)):
        if BOOKS[i].rating == rating:
            books_by_rating.append(BOOKS[i])
    return books_by_rating if len(books_by_rating)>0 else {"message":"Books not found"}


@app.put("/books/")
def update_book(upt_book:BookRequest):
    updated_book = Book(**upt_book.model_dump())
    flag = 0
    for i in range(len(BOOKS)):
        if BOOKS[i].id == updated_book.id:
            BOOKS[i] = updated_book
            flag =1
            break
    if flag == 0:
        updated_book = update_id(updated_book)
        BOOKS.append(updated_book)
    return {"message":"Book updated successfully"}

@app.delete("/books/{book_id}")
def delete_book_by_id(book_id:int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return {"message":"Book deleted successfully"}
    return {"message":"Book not found"}

# Assignment to fetch book using published_date
@app.get("/books/publish/")
def fetch_book_by_published_date(published_date:int):
    books_by_published_date = []
    print(published_date)
    for i in range(len(BOOKS)):
        if BOOKS[i].published_date == published_date:
            books_by_published_date.append(BOOKS[i])
    return books_by_published_date