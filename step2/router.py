from fastapi import APIRouter, Depends, Request, Body, Query
from repository import TaskRepository
from schemas import STask, STaskAdd, STaskId, SUser, SUserAdd, SUserId, SLoginData
from typing import Optional

# class STaskId(BaseModel):
#     id: int

router = APIRouter(
    prefix = "/tasks", 
    tags = ["Таски"],
    # prefix = "/login",
    # tags = ["login"],
)

@router.post("", response_model=STaskId)    
async def add_task(task: STaskAdd = Depends()) -> STaskId:
    new_task_id = await TaskRepository.add_task(task)
    return {"id": new_task_id}

@router.get("", response_model=list[STask])
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.get_tasks()
    return tasks

# If you want send data through body 
# async def add_user(user: SUserAdd = Body(...) ) -> SUser:

# If you want send data through header  
# async def add_user(user: SUserAdd = Depends() ) -> SUser:

@router.post("/add_user", response_model=SUser)
async def add_user(user: SUserAdd = Depends()) -> SUser:
    # data = await request.json()
    new_user = await TaskRepository.add_user(user)
    return new_user

@router.get("/add_user", response_model=list[SUser])
async def get_users() -> list[SUser]:
    # print("aboba")
    users = await TaskRepository.get_users()
    return users

@router.post("/login")
async def login(login_data: SLoginData = Depends()):
    
    # data = await request.json()
    token = await TaskRepository.login(login_data)
    return {"token": token}

# @router.get("/salary")

