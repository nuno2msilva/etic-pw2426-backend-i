import os
from sqlmodel import Session
from session_12.models import Task

def get_engine()->Engine

def get_session() -> Session:
    DB_USER = os.getenv("DB_USER", None)
    DB_PASS = os.getenv("DB_PASS", None)
    DB_HOST = os.getenv("DB_HOST", None)
    DB_PORT = os.getenv("DB_PORT", None)
    DB_NAME = os.getenv("DB_NAME", None) 
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    return Session(engine)


def create_task(task: Task):
        assert task
        with get_session() as session:
        