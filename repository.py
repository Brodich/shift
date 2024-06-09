from fastapi import HTTPException
from sqlalchemy import select  
import datetime
import jwt

from database import UserOrm, new_session
from schemas import SUser, SUserAdd, SLoginData
from config import Config


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
    async def login(cls, login_data: SLoginData) -> str:
        login = login_data.login
        password = login_data.password
        async with new_session() as session:
            query = select(UserOrm).where(
                (UserOrm.login == login) 
                & (UserOrm.password == password))

            result = await session.execute(query)
            users_models = result.scalars().all()
            user = [SUser.model_validate(user_model) for user_model in users_models]
            if user == []:
                raise HTTPException(status_code=401, detail="Incorrect login or password")
            payload = {
                "login": login,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=Config.JWT_EXPIRATION_DELTA)
            }
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
        return token


    @classmethod
    async def verify_token(cls, pure_token: str) -> str:
        try:
            payload = jwt.decode(pure_token, Config.SECRET_KEY, algorithms=["HS256"])
            return payload["login"]
        except:
            raise HTTPException(status_code=498, detail="Expired or invalid token") 


    @classmethod
    async def get_salary(cls, token: str) -> dict:
        try:
            pure_token = token.split(sep="Authorization: Bearer ")[1]
        except:
            raise HTTPException(status_code=498, detail="Expired or invalid token") 
        if pure_token:
            login = await cls.verify_token(pure_token)
            if login:
                async with new_session() as session:
                    query = select(UserOrm).where(
                    (UserOrm.login == login))
                    result = await session.execute(query)
                    user_model = result.scalars().first()
                    user = SUser.model_validate(user_model)
                    # print("query", user)
                    return {"login:": user.login, "salary": user.salary, "next_raise_date": user.next_raise_date}
