# ============================================================
# ============================================================
# EXAMINA AI
# DATABASE CONNECTION
# ============================================================

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base

# Import models so SQLAlchemy registers every table
from database import models


# ============================================================
# DATABASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "data"

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# DATABASE FILE
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
# CREATE DATABASE TABLES
# ============================================================

def create_database():
    """
    Create all Examinа AI database tables.

    Tables are defined in database/models.py.
    """

    Base.metadata.create_all(
        bind=engine,
    )


# ============================================================
# GET DATABASE SESSION
# ============================================================

def get_db():
    """
    Create a database session.

    The session is automatically closed
    after use.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# INITIALIZE DATABASE
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("EXAMINA AI DATABASE")
    print("=" * 70)

    print("Database location:")
    print(DATABASE_PATH)

    create_database()

    print()
    print("Database initialized successfully.")
    print("All tables are ready.")
    print("=" * 70)
