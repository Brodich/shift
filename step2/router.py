from fastapi import APIRouter, Depends, Request, Body, Header, Query
from repository import UserRepository
from schemas import STask, STaskAdd, STaskId, SUser, SUserAdd, SUserId, SLoginData


router = APIRouter(
    prefix = "/tasks", 
    tags = ["Таски"],
    # prefix = "/login",
    # tags = ["login"],
)

# @router.post("", response_model=STaskId)    
# async def add_task(task: STaskAdd = Depends()) -> STaskId:
#     new_task_id = await UserRepository.add_task(task)
#     return {"id": new_task_id}

# @router.get("", response_model=list[STask])
# async def get_tasks() -> list[STask]:
#     tasks = await UserRepository.get_tasks()
#     return tasks

# If you want send data through body 
# async def add_user(user: SUserAdd = Body(...) ) -> SUser:

# If you want send data through header  
# async def add_user(user: SUserAdd = Depends() ) -> SUser:

@router.post("/add_user", response_model=SUser)
async def add_user(user: SUserAdd = Depends()) -> SUser:
    # data = await request.json()
    new_user = await UserRepository.add_user(user)
    return new_user

@router.get("/add_user", response_model=list[SUser])
async def get_users() -> list[SUser]:
    # print("aboba")
    users = await UserRepository.get_users()
    return users

@router.post("/login")
async def login(login_data: SLoginData = Depends()):
    token = await UserRepository.login(login_data)
    return {"token": token}

@router.get("/salary")
async def get_salary(token: str = Header(...)):
    # print(token)
    data = await UserRepository.get_salary(token)
    return data

