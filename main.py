from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# ✅ Create FastAPI app (this MUST exist, otherwise error comes)
app = FastAPI(
    title="Library API",
    description="A RESTful API for Library System",
    version="1.0"
)

# In-memory database
books_db = []

# Book model
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int

# ---------------- CRUD Endpoints ----------------

# Create Book
@app.post("/books/", response_model=Book)
def create_book(book: Book):
    for b in books_db:
        if b.id == book.id:
            raise HTTPException(status_code=400, detail="Book with this ID already exists")
    books_db.append(book)
    return book

# Read All Books
@app.get("/books/", response_model=List[Book])
def get_books():
    return books_db

# Read Book by ID
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Update Book
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            books_db[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# Delete Book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            del books_db[i]
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
