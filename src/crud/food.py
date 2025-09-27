from sqlmodel import Session, select
from ..models import FoodLog
from sqlalchemy.exc import IntegrityError


def db_add_food(session: Session, food: FoodLog) -> FoodLog | None:
    try:
        session.add(food)
        session.commit()
        session.refresh(food)
        return food
    except IntegrityError:
        session.rollback()
        return None


def db_get_food_logs(session: Session):
    return session.exec(select(FoodLog)).all()


def db_search_food(session: Session, name: str) -> FoodLog | None:
    food = session.exec(select(FoodLog).where(
        FoodLog.food_name == name)).first()
    return food
