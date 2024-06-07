from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict

from database import *
from schemas import *
from router import router as tasks_router

from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables, delete_tables 

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

# class STaskAdd(BaseModel):
#     name: str
#     description: str | None = None

# class STask(STaskAdd):
#     id: int
#     model_config = ConfigDict(from_attributes=True)
    

# @app.post("/")
# async def add_task(task: STaskAdd = Depends()):
#     return {"data": task}

@app.get("/")
async def home():
    return {"data": "Hello World"}

@app.get("/")
async def bbbb():
    return {"data": "gav"}

# employee = {
#     "Alex": {
#         "password": "dontgooglegitler34",
#         "salary": 60000,
#         "date_raise": "20-03-2024"
#     }
#     # {"login": "Alex", "password": "dontgooglegitler34", "salary": 60000, "date_raise": "20-03-2024"}
# }

# curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"username": "john_doe", "password": "password123"}'


    
# @app.route("/login", methods=['GET'])
# async def login():
#     return {"data": "gav"}
    # data = request.get_json()
    # login = data.get("login")
    # password = data.get("password")
    # return jsonify(login + password)
    


