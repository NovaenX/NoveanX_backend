from zoneinfo import ZoneInfo
from datetime import datetime
from sqlmodel import SQLModel, Field


class FoodLog(SQLModel, table=True):
    __tablename__ = "food_logs"
    id: int | None = Field(default=None, primary_key=True)
    food_name: str = Field(index=True, unique=True)
    calories: float = Field(default=0.0)
    protein: float = Field(default=0.0)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("Asia/Kolkata")))
