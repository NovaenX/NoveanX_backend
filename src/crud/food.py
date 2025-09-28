from sqlmodel import Session, select
from ..models import FoodLog
from sqlalchemy.exc import IntegrityError
from ..schemas import FoodLogCreate


def db_add_food(session: Session, food: FoodLogCreate) -> FoodLog | None:
    db_food = FoodLog(**food.model_dump())
    try:
        session.add(db_food)
        session.commit()
        session.refresh(db_food)
        return db_food
    except IntegrityError:
        session.rollback()
        return None


def db_get_food_logs(session: Session):
    return session.exec(select(FoodLog)).all()


def db_search_food(session: Session, name: str) -> FoodLog | None:
    food = session.exec(select(FoodLog).where(
        FoodLog.food_name == name)).first()
    return food


def db_update_food(session: Session, food_id: int, food_data: FoodLogCreate) -> FoodLog | None:
    db_food = session.get(FoodLog, food_id)
    if not db_food:
        return None

    update_data = food_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_food, key, value)

    session.add(db_food)
    session.commit()
    session.refresh(db_food)
    return db_food


def db_delete_food(session: Session, food_id: int) -> bool:
    db_food = session.get(FoodLog, food_id)
    if not db_food:
        return False

    session.delete(db_food)
    session.commit()
    return True
