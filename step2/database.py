
# employee = {
#     {"login": "Alex", "password": "dontgooglegitler34", "salary": 60000, "date_raise": "20-03-2024"},
#     {"login": "Bob", "password": "mommysony", "salary": 100, "date_raise": "22-01-2028"}
# }

from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///tasks.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)