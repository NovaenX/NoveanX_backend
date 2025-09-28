from typing import Optional
from sqlmodel import SQLModel
from datetime import datetime


class FoodLogRead(SQLModel):
    id: int
    food_name: str
    calories: float
    protein: float
    created_at: datetime


class FoodLogCreate(SQLModel):
    food_name: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    created_at: Optional[datetime] = None
