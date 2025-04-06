#Son algunos pasos los que tengo que llevar a cabo
# LLamar la db
# Crearla
# Hacer la dependencia

from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends, FastAPI

DB_NAME = "database.db"
DB_URL = f"sqlite:///{DB_NAME}"

engine = create_engine(DB_URL, echo=True)


def create_db_and_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
