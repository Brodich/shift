from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select  
from typing import Annotated
import datetime
import jwt

from database import UserOrm, new_session
from schemas import SUser, SUserAdd, SLoginData
from config import Config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class UserRepository:
    @classmethod
    async def add_user(cls, user: SUserAdd) -> SUser:
        async with new_session() as session:
            data = user.model_dump(mode='json')
            new_user = UserOrm(**data)
            session.add(new_user)
            await session.flush()
            await session.commit()
            return new_user


    @classmethod
    async def login(cls, login_data: OAuth2PasswordRequestForm) -> str:
        username = login_data.username
        password = login_data.password
        async with new_session() as session:
            query = select(UserOrm).where(
                (UserOrm.username == username) 
                & (UserOrm.password == password))

            result = await session.execute(query)
            users_model = result.scalars().first()
            user = SUser.model_validate(users_model)
            if user == []:
                raise HTTPException(status_code=401, detail="Incorrect username or password")
            payload = {
                "username": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=Config.JWT_EXPIRATION_DELTA)
            }
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
        return token


    @classmethod
    async def verify_token(cls, token: str) -> str:
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            return payload["username"]
        except:
            raise HTTPException(status_code=498, detail="Expired or invalid token") 


    @classmethod
    async def get_current_username(cls, token: Annotated[str, Depends(oauth2_scheme)]):
        username = await cls.verify_token(token)
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.username == username)
            result = await session.execute(query)
            user_model = result.scalars().first()
            if not user_model:
                raise HTTPException(status_code=401, detail="Invalid authentication")
            user = SUser.model_validate(user_model)
            return user.username


    @classmethod
    async def get_salary(cls, username: str) -> dict:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.username == username)
            result = await session.execute(query)
            user_model = result.scalars().first()
            if not user_model:
                raise HTTPException(status_code=404, detail="User not found")
            user = SUser.model_validate(user_model)
            return {"username": user.username, "salary": user.salary, "next_raise_date": user.next_raise_date}
