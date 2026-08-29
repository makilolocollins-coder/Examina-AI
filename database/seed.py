# ============================================================
# EXAMINA AI
# DATABASE SEED
# ============================================================
#
# This file creates the initial data required by Examinа AI.
#
# It creates:
#
#   1. Academic sessions
#   2. 1st Term
#   3. 2nd Term
#   4. 3rd Term
#   5. Subjects
#
# It does NOT create individual students or results.
# Those will be created through the school portal.
#
# ============================================================

from sqlalchemy import select

from database.database import SessionLocal, create_database

from database.models import (
    AcademicSession,
    AcademicTerm,
    Subject,
)


# ============================================================
# CURRICULUM VERSION
# ============================================================

CURRICULUM_VERSION = "Nigeria National Curriculum"


# ============================================================
# SUBJECTS
# ============================================================
#
# These are the general subjects available in the system.
#
# A student will NOT automatically take every subject.
#
# The school will assign the appropriate subjects to each
# student according to their education level and field.
#
# ============================================================

SUBJECTS = [

    # --------------------------------------------------------
    # PRIMARY
    # --------------------------------------------------------

    {
        "name": "Mathematics",
        "category": "Primary",
    },

    {
        "name": "English Studies",
        "category": "Primary",
    },

    {
        "name": "Basic Science",
        "category": "Primary",
    },

    {
        "name": "Social Studies",
        "category": "Primary",
    },

    {
        "name": "Civic Education",
        "category": "Primary",
    },

    {
        "name": "Computer Studies",
        "category": "Primary",
    },

    {
        "name": "Physical and Health Education",
        "category": "Primary",
    },

    {
        "name": "Agricultural Science",
        "category": "Primary",
    },

    {
        "name": "Cultural and Creative Arts",
        "category": "Primary",
    },

    # --------------------------------------------------------
    # JSS
    # --------------------------------------------------------

    {
        "name": "English Language",
        "category": "JSS",
    },

    {
        "name": "Mathematics",
        "category": "JSS",
    },

    {
        "name": "Basic Science",
        "category": "JSS",
    },

    {
        "name": "Basic Technology",
        "category": "JSS",
    },

    {
        "name": "Social Studies",
        "category": "JSS",
    },

    {
        "name": "Civic Education",
        "category": "JSS",
    },

    {
        "name": "Computer Studies",
        "category": "JSS",
    },

    {
        "name": "Agricultural Science",
        "category": "JSS",
    },

    {
        "name": "Business Studies",
        "category": "JSS",
    },

    {
        "name": "Physical and Health Education",
        "category": "JSS",
    },

    {
        "name": "Christian Religious Studies",
        "category": "JSS",
    },

    {
        "name": "Islamic Religious Studies",
        "category": "JSS",
    },

    {
        "name": "French",
        "category": "JSS",
    },

    # --------------------------------------------------------
    # SENIOR SECONDARY
    # --------------------------------------------------------

    {
        "name": "English Language",
        "category": "SS",
    },

    {
        "name": "Mathematics",
        "category": "SS",
    },

    {
        "name": "Biology",
        "category": "SS",
    },

    {
        "name": "Chemistry",
        "category": "SS",
    },

    {
        "name": "Physics",
        "category": "SS",
    },

    {
        "name": "Economics",
        "category": "SS",
    },

    {
        "name": "Government",
        "category": "SS",
    },

    {
        "name": "Literature in English",
        "category": "SS",
    },

    {
        "name": "Geography",
        "category": "SS",
    },

    {
        "name": "Commerce",
        "category": "SS",
    },

    {
        "name": "Financial Accounting",
        "category": "SS",
    },

    {
        "name": "Agricultural Science",
        "category": "SS",
    },

    {
        "name": "Computer Studies",
        "category": "SS",
    },

    {
        "name": "Data Processing",
        "category": "SS",
    },

    {
        "name": "Further Mathematics",
        "category": "SS",
    },

    {
        "name": "Christian Religious Studies",
        "category": "SS",
    },

    {
        "name": "Islamic Religious Studies",
        "category": "SS",
    },

    {
        "name": "French",
        "category": "SS",
    },
]


# ============================================================
# ACADEMIC TERMS
# ============================================================

TERMS = [
    "1st Term",
    "2nd Term",
    "3rd Term",
]


# ============================================================
# CREATE ACADEMIC SESSION
# ============================================================

def create_academic_session(
    db,
    session_name: str,
):
    """
    Create an academic session and its three terms.

    Example:

        2026/2027
            ├── 1st Term
            ├── 2nd Term
            └── 3rd Term
    """

    # --------------------------------------------------------
    # CHECK WHETHER SESSION ALREADY EXISTS
    # --------------------------------------------------------

    existing_session = db.scalar(
        select(AcademicSession).where(
            AcademicSession.name == session_name
        )
    )

    if existing_session:

        print(
            f"Academic session {session_name} "
            f"already exists."
        )

        return existing_session

    # --------------------------------------------------------
    # CREATE SESSION
    # --------------------------------------------------------

    academic_session = AcademicSession(
        name=session_name,

        curriculum_version=CURRICULUM_VERSION,

        is_current=True,
    )

    db.add(
        academic_session
    )

    db.flush()

    print(
        f"Created academic session: "
        f"{session_name}"
    )

    # --------------------------------------------------------
    # CREATE THREE TERMS
    # --------------------------------------------------------

    for index, term_name in enumerate(TERMS):

        term = AcademicTerm(

            academic_session_id=
                academic_session.id,

            name=term_name,

            # Make the first term current initially.
            is_current=(index == 0),
        )

        db.add(term)

        print(
            f"    Created {term_name}"
        )

    return academic_session


# ============================================================
# CREATE SUBJECTS
# ============================================================

def create_subjects(db):
    """
    Create the master subject list.

    Existing subjects are skipped.
    """

    created = 0
    skipped = 0

    for subject_data in SUBJECTS:

        subject_name = subject_data["name"]

        # ----------------------------------------------------
        # CHECK FOR EXISTING SUBJECT
        # ----------------------------------------------------

        existing_subject = db.scalar(
            select(Subject).where(
                Subject.name == subject_name
            )
        )

        if existing_subject:

            skipped += 1

            continue

        # ----------------------------------------------------
        # CREATE SUBJECT
        # ----------------------------------------------------

        subject = Subject(

            name=subject_name,

            category=
                subject_data["category"],

            active=True,
        )

        db.add(subject)

        created += 1

    print()
    print(
        f"Subjects created: {created}"
    )

    print(
        f"Subjects already existing: {skipped}"
    )


# ============================================================
# MAIN SEED FUNCTION
# ============================================================

def seed_database():
    """
    Populate the Examinа AI database with initial data.
    """

    print("=" * 70)
    print("EXAMINA AI DATABASE SEED")
    print("=" * 70)

    # --------------------------------------------------------
    # MAKE SURE DATABASE TABLES EXIST
    # --------------------------------------------------------

    create_database()

    # --------------------------------------------------------
    # OPEN DATABASE SESSION
    # --------------------------------------------------------

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # CREATE CURRENT ACADEMIC SESSION
        # ----------------------------------------------------

        create_academic_session(
            db=db,
            session_name="2026/2027",
        )

        # ----------------------------------------------------
        # CREATE MASTER SUBJECTS
        # ----------------------------------------------------

        create_subjects(
            db=db
        )

        # ----------------------------------------------------
        # SAVE EVERYTHING
        # ----------------------------------------------------

        db.commit()

        print()
        print(
            "=" * 70
        )

        print(
            "DATABASE SEED COMPLETED SUCCESSFULLY."
        )

        print(
            "=" * 70
        )

    except Exception as error:

        # ----------------------------------------------------
        # UNDO CHANGES IF SOMETHING FAILS
        # ----------------------------------------------------

        db.rollback()

        print()
        print(
            "DATABASE SEED FAILED."
        )

        print(
            f"Error: {error}"
        )

        raise

    finally:

        # ----------------------------------------------------
        # CLOSE DATABASE CONNECTION
        # ----------------------------------------------------

        db.close()


# ============================================================
# RUN SEED
# ============================================================

if __name__ == "__main__":

    seed_database()
