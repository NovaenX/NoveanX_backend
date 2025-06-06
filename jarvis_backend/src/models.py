from datetime import datetime
from pydantic import BaseModel, Field as PydanticField
from sqlmodel import Field, SQLModel


class FoodCreate(BaseModel):
    name: str
    quantity: int = PydanticField(ge=0)
    protein: float = PydanticField(ge=0)
    calories: float = PydanticField(ge=0)


class Food(SQLModel, table=True):
    id: int = Field(unique=True, primary_key=True)
    name: str = Field(unique=True, index=True)
    quantity: int
    created_date: datetime
    protein: float
    calories: float
