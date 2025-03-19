from typing import Annotated
from fastapi import FastAPI, Depends, Form
from fastapi.responses import JSONResponse
from session_12.models import Task
from starlette import status
from session_12.services import start_engine, Session
import logging
from fastapi.exceptions import HTTPException

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

api = FastAPI(
    title="TODO Etic_Algarve API"
)

start_engine()

@api.get("/task", response_model=Task)
def list_task():
    pass


@api.post("/task")
def create_task(data: Annotated[Task,Form()]):
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    database.create(task=Task(**data))
    new_task = Task(**data)

    return JSONResponse({"status": "created"}, status_code=status.HTTP_201_CREATED)

@api.put("/task")
def edit_task():
    pass

@api.patch("/task")
def close_task():
    pass

@api.delete("/task")
def delete_task():
    pass

 