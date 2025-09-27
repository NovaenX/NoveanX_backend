from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from ..models import FoodLog
from ..database import get_session
from ..crud.food import db_add_food, db_get_food_logs, db_search_food
from fastapi import HTTPException

router = APIRouter(prefix="/food", tags=["Food"])


@router.post("/", response_model=FoodLog)
def add_food(food: FoodLog, session: Session = Depends(get_session)):
    result = db_add_food(session, food)
    if result is None:
        raise HTTPException(status_code=400, detail="Food already exists")

    return result


@router.get("/", response_model=List[FoodLog])
def get_food_logs(session: Session = Depends(get_session)):
    return db_get_food_logs(session)


@router.get("/search/{name}", response_model=FoodLog)
def search_food(name: str, session: Session = Depends(get_session)):
    result = db_search_food(session, name)
    if result is None:
        raise HTTPException(status_code=404, detail="Food not found")

    return result
