from fastapi import FastAPI
from database import create_tables, delete_tables
from router import router as users_router


async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    # await delete_tables()
    # print("База очищена")

app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
