from fastapi import APIRouter, Depends, Request, Body, Header, Query
from repository import UserRepository
from schemas import STask, STaskAdd, STaskId, SUser, SUserAdd, SUserId, SLoginData


router = APIRouter(
    prefix = "", 
    tags = ["Users"],
)

'''
If you want send data through body 
async def add_user(user: SUserAdd = Body(...)) -> SUser:

If you want send data through header  
async def add_user(user: SUserAdd = Depends()) -> SUser:
'''
@router.post("/add_user", response_model=SUser)
async def add_user(user: SUserAdd = Depends()) -> SUser:
    new_user = await UserRepository.add_user(user)
    return new_user

@router.get("/add_user", response_model=list[SUser])
async def get_users() -> list[SUser]:
    users = await UserRepository.get_users()
    return users

@router.post("/login")
async def login(login_data: SLoginData = Depends()) -> dict:
    token = await UserRepository.login(login_data)
    return {"token": token}

@router.get("/salary")
async def get_salary(token: str = Header(...)) -> dict:
    # print(token)
    data_salary = await UserRepository.get_salary(token)
    return data_salary
