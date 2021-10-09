from typing import Generator

from sqlmodel import create_engine, Session
from sqlalchemy.future import Engine

DATABASE_URL: str = "sqlite:///database.db"
engine: Engine = create_engine(DATABASE_URL)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
