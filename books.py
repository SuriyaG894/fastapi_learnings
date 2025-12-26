from fastapi import Body, FastAPI

app = FastAPI()

books = [
    {"Author":"One","Title":"Title One","category":"Science"},
    {"Author":"Two","Title":"Title Two","category":"Science"},
    {"Author":"Three","Title":"Title Three","category":"Science"},
    {"Author":"Four","Title":"Title Four","category":"Science"}
]

@app.get("/books")
def read_all_books():
    return books

@app.get("/books/{book_title}")
def read_books_by_name(book_title:str):
    for book in books:
        if book['Title'].casefold() == book_title.casefold():
            return book
    return {"response":"Books not found with the specified title"}

@app.get("/books/{author_name}/")
def read_books_by_author_and_category(author_name:str,category:str):
    for book in books:
        if book.get('Author').casefold() == author_name.casefold() and \
            book.get('category').casefold() == category.casefold():
            return book
    return {"response":"Book not found"}


@app.post("/books")
def add_new_books(new_books=Body()):
    books.append(new_books)


@app.put("/books")
def update_books(updated_books=Body()):
    for index,book in enumerate(books):
        if book.get("Title").casefold() == updated_books.get('Title').casefold():
            books[index] = updated_books
    # print("Updated Books : "+updated_books)
    # for index,book in enumerate(books):
    #     for upt_book in updated_books:
    #         if book.get('Title').casefold() == upt_book.get('Title'):
    #             books[index] = upt_book


@app.delete("/books/{book_title}")
def delete_book(book_title: str):
    i=0
    for index, book in enumerate(books):
        if book["Title"].casefold() == book_title.casefold():
            i=index
            break
    books.pop(i)
    return {"message": "Book deleted successfully"}


@app.delete("/books/all")
def delete_all_books():
    books.clear()
    return {"message":"All books deleted"}

