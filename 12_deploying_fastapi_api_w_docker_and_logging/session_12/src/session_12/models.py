from datetime import datetime
import os
from typing import Optional
from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    due_date: datetime
    is_done: bool = False

