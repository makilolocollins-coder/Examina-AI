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
# SUBJECTS
# ============================================================

SUBJECTS = [
    ("Mathematics", "MATH", "Primary"),
    ("English Language", "ENG", "Primary"),
    ("Basic Science", "BSC", "Primary"),
    ("Social Studies", "SOS", "Primary"),
    ("Computer Studies", "ICT", "Primary"),
    ("Civic Education", "CIV", "Primary"),

    ("Mathematics", "MATH", "JSS"),
    ("English Language", "ENG", "JSS"),
    ("Basic Science", "BSC", "JSS"),
    ("Basic Technology", "BT", "JSS"),
    ("Social Studies", "SOS", "JSS"),
    ("Civic Education", "CIV", "JSS"),
    ("Computer Studies", "ICT", "JSS"),

    ("Mathematics", "MATH", "SS"),
    ("English Language", "ENG", "SS"),
    ("Biology", "BIO", "SS"),
    ("Chemistry", "CHEM", "SS"),
    ("Physics", "PHY", "SS"),
    ("Civic Education", "CIV", "SS"),
    ("Economics", "ECO", "SS"),
    ("Government", "GOV", "SS"),
    ("Literature in English", "LIT", "SS"),
    ("Financial Accounting", "FA", "SS"),
    ("Commerce", "COM", "SS"),
]


# ============================================================
# CLASSES
# ============================================================

CLASSES = [
    ("Primary 1", "Primary", None),
    ("Primary 2", "Primary", None),
    ("Primary 3", "Primary", None),
    ("Primary 4", "Primary", None),
    ("Primary 5", "Primary", None),
    ("Primary 6", "Primary", None),

    ("JSS 1", "JSS", None),
    ("JSS 2", "JSS", None),
    ("JSS 3", "JSS", None),

    ("SS 1", "SS", "Science"),
    ("SS 2", "SS", "Science"),
    ("SS 3", "SS", "Science"),

    ("SS 1", "SS", "Humanities"),
    ("SS 2", "SS", "Humanities"),
    ("SS 3", "SS", "Humanities"),

    ("SS 1", "SS", "Business"),
    ("SS 2", "SS", "Business"),
    ("SS 3", "SS", "Business"),
]


# ============================================================
# SEED DATABASE
# ============================================================

def seed_database():

    create_database()

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # SCHOOL
        # ----------------------------------------------------

        school = db.scalar(
            select(School).where(
                School.registration_number
                == "EXAMINA-DEMO-001"
            )
        )

        if school is None:

            school = School(
                name="Examina Demo School",
                registration_number="EXAMINA-DEMO-001",
                local_government="Demo LGA",
                state="Delta",
                address="Nigeria",
                email="demo@examina.ai",
                is_verified=True,
                is_active=True,
            )

            db.add(school)
            db.flush()

        # ----------------------------------------------------
        # ACADEMIC SESSION
        # ----------------------------------------------------

        session = db.scalar(
            select(AcademicSession).where(
                AcademicSession.school_id == school.id,
                AcademicSession.name == "2026/2027",
            )
        )

        if session is None:

            session = AcademicSession(
                school_id=school.id,
                name="2026/2027",
                curriculum_version="Nigeria Curriculum",
                is_current=True,
            )

            db.add(session)
            db.flush()

        # ----------------------------------------------------
        # TERMS
        # ----------------------------------------------------

        terms = [
            (1, "1st Term", True),
            (2, "2nd Term", False),
            (3, "3rd Term", False),
        ]

        for term_number, name, is_current in terms:

            existing = db.scalar(
                select(AcademicTerm).where(
                    AcademicTerm.academic_session_id
                    == session.id,
                    AcademicTerm.term_number
                    == term_number,
                )
            )

            if existing is None:

                db.add(
                    AcademicTerm(
                        academic_session_id=session.id,
                        name=name,
                        term_number=term_number,
                        is_current=is_current,
                    )
                )

        # ----------------------------------------------------
        # CLASSES
        # ----------------------------------------------------

        for class_name, education_level, stream in CLASSES:

            existing = db.scalar(
                select(SchoolClass).where(
                    SchoolClass.school_id == school.id,
                    SchoolClass.name == class_name,
                )
            )

            # SS classes can have multiple streams, so check
            # the stream as well.
            if education_level == "SS":

                existing = db.scalar(
                    select(SchoolClass).where(
                        SchoolClass.school_id == school.id,
                        SchoolClass.name == class_name,
                        SchoolClass.stream == stream,
                    )
                )

            if existing is None:

                db.add(
                    SchoolClass(
                        school_id=school.id,
                        name=class_name,
                        education_level=education_level,
                        stream=stream,
                    )
                )

        # ----------------------------------------------------
        # SUBJECTS
        # ----------------------------------------------------

        for name, code, education_level in SUBJECTS:

            existing = db.scalar(
                select(Subject).where(
                    Subject.name == name,
                    Subject.education_level
                    == education_level,
                )
            )

            if existing is None:

                db.add(
                    Subject(
                        name=name,
                        code=code,
                        education_level=education_level,
                        is_active=True,
                    )
                )

        db.commit()

        print(
            "=================================================="
        )
        print(
            "EXAMINA AI DATABASE SEEDED SUCCESSFULLY"
        )
        print(
            "=================================================="
        )

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    seed_database()
