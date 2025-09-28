from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from ..schemas import FoodLogCreate, FoodLogRead
from ..database import get_session
from ..crud.food import *
from fastapi import HTTPException

router = APIRouter(prefix="/food", tags=["Food"])


@router.post("/", response_model=FoodLogRead)
def add_food(food: FoodLogCreate, session: Session = Depends(get_session)):
    result = db_add_food(session, food)
    if result is None:
        raise HTTPException(status_code=400, detail="Food already exists")

    return result


@router.get("/", response_model=List[FoodLogRead])
def get_food_logs(session: Session = Depends(get_session)):
    return db_get_food_logs(session)


@router.get("/search/{name}", response_model=FoodLogRead)
def search_food(name: str, session: Session = Depends(get_session)):
    result = db_search_food(session, name)
    if result is None:
        raise HTTPException(status_code=404, detail="Food not found")

    return result


@router.put("/{food_id}", response_model=FoodLogRead)
def update_food(food_id: int, food: FoodLogCreate, session: Session = Depends(get_session)):
    result = db_update_food(session, food_id, food)
    if result is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return result


@router.delete("/{food_id}", response_model=dict)
def delete_food(food_id: int, session: Session = Depends(get_session)):
    success = db_delete_food(session, food_id)
    if not success:
        raise HTTPException(status_code=404, detail="Food not found")
    return {"detail": "Food deleted successfully"}
