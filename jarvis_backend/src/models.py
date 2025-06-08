from datetime import datetime, date
from pydantic import BaseModel, Field as PydanticField
from sqlmodel import Field, SQLModel
from typing import Optional
from .core import ist


class DailyIntake(SQLModel, table=True):
    id: int = Field(unique=True, primary_key=True)
    today_date: date = Field(
        default_factory=lambda: datetime.now(ist).date(), index=True)
    calories_intake: float = 0
    protein_intake: float = 0


class FoodCreate(BaseModel):
    name: str
    quantity: int = PydanticField(ge=0)
    protein: float = PydanticField(ge=0)
    calories: float = PydanticField(ge=0)
    created_date: Optional[datetime] = None  # 👈 Allow custom date input


class Food(SQLModel, table=True):
    id: int = Field(unique=True, primary_key=True)
    name: str = Field(unique=True, index=True)
    quantity: int
    created_date: datetime
    protein: float
    calories: float


class FoodSettings(SQLModel, table=True):
    id: int = Field(default=1, primary_key=True)
    target_protein: float
    target_calories: float
