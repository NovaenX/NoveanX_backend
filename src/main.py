from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel,  Session, select
from contextlib import asynccontextmanager
from models import FoodLog
from sqlalchemy.exc import IntegrityError
from database import engine, get_session
from schemas import FoodLogCreate, FoodLogRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)


@app.post("/food/", response_model=FoodLogRead)
def add_food(food: FoodLogCreate, session: Session = Depends(get_session)):
    db_food = FoodLog(**food.model_dump())
    try:
        session.add(db_food)
        session.commit()
        session.refresh(db_food)
        return db_food
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Food already exists")


@app.get("/food/", response_model=List[FoodLogRead])
def get_food_logs(session: Session = Depends(get_session)):
    return session.exec(select(FoodLog)).all()


@app.get("/food/search/{name}", response_model=List[FoodLogRead])
def search_food(name: str, session: Session = Depends(get_session)):
    results = session.exec(
        select(FoodLog).where(FoodLog.food_name.ilike(f"%{name}%"))
    ).all()
    if not results:
        raise HTTPException(status_code=404, detail="No foods found")
    return results
