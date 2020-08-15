import sqlalchemy as sa
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Process(Base):
    __tablename__ = 'process'
    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    consultado = sa.Column(sa.Text(), nullable=True)
    extraido = sa.Column(sa.Text(), nullable=True)
    comarca = sa.Column(sa.Text(), nullable=True)
    o_julgador = sa.Column(sa.Text(), nullable=True)
    procedimento = sa.Column(sa.Text(), nullable=True)
    ativa = sa.Column(sa.Text(), nullable=True)
    passiva = sa.Column(sa.Text(), nullable=True)
    e_ativa = sa.Column(sa.Text(), nullable=True)
    e_passiva = sa.Column(sa.Text(), nullable=True)
    created = sa.Column(sa.Text())

Base.metadata.create_all(bind=engine)

PydanticProcess = sqlalchemy_to_pydantic(Process)
