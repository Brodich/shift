from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from contextlib import asynccontextmanager
from database import create_tables, delete_tables 

# from schemas import *
from router import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    # await delete_tables()
    # print("База очищена")

app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)


''' 
curl -v -X POST 'http://127.0.0.1:8000/tasks/add_user' \
-H 'Content-Type: application/json' \
-d '{"login": "Gats", "password": "ilovegriffit", "salary": 10, "next_raise_date": "10-10-2010"}'
'''

@app.get("/")
async def home():
    return {"data": "Hello World"}

@app.get("/")
async def bbbb():
    return {"data": "gav"}

# curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"username": "john_doe", "password": "password123"}'

