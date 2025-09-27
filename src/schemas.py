from sqlmodel import SQLModel
from datetime import datetime


class FoodLogCreate(SQLModel):
    food_name: str
    calories: float = 0
    protein: float = 0


class FoodLogRead(SQLModel):
    id: int
    food_name: str
    calories: float
    protein: float
    created_at: datetime
