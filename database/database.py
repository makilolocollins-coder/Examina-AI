# ============================================================
# EXAMINA AI
# DATABASE CONNECTION
# ============================================================

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Import Base
from database.models import Base

# Import all models so SQLAlchemy registers every table
from database import models  # noqa: F401


# ============================================================
# PROJECT DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# DATABASE DIRECTORY
# ============================================================

DATABASE_DIR = BASE_DIR / "data"

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# SQLITE DATABASE FILE
# ============================================================

DATABASE_PATH = DATABASE_DIR / "examina.db"


# ============================================================
# DATABASE URL
# ============================================================

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# ============================================================
# DATABASE ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    echo=False,
)


# ============================================================
# DATABASE SESSION
# ============================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# ============================================================
# CREATE ALL DATABASE TABLES
# ============================================================

def create_database() -> None:
    """
    Create all Examina AI database tables.

    The table definitions are contained in:

        database/models.py

    If the database already exists, existing tables
    are not deleted.
    """

    Base.metadata.create_all(
        bind=engine,
    )


# ============================================================
# GET DATABASE SESSION
# ============================================================

def get_db():
    """
    Provide a SQLAlchemy database session.

    The session is automatically closed after use.
    """

    db: Session = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database() -> None:
    """
    Initialize the Examina AI SQLite database.
    """

    create_database()


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("EXAMINA AI DATABASE")
    print("=" * 70)

    print()
    print("Database location:")
    print(DATABASE_PATH)

    print()

    initialize_database()

    print("Database initialized successfully.")
    print("All tables are ready.")

    print("=" * 70)
