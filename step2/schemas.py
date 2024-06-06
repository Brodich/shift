from pydantic import BaseModel, ConfigDict

class STaskAdd(BaseModel):
    name: str
    description: str | None = None

class STask(STaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)

class STaskId(BaseModel):
    id: int



class SUserAdd(BaseModel):
    login: str
    password: str
    salary: int
    next_raise_date: str

class SUser(SUserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)

class SUserId(BaseModel):
    id: int
# @app.post("/")
# async def add_task(task: STaskAdd):
#     return {"data": task}

    