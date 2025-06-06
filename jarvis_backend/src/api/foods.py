from typing import Annotated
from datetime import datetime
from sqlmodel import select
from fastapi import HTTPException, Query, APIRouter

from ..models import Food, FoodCreate
from ..db import SessionDep
from ..core import ist

router = APIRouter(prefix="/foods", tags=["foods"])


@router.post("/", response_model=Food)
def create_food(food: FoodCreate, session: SessionDep) -> Food:
    food = Food(
        **food.model_dump(),
        created_date=datetime.now(ist)

    )  # type: ignore
    session.add(food)
    session.commit()
    session.refresh(food)

    return food  # type: ignore


@router.get("/", response_model=list[Food])
def read_foods(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Food]:
    foods = session.exec(select(Food).offset(offset).limit(limit)).all()

    return foods  # type: ignore


@router.get("/{name}", response_model=Food)
def read_food(name: str, session: SessionDep) -> Food:
    food = session.exec(select(Food).where(Food.name == name)).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    return food


@router.put("/{name}", response_model=Food)
def update_food_by_name(
    name: str,
    updated_data: FoodCreate,
    session: SessionDep
) -> Food:
    food = session.exec(select(Food).where(Food.name == name)).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    food.quantity = updated_data.quantity
    food.protein = updated_data.protein
    food.calories = updated_data.calories
    food.created_date = datetime.now(ist)

    session.commit()
    session.refresh(food)

    return food


@router.delete("/{name}")
def delete_food(name: str, session: SessionDep):
    food = session.exec(select(Food).where(Food.name == name)).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    session.delete(food)
    session.commit()

    return {"ok": True}
