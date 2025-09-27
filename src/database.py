from sqlmodel import Session, create_engine, SQLModel
import settings as s

DATABASE_URL = f"sqlite:///{s.db_path}"
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
