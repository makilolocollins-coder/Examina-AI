# ============================================================
# EXAMINA AI
# ACADEMIC SESSION AND TERM SERVICE
# ============================================================

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import (
    AcademicSession,
    AcademicTerm,
)


# ============================================================
# CREATE ACADEMIC SESSION
# ============================================================

def create_academic_session(
    db: Session,
    name: str,
    curriculum_version: str,
):
    """
    Create an academic session.

    Example:
        2026/2027
    """

    name = name.strip()

    if not name:
        raise ValueError(
            "Academic session name cannot be empty."
        )

    # --------------------------------------------------------
    # Prevent duplicate session
    # --------------------------------------------------------

    existing = db.scalar(
        select(AcademicSession).where(
            AcademicSession.name == name
        )
    )

    if existing:
        raise ValueError(
            "This academic session already exists."
        )

    # --------------------------------------------------------
    # Create session
    # --------------------------------------------------------

    session = AcademicSession(
        name=name,
        curriculum_version=curriculum_version,
        is_current=False,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


# ============================================================
# CREATE THE THREE TERMS
# ============================================================

def create_default_terms(
    db: Session,
    academic_session_id: int,
):
    """
    Create the standard three terms:

        1st Term
        2nd Term
        3rd Term

    for an academic session.
    """

    academic_session = db.get(
        AcademicSession,
        academic_session_id,
    )

    if academic_session is None:
        raise ValueError(
            "Academic session does not exist."
        )

    term_names = [
        "1st Term",
        "2nd Term",
        "3rd Term",
    ]

    created_terms = []

    for term_name in term_names:

        existing = db.scalar(
            select(AcademicTerm).where(
                AcademicTerm.academic_session_id
                == academic_session_id,
                AcademicTerm.name
                == term_name,
            )
        )

        if existing:
            created_terms.append(existing)
            continue

        term = AcademicTerm(
            academic_session_id=academic_session_id,
            name=term_name,
            is_current=False,
        )

        db.add(term)

        created_terms.append(term)

    db.commit()

    for term in created_terms:
        db.refresh(term)

    return created_terms


# ============================================================
# GET ALL ACADEMIC SESSIONS
# ============================================================

def get_academic_sessions(
    db: Session,
):
    """
    Return all academic sessions.
    """

    query = (
        select(AcademicSession)
        .order_by(
            AcademicSession.name.desc()
        )
    )

    return list(
        db.scalars(query).all()
    )


# ============================================================
# GET ONE ACADEMIC SESSION
# ============================================================

def get_academic_session(
    db: Session,
    academic_session_id: int,
):
    """
    Get one academic session by ID.
    """

    return db.get(
        AcademicSession,
        academic_session_id,
    )


# ============================================================
# GET TERMS FOR A SESSION
# ============================================================

def get_academic_terms(
    db: Session,
    academic_session_id: int,
):
    """
    Return the three terms belonging
    to an academic session.
    """

    query = (
        select(AcademicTerm)
        .where(
            AcademicTerm.academic_session_id
            == academic_session_id
        )
        .order_by(
            AcademicTerm.id
        )
    )

    return list(
        db.scalars(query).all()
    )


# ============================================================
# GET CURRENT SESSION
# ============================================================

def get_current_session(
    db: Session,
):
    """
    Return the academic session currently
    marked as active.
    """

    return db.scalar(
        select(AcademicSession).where(
            AcademicSession.is_current.is_(True)
        )
    )


# ============================================================
# SET CURRENT SESSION
# ============================================================

def set_current_session(
    db: Session,
    academic_session_id: int,
):
    """
    Make one academic session the current session.

    Only one session should be current.
    """

    session = db.get(
        AcademicSession,
        academic_session_id,
    )

    if session is None:
        raise ValueError(
            "Academic session does not exist."
        )

    # --------------------------------------------------------
    # Remove current status from every session
    # --------------------------------------------------------

    sessions = list(
        db.scalars(
            select(AcademicSession)
        ).all()
    )

    for item in sessions:
        item.is_current = False

    # --------------------------------------------------------
    # Make selected session current
    # --------------------------------------------------------

    session.is_current = True

    db.commit()
    db.refresh(session)

    return session


# ============================================================
# GET CURRENT TERM
# ============================================================

def get_current_term(
    db: Session,
    academic_session_id: int,
):
    """
    Return the current term for a session.
    """

    return db.scalar(
        select(AcademicTerm).where(
            AcademicTerm.academic_session_id
            == academic_session_id,
            AcademicTerm.is_current.is_(True),
        )
    )


# ============================================================
# SET CURRENT TERM
# ============================================================

def set_current_term(
    db: Session,
    academic_session_id: int,
    academic_term_id: int,
):
    """
    Make one term the current term
    within an academic session.
    """

    term = db.get(
        AcademicTerm,
        academic_term_id,
    )

    if term is None:
        raise ValueError(
            "Academic term does not exist."
        )

    # --------------------------------------------------------
    # Make sure the term belongs to the session
    # --------------------------------------------------------

    if (
        term.academic_session_id
        != academic_session_id
    ):
        raise ValueError(
            "This term does not belong "
            "to the selected academic session."
        )

    # --------------------------------------------------------
    # Reset current term
    # --------------------------------------------------------

    terms = list(
        db.scalars(
            select(AcademicTerm).where(
                AcademicTerm.academic_session_id
                == academic_session_id
            )
        ).all()
    )

    for item in terms:
        item.is_current = False

    # --------------------------------------------------------
    # Set selected term
    # --------------------------------------------------------

    term.is_current = True

    db.commit()
    db.refresh(term)

    return term


# ============================================================
# GET TERM
# ============================================================

def get_term(
    db: Session,
    academic_term_id: int,
):
    """
    Get one academic term by ID.
    """

    return db.get(
        AcademicTerm,
        academic_term_id,
    )
