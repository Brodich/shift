from fastapi import APIRouter, Depends
from repository import UserRepository
from schemas import SUser, SUserAdd
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


router = APIRouter(
    prefix="",
    tags=["Users"],
)


@router.post("/add_user", response_model=SUser)
async def add_user(user: SUserAdd = Depends()) -> SUser:
    new_user = await UserRepository.add_user(user)
    return new_user


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    token = await UserRepository.login(form_data)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/salary")
async def get_salary(
    current_user: Annotated[SUserAdd,
                            Depends(UserRepository.get_current_username)],):
    data_salary = await UserRepository.get_salary(current_user)
    return data_salary
