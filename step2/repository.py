from fastapi import HTTPException
import datetime

from sqlalchemy import select, text
from database import TaskOrm, UserOrm, new_session
from schemas import STaskAdd, STask, SUser, SUserAdd, SLoginData
from config import Config

from sqlalchemy.ext.asyncio import AsyncSession
import jwt
# from sayffer import STaskAdd, STask

class TaskRepository:
    @classmethod
    async def add_task(cls, task: STaskAdd) -> int:
        async with new_session() as session:
            # data = task.model_dump()
            data = task.model_dump()
            new_task = TaskOrm(**data)
            session.add(new_task)
            await session.flush()
            await session.commit()
            return new_task.id

    @classmethod
    async def get_tasks(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            tasks = [STask.model_validate(task_model) for task_model in task_models]
            return tasks

    @classmethod
    async def add_user(cls, user: SUserAdd) -> SUser:
        async with new_session() as session:
            data = user.model_dump(mode='json')
            new_user = UserOrm(**data)
            session.add(new_user)
            await session.flush()
            await session.commit()
            # print(session)
            return new_user


    @classmethod
    async def get_users(cls) -> list[SUser]:
        async with new_session() as session:
            query = select(UserOrm)

            # query = text("select * from users")
            result = await session.execute(query)
            users_models = result.scalars().all()
            users = [SUser.model_validate(user_model) for user_model in users_models]
            # print("aaaaaaaaa")

            # data = user.dict()
            # new_user = UserOrm(**data)
            # session.add(new_user)
            # await session.flush()
            # await session.commit()
            return users

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
            # print(user)
            if user == []:
                raise HTTPException(status_code=401, detail="Incorrect login or password")
            payload = {
                "login": login,
                "expires": (datetime.datetime.utcnow() + datetime.timedelta(minutes=Config.JWT_EXPIRATION_DELTA)).isoformat()
            }
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
        return token


