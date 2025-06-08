from typing import Annotated
from datetime import datetime, date
from sqlmodel import select
from fastapi import HTTPException, APIRouter, Query

from ..models import Food, FoodCreate, FoodSettings, DailyIntake
from ..db import SessionDep
from ..core import ist

router = APIRouter(prefix="/foods", tags=["foods"])
settings_router = APIRouter(prefix="/settings", tags=["Settings"])
daily_router = APIRouter(prefix="/daily", tags=["Daily Intake"])


@router.post("/", response_model=Food)
def create_food(food: FoodCreate, session: SessionDep) -> Food:
    food = Food(
        **food.model_dump(),
        created_date=datetime.now(ist)

    )  # type: ignore
    session.add(food)

    # Update DailyIntake
    today = datetime.now(ist).date()
    summary = session.exec(select(DailyIntake).where(
        DailyIntake.today_date == today)).first()
    if summary:
        summary.calories_intake += calories
        summary.protein_intake += protein
    else:
        summary = DailyIntake(
            today_date=today,
            calories_intake=calories,
            protein_intake=protein
        )

    session.add(summary)
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
    if updated_data.created_date is not None:
        food.created_date = updated_data.created_date
    else:
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


@settings_router.get("/", response_model=FoodSettings)
def get_food_settings(session: SessionDep):
    settings = session.get(FoodSettings, 1)
    if not settings:
        # Auto-create with zero values if not exists
        settings = FoodSettings(id=1, target_protein=0, target_calories=0)
        session.add(settings)
        session.commit()
        session.refresh(settings)
    return settings


@settings_router.put("/", response_model=FoodSettings)
def update_settings(
    target_protein: float,
    target_calories: float,
    session: SessionDep
):
    settings = session.get(FoodSettings, 1)
    if not settings:
        settings = FoodSettings(
            id=1, target_protein=target_protein, target_calories=target_calories)
        session.add(settings)
    else:
        settings.target_protein = target_protein
        settings.target_calories = target_calories

    session.commit()
    session.refresh(settings)

    return settings


@router.get("/")
def get_today_intake(session: SessionDep):
    today = date.today()
    intake = session.exec(select(DailyIntake).where(
        DailyIntake.today_date == today)).first()
    if not intake:
        intake = DailyIntake(
            today_date=today, calories_intake=0, protein_intake=0)
        session.add(intake)
        session.commit()
        session.refresh(intake)
    return intake


@router.put("/")
def update_today_intake(
    calories_intake: float,
    protein_intake: float,
    session: SessionDep,
):
    today = date.today()
    intake = session.exec(select(DailyIntake).where(
        DailyIntake.today_date == today)).first()

    if not intake:
        intake = DailyIntake(
            today_date=today, calories_intake=calories_intake, protein_intake=protein_intake)
        session.add(intake)
    else:
        intake.calories_intake = calories_intake
        intake.protein_intake = protein_intake

    session.commit()
    session.refresh(intake)
    return intake
