from fastapi import APIRouter, Depends
from repository import TaskRepository
from schemas import STask, STaskAdd, STaskId

# class STaskId(BaseModel):
#     id: int

router = APIRouter(
    prefix = "/tasks",
    tags = ["Таски"],
)

@router.post("", response_model=STaskId)    
async def add_task(task: STaskAdd) -> STaskId:
    new_task_id = await TaskRepository.add_task(task)
    return {"id": new_task_id}

@router.get("", response_model=list[STask])
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.get_tasks()
    return tasks

