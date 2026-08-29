# ============================================================
# EXAMINA AI
# SUBJECT SERVICE
# ============================================================

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import (
    Subject,
    Student,
    StudentSubject,
    AcademicTerm,
)


# ============================================================
# CREATE SUBJECT
# ============================================================

def create_subject(
    db: Session,
    name: str,
    category: str,
):
    """
    Create a new subject.

    Example:

        Mathematics
        Physics
        Chemistry
        Biology
    """

    name = name.strip()
    category = category.strip()

    # --------------------------------------------------------
    # Check if subject already exists
    # --------------------------------------------------------

    existing = db.scalar(
        select(Subject).where(
            Subject.name == name
        )
    )

    if existing is not None:
        raise ValueError(
            f"Subject '{name}' already exists."
        )

    # --------------------------------------------------------
    # Create subject
    # --------------------------------------------------------

    subject = Subject(
        name=name,
        category=category,
        active=True,
    )

    db.add(subject)
    db.commit()
    db.refresh(subject)

    return subject


# ============================================================
# GET SUBJECT
# ============================================================

def get_subject(
    db: Session,
    subject_id: int,
):
    """
    Get one subject by ID.
    """

    subject = db.get(
        Subject,
        subject_id,
    )

    if subject is None:
        raise ValueError(
            "Subject not found."
        )

    return subject


# ============================================================
# GET ALL SUBJECTS
# ============================================================

def get_subjects(
    db: Session,
    active_only: bool = True,
):
    """
    Get all subjects.

    By default, only active subjects are returned.
    """

    query = select(Subject)

    if active_only:
        query = query.where(
            Subject.active.is_(True)
        )

    query = query.order_by(
        Subject.name
    )

    return list(
        db.scalars(query).all()
    )


# ============================================================
# DEACTIVATE SUBJECT
# ============================================================

def deactivate_subject(
    db: Session,
    subject_id: int,
):
    """
    Deactivate a subject.

    We do NOT delete the subject because
    old student results may depend on it.
    """

    subject = get_subject(
        db,
        subject_id,
    )

    subject.active = False

    db.commit()
    db.refresh(subject)

    return subject


# ============================================================
# ACTIVATE SUBJECT
# ============================================================

def activate_subject(
    db: Session,
    subject_id: int,
):
    """
    Reactivate a subject.
    """

    subject = get_subject(
        db,
        subject_id,
    )

    subject.active = True

    db.commit()
    db.refresh(subject)

    return subject


# ============================================================
# ASSIGN SUBJECT TO STUDENT
# ============================================================

def assign_subject_to_student(
    db: Session,
    student_id: int,
    subject_id: int,
    academic_term_id: int,
):
    """
    Assign a subject to a student for a specific term.

    Example:

        Student: John
        Session: 2026/2027
        Term: 1st Term
        Subject: Mathematics
    """

    # --------------------------------------------------------
    # Check student
    # --------------------------------------------------------

    student = db.get(
        Student,
        student_id,
    )

    if student is None:
        raise ValueError(
            "Student not found."
        )

    # --------------------------------------------------------
    # Check subject
    # --------------------------------------------------------

    subject = get_subject(
        db,
        subject_id,
    )

    if not subject.active:
        raise ValueError(
            "This subject is inactive."
        )

    # --------------------------------------------------------
    # Check academic term
    # --------------------------------------------------------

    term = db.get(
        AcademicTerm,
        academic_term_id,
    )

    if term is None:
        raise ValueError(
            "Academic term not found."
        )

    # --------------------------------------------------------
    # Make sure term belongs to the student's
    # intended academic structure
    # --------------------------------------------------------

    existing = db.scalar(
        select(StudentSubject).where(
            StudentSubject.student_id
            == student_id,

            StudentSubject.subject_id
            == subject_id,

            StudentSubject.academic_term_id
            == academic_term_id,
        )
    )

    if existing is not None:
        raise ValueError(
            "This subject is already assigned "
            "to this student for this term."
        )

    # --------------------------------------------------------
    # Create assignment
    # --------------------------------------------------------

    student_subject = StudentSubject(
        student_id=student_id,
        subject_id=subject_id,
        academic_term_id=academic_term_id,
    )

    db.add(student_subject)
    db.commit()
    db.refresh(student_subject)

    return student_subject


# ============================================================
# REMOVE SUBJECT FROM STUDENT
# ============================================================

def remove_subject_from_student(
    db: Session,
    student_id: int,
    subject_id: int,
    academic_term_id: int,
):
    """
    Remove a subject assignment from a student.

    Existing results are not automatically deleted.
    """

    assignment = db.scalar(
        select(StudentSubject).where(
            StudentSubject.student_id
            == student_id,

            StudentSubject.subject_id
            == subject_id,

            StudentSubject.academic_term_id
            == academic_term_id,
        )
    )

    if assignment is None:
        raise ValueError(
            "Subject assignment not found."
        )

    db.delete(assignment)
    db.commit()

    return True


# ============================================================
# GET STUDENT SUBJECTS
# ============================================================

def get_student_subjects(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    """
    Get all subjects a student takes
    during a particular term.
    """

    query = (
        select(StudentSubject)
        .where(
            StudentSubject.student_id
            == student_id,

            StudentSubject.academic_term_id
            == academic_term_id,
        )
        .order_by(
            StudentSubject.subject_id
        )
    )

    return list(
        db.scalars(query).all()
    )


# ============================================================
# GET STUDENT SUBJECT NAMES
# ============================================================

def get_student_subject_names(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    """
    Return subject names instead of
    StudentSubject records.
    """

    assignments = get_student_subjects(
        db,
        student_id,
        academic_term_id,
    )

    return [
        assignment.subject.name
        for assignment in assignments
    ]


# ============================================================
# ASSIGN MULTIPLE SUBJECTS
# ============================================================

def assign_subjects_to_student(
    db: Session,
    student_id: int,
    subject_ids: list[int],
    academic_term_id: int,
):
    """
    Assign multiple subjects to a student
    for one academic term.
    """

    assignments = []

    for subject_id in subject_ids:

        assignment = assign_subject_to_student(
            db=db,
            student_id=student_id,
            subject_id=subject_id,
            academic_term_id=academic_term_id,
        )

        assignments.append(
            assignment
        )

    return assignments
