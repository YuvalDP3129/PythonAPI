from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Lists(BaseModel):
    list_title: str
    list_description: Optional[str] = None
    note: Optional[str] = None


class Tasks(BaseModel):
    list_id: int
    task_title: str
    task_description: Optional[str] = None
    due_date: Optional[str] = None

class TasksParams(BaseModel):
    task_title: str
    task_description: Optional[str] = None
    due_date: Optional[str] = None


class TaskStatus(BaseModel):
    PENDING = 'pending'
    DONE = 'done'
    IN_PROGRESS = 'in-progress'

