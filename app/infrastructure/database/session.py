from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.database.engine import engine

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
)
