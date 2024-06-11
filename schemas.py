from pydantic import BaseModel, ConfigDict


class SUserAdd(BaseModel):
    username: str
    password: str
    salary: int
    next_raise_date: str


class SUser(SUserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SLoginData(BaseModel):
    username: str
    password: str
