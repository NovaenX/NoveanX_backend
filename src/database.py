from sqlmodel import Session, create_engine, SQLModel
from . import settings as s
from contextlib import asynccontextmanager
from fastapi import FastAPI

DATABASE_URL = f"sqlite:///{s.db_path}"
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    yield
    print("Shutting down...")
