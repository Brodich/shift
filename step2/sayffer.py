from fastapi import FastAPI
from fastapi import Depends

from pydantic import BaseModel
from database import *
from valid import *

app = FastAPI()


class STaskAdd(BaseModel):
    name: str
    description: str | None = None

class STask(STaskAdd):
    id: int
    
    # model_config = ConfigDict(from_attributes=True)
    

@app.post("/")
async def add_task(task: STaskAdd = Depends()):
    return {"data": task}


employee = {
    "Alex": {
        "password": "dontgooglegitler34",
        "salary": 60000,
        "date_raise": "20-03-2024"
    }
    # {"login": "Alex", "password": "dontgooglegitler34", "salary": 60000, "date_raise": "20-03-2024"}
}

# curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"username": "john_doe", "password": "password123"}'


# @app.get("/")
# async def home():
#     return {"data": "Hello World"}
    
@app.route("/login", methods=['POST'])
async def login():
    data = request.get_json()
    login = data.get("login")
    password = data.get("password")
    return jsonify(login + password)
    


