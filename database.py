from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class Model(DeclarativeBase):
    pass


class UserOrm(Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] 
    password: Mapped[str]
    salary: Mapped[float]
    next_raise_date: Mapped[str]


engine = create_async_engine("sqlite+aiosqlite:///users.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

Base = DeclarativeBase()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
