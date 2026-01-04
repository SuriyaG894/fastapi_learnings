import os

from fastapi import FastAPI
import models
from database import engine
from routers import auth,todos
from dotenv import load_dotenv

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)


# Just learning purpose of dotenv
load_dotenv()
val = os.getenv("api_key")
print(val)
