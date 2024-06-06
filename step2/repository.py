from sqlalchemy import select, text
from database import TaskOrm, UserOrm, new_session
from schemas import STaskAdd, STask, SUser, SUserAdd
# from sayffer import STaskAdd, STask

class TaskRepository:
    @classmethod
    async def add_task(cls, task: STaskAdd) -> int:
        async with new_session() as session:
            # data = task.model_dump()
            data = task.dict()
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
    async def add_user(cls, user: SUserAdd) -> int:
        async with new_session() as session:
            data = user.dict()
            new_user = UserOrm(**data)
            session.add(new_user)
            await session.flush()
            await session.commit()
            return new_user.id


    @classmethod
    async def get_users(cls) -> list[SUser]:
        async with new_session() as session:
            # query = select(UserOrm)

            query = text("select * from users")
            result = await session.execute(query) # тут падает 
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
    async def login(cls, data: dict):
        login = data["login"]
        password = data["password"]

        # data = request.get_json()

        print(data)
        return data["login"]


