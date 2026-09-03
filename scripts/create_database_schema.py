from app.infrastructure.database.models import Base, DocumentModel
from app.infrastructure.database.engine import engine


def create_schema() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_schema()
    print("Database schema created successfully.")