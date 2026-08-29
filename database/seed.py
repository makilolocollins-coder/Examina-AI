# ============================================================
# EXAMINA AI
# DATABASE SEED
# ============================================================
#
# PURPOSE:
#   Populate a new Examinа AI database with:
#
#   1. Academic session
#   2. 1st, 2nd and 3rd terms
#   3. School classes
#   4. Nigerian school subjects
#
# ============================================================

from sqlalchemy import select

from database.database import SessionLocal, create_database

from database.models import (
    AcademicSession,
    AcademicTerm,
    School,
    SchoolClass,
    Subject,
)


# ============================================================
# DEFAULT ACADEMIC SESSION
# ============================================================

DEFAULT_SESSION = "2026/2027"

DEFAULT_CURRICULUM = "Nigeria Curriculum"


# ============================================================
# TERMS
# ============================================================

TERMS = [
    "1st Term",
    "2nd Term",
    "3rd Term",
]


# ============================================================
# SCHOOL LEVELS AND CLASSES
# ============================================================
#
# The class name is stored in SchoolClass.
#
# Student does NOT store class_name.
#
# Student only stores:
#
#     class_id
#
# ============================================================

CLASSES = [

    # --------------------------------------------------------
    # PRIMARY
    # --------------------------------------------------------

    {
        "name": "Primary 1",
        "education_level": "Primary",
        "field": None,
    },

    {
        "name": "Primary 2",
        "education_level": "Primary",
        "field": None,
    },

    {
        "name": "Primary 3",
        "education_level": "Primary",
        "field": None,
    },

    {
        "name": "Primary 4",
        "education_level": "Primary",
        "field": None,
    },

    {
        "name": "Primary 5",
        "education_level": "Primary",
        "field": None,
    },

    {
        "name": "Primary 6",
        "education_level": "Primary",
        "field": None,
    },

    # --------------------------------------------------------
    # JUNIOR SECONDARY SCHOOL
    # --------------------------------------------------------

    {
        "name": "JSS 1",
        "education_level": "JSS",
        "field": None,
    },

    {
        "name": "JSS 2",
        "education_level": "JSS",
        "field": None,
    },

    {
        "name": "JSS 3",
        "education_level": "JSS",
        "field": None,
    },

    # --------------------------------------------------------
    # SENIOR SECONDARY SCHOOL
    # --------------------------------------------------------

    {
        "name": "SS 1",
        "education_level": "SS",
        "field": None,
    },

    {
        "name": "SS 2",
        "education_level": "SS",
        "field": None,
    },

    {
        "name": "SS 3",
        "education_level": "SS",
        "field": None,
    },
]


# ============================================================
# SUBJECT CATALOGUE
# ============================================================
#
# These are the subjects available in Examinа AI.
#
# category tells us the general subject grouping.
#
# Individual students will NOT automatically take every
# subject in this list.
#
# Their actual subjects will be assigned through
# StudentSubject.
#
# ============================================================

SUBJECTS = [

    # ========================================================
    # PRIMARY / BASIC
    # ========================================================

    {
        "name": "English Studies",
        "category": "Language",
    },

    {
        "name": "Mathematics",
        "category": "Mathematics",
    },

    {
        "name": "Basic Science",
        "category": "Science",
    },

    {
        "name": "Social Studies",
        "category": "Social Science",
    },

    {
        "name": "Civic Education",
        "category": "Civic",
    },

    {
        "name": "Computer Studies",
        "category": "Technology",
    },

    {
        "name": "Physical and Health Education",
        "category": "Physical Education",
    },

    {
        "name": "Agricultural Science",
        "category": "Agriculture",
    },

    {
        "name": "Cultural and Creative Arts",
        "category": "Arts",
    },

    {
        "name": "Religious Studies",
        "category": "Religion",
    },

    # ========================================================
    # JUNIOR SECONDARY
    # ========================================================

    {
        "name": "Basic Technology",
        "category": "Technology",
    },

    {
        "name": "Business Studies",
        "category": "Business",
    },

    {
        "name": "Home Economics",
        "category": "Vocational",
    },

    {
        "name": "French",
        "category": "Language",
    },

    {
        "name": "Arabic",
        "category": "Language",
    },

    # ========================================================
    # SENIOR SECONDARY
    # ========================================================

    {
        "name": "English Language",
        "category": "Language",
    },

    {
        "name": "General Mathematics",
        "category": "Mathematics",
    },

    {
        "name": "Further Mathematics",
        "category": "Mathematics",
    },

    {
        "name": "Physics",
        "category": "Science",
    },

    {
        "name": "Chemistry",
        "category": "Science",
    },

    {
        "name": "Biology",
        "category": "Science",
    },

    {
        "name": "Agricultural Science",
        "category": "Agriculture",
    },

    {
        "name": "Economics",
        "category": "Social Science",
    },

    {
        "name": "Government",
        "category": "Humanities",
    },

    {
        "name": "Geography",
        "category": "Social Science",
    },

    {
        "name": "Literature in English",
        "category": "Humanities",
    },

    {
        "name": "Commerce",
        "category": "Business",
    },

    {
        "name": "Accounting",
        "category": "Business",
    },

    {
        "name": "Computer Science",
        "category": "Technology",
    },

    {
        "name": "Data Processing",
        "category": "Technology",
    },

    {
        "name": "Technical Drawing",
        "category": "Technical",
    },

    {
        "name": "Civic Education",
        "category": "Civic",
    },

    {
        "name": "Physical and Health Education",
        "category": "Physical Education",
    },

    {
        "name": "Christian Religious Studies",
        "category": "Religion",
    },

    {
        "name": "Islamic Religious Studies",
        "category": "Religion",
    },

    {
        "name": "French",
        "category": "Language",
    },

    {
        "name": "Visual Art",
        "category": "Arts",
    },

    {
        "name": "Music",
        "category": "Arts",
    },

    {
        "name": "Food and Nutrition",
        "category": "Vocational",
    },

    {
        "name": "Home Management",
        "category": "Vocational",
    },
]


# ============================================================
# GET OR CREATE ACADEMIC SESSION
# ============================================================

def seed_academic_session(db):
    """
    Create the default academic session if it does not
    already exist.
    """

    session = db.scalar(
        select(AcademicSession).where(
            AcademicSession.name == DEFAULT_SESSION
        )
    )

    if session is None:

        session = AcademicSession(
            name=DEFAULT_SESSION,
            curriculum_version=DEFAULT_CURRICULUM,
            is_current=True,
        )

        db.add(session)
        db.flush()

        print(
            f"Created academic session: {DEFAULT_SESSION}"
        )

    else:

        print(
            f"Academic session already exists: {DEFAULT_SESSION}"
        )

    return session


# ============================================================
# CREATE TERMS
# ============================================================

def seed_terms(db, academic_session):
    """
    Create the three academic terms for the session.
    """

    for term_name in TERMS:

        existing_term = db.scalar(
            select(AcademicTerm).where(
                AcademicTerm.academic_session_id
                == academic_session.id,
                AcademicTerm.name
                == term_name,
            )
        )

        if existing_term is None:

            term = AcademicTerm(
                academic_session_id=academic_session.id,
                name=term_name,
                is_current=(term_name == "1st Term"),
            )

            db.add(term)

            print(
                f"Created term: {term_name}"
            )

        else:

            print(
                f"Term already exists: {term_name}"
            )


# ============================================================
# CREATE SUBJECT CATALOGUE
# ============================================================

def seed_subjects(db):
    """
    Create the master subject catalogue.

    Subjects are created only if they do not already exist.
    """

    for subject_data in SUBJECTS:

        existing_subject = db.scalar(
            select(Subject).where(
                Subject.name == subject_data["name"]
            )
        )

        if existing_subject is None:

            subject = Subject(
                name=subject_data["name"],
                category=subject_data["category"],
                active=True,
            )

            db.add(subject)

            print(
                f"Created subject: {subject_data['name']}"
            )

        else:

            print(
                f"Subject already exists: "
                f"{subject_data['name']}"
            )


# ============================================================
# CREATE SCHOOL CLASSES
# ============================================================

def seed_classes(db, school):
    """
    Create the standard school classes for a school.

    Every school gets its own class records.

    Example:

        School A
            ├── Primary 1
            ├── Primary 2
            ├── JSS 1
            └── SS 1

        School B
            ├── Primary 1
            ├── Primary 2
            ├── JSS 1
            └── SS 1

    The classes belong to different schools.
    """

    for class_data in CLASSES:

        existing_class = db.scalar(
            select(SchoolClass).where(
                SchoolClass.school_id == school.id,
                SchoolClass.name == class_data["name"],
            )
        )

        if existing_class is None:

            school_class = SchoolClass(
                name=class_data["name"],
                education_level=class_data[
                    "education_level"
                ],
                field=class_data["field"],
                school_id=school.id,
            )

            db.add(school_class)

            print(
                f"Created class: "
                f"{class_data['name']}"
            )

        else:

            print(
                f"Class already exists: "
                f"{class_data['name']}"
            )


# ============================================================
# CREATE DEFAULT DEVELOPMENT SCHOOL
# ============================================================

def seed_default_school(db):
    """
    Create a development school so that the database can
    immediately be tested.

    In production, real schools will register through the
    Examinа AI school registration system.
    """

    school = db.scalar(
        select(School).where(
            School.name == "Examina AI Demo School"
        )
    )

    if school is None:

        school = School(
            name="Examina AI Demo School",
            phone="0000000000",
            email="demo@examina.ai",
            local_government="Demo",
            state="Delta",
            verified=True,
        )

        db.add(school)
        db.flush()

        print(
            "Created development school."
        )

    else:

        print(
            "Development school already exists."
        )

    return school


# ============================================================
# MAIN SEED FUNCTION
# ============================================================

def seed_database():

    print()
    print("=" * 70)
    print("EXAMINA AI DATABASE SEED")
    print("=" * 70)

    # --------------------------------------------------------
    # MAKE SURE TABLES EXIST
    # --------------------------------------------------------

    create_database()

    # --------------------------------------------------------
    # OPEN DATABASE SESSION
    # --------------------------------------------------------

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # ACADEMIC SESSION
        # ----------------------------------------------------

        academic_session = seed_academic_session(db)

        # ----------------------------------------------------
        # TERMS
        # ----------------------------------------------------

        seed_terms(
            db,
            academic_session,
        )

        # ----------------------------------------------------
        # SUBJECTS
        # ----------------------------------------------------

        seed_subjects(db)

        # ----------------------------------------------------
        # DEVELOPMENT SCHOOL
        # ----------------------------------------------------

        school = seed_default_school(db)

        # ----------------------------------------------------
        # SCHOOL CLASSES
        # ----------------------------------------------------

        seed_classes(
            db,
            school,
        )

        # ----------------------------------------------------
        # SAVE EVERYTHING
        # ----------------------------------------------------

        db.commit()

        print()
        print("=" * 70)
        print("DATABASE SEED COMPLETED SUCCESSFULLY")
        print("=" * 70)

    except Exception as error:

        db.rollback()

        print()
        print("=" * 70)
        print("DATABASE SEED FAILED")
        print("=" * 70)

        print(
            f"Error: {error}"
        )

        raise

    finally:

        db.close()


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    seed_database()
