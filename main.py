from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables, delete_tables 

from router import router as tasks_router

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
