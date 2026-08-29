# ============================================================
# EXAMINA AI
# STUDENT SERVICE
# ============================================================

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import (
    Student,
    School,
    SchoolClass,
    Subject,
    StudentSubject,
    AcademicTerm,
)


# ============================================================
# CREATE STUDENT
# ============================================================

def create_student(
    db: Session,
    admission_number: str,
    first_name: str,
    last_name: str,
    school_id: int,
    class_id: int,
    education_level: str,
    middle_name: str | None = None,
    field: str | None = None,
):
    """
    Create a new student.
    """

    # --------------------------------------------------------
    # Check admission number
    # --------------------------------------------------------

    existing_student = db.scalar(
        select(Student).where(
            Student.admission_number == admission_number
        )
    )

    if existing_student:
        raise ValueError(
            "A student with this admission number already exists."
        )

    # --------------------------------------------------------
    # Check school
    # --------------------------------------------------------

    school = db.get(School, school_id)

    if school is None:
        raise ValueError(
            "School does not exist."
        )

    # --------------------------------------------------------
    # Check class
    # --------------------------------------------------------

    school_class = db.get(
        SchoolClass,
        class_id,
    )

    if school_class is None:
        raise ValueError(
            "Class does not exist."
        )

    # --------------------------------------------------------
    # Make sure class belongs to school
    # --------------------------------------------------------

    if school_class.school_id != school_id:
        raise ValueError(
            "This class does not belong to the selected school."
        )

    # --------------------------------------------------------
    # Create student
    # --------------------------------------------------------

    student = Student(
        admission_number=admission_number,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        school_id=school_id,
        class_id=class_id,
        education_level=education_level,
        field=field,
        active=True,
    )

    db.add(student)

    db.commit()

    db.refresh(student)

    return student


# ============================================================
# GET STUDENT BY ID
# ============================================================

def get_student(
    db: Session,
    student_id: int,
):
    """
    Get a student using their database ID.
    """

    return db.get(
        Student,
        student_id,
    )


# ============================================================
# GET STUDENT BY ADMISSION NUMBER
# ============================================================

def get_student_by_admission_number(
    db: Session,
    admission_number: str,
):
    """
    Find a student using admission number.
    """

    return db.scalar(
        select(Student).where(
            Student.admission_number == admission_number
        )
    )


# ============================================================
# GET STUDENTS IN A SCHOOL
# ============================================================

def get_school_students(
    db: Session,
    school_id: int,
    active_only: bool = True,
):
    """
    Return students belonging to a school.
    """

    query = select(Student).where(
        Student.school_id == school_id
    )

    if active_only:
        query = query.where(
            Student.active.is_(True)
        )

    query = query.order_by(
        Student.last_name,
        Student.first_name,
    )

    return list(
        db.scalars(query).all()
    )


# ============================================================
# GET STUDENTS IN A CLASS
# ============================================================

def get_class_students(
    db: Session,
    class_id: int,
    active_only: bool = True,
):
    """
    Return students belonging to a particular class.
    """

    query = select(Student).where(
        Student.class_id == class_id
    )

    if active_only:
        query = query.where(
            Student.active.is_(True)
        )

    query = query.order_by(
        Student.last_name,
        Student.first_name,
    )

    return list(
        db.scalars(query).all()
    )


# ============================================================
# MOVE STUDENT TO ANOTHER CLASS
# ============================================================

def move_student_to_class(
    db: Session,
    student_id: int,
    new_class_id: int,
):
    """
    Move a student to another class.
    """

    student = db.get(
        Student,
        student_id,
    )

    if student is None:
        raise ValueError(
            "Student does not exist."
        )

    new_class = db.get(
        SchoolClass,
        new_class_id,
    )

    if new_class is None:
        raise ValueError(
            "New class does not exist."
        )

    # --------------------------------------------------------
    # Class must belong to same school
    # --------------------------------------------------------

    if new_class.school_id != student.school_id:
        raise ValueError(
            "Student cannot be moved to a class "
            "belonging to another school."
        )

    student.class_id = new_class_id

    db.commit()

    db.refresh(student)

    return student


# ============================================================
# UPDATE STUDENT
# ============================================================

def update_student(
    db: Session,
    student_id: int,
    first_name: str | None = None,
    middle_name: str | None = None,
    last_name: str | None = None,
    field: str | None = None,
):
    """
    Update student information.
    """

    student = db.get(
        Student,
        student_id,
    )

    if student is None:
        raise ValueError(
            "Student does not exist."
        )

    if first_name is not None:
        student.first_name = first_name

    if middle_name is not None:
        student.middle_name = middle_name

    if last_name is not None:
        student.last_name = last_name

    if field is not None:
        student.field = field

    db.commit()

    db.refresh(student)

    return student


# ============================================================
# DEACTIVATE STUDENT
# ============================================================

def deactivate_student(
    db: Session,
    student_id: int,
):
    """
    Deactivate a student without deleting their records.
    """

    student = db.get(
        Student,
        student_id,
    )

    if student is None:
        raise ValueError(
            "Student does not exist."
        )

    student.active = False

    db.commit()

    db.refresh(student)

    return student


# ============================================================
# ACTIVATE STUDENT
# ============================================================

def activate_student(
    db: Session,
    student_id: int,
):
    """
    Reactivate a student.
    """

    student = db.get(
        Student,
        student_id,
    )

    if student is None:
        raise ValueError(
            "Student does not exist."
        )

    student.active = True

    db.commit()

    db.refresh(student)

    return student


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
    Assign a subject to a student for a particular term.
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
            "Student does not exist."
        )

    # --------------------------------------------------------
    # Check subject
    # --------------------------------------------------------

    subject = db.get(
        Subject,
        subject_id,
    )

    if subject is None:
        raise ValueError(
            "Subject does not exist."
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
            "Academic term does not exist."
        )

    # --------------------------------------------------------
    # Prevent duplicate assignment
    # --------------------------------------------------------

    existing = db.scalar(
        select(StudentSubject).where(
            StudentSubject.student_id == student_id,
            StudentSubject.subject_id == subject_id,
            StudentSubject.academic_term_id == academic_term_id,
        )
    )

    if existing:
        raise ValueError(
            "This subject is already assigned "
            "to the student for this term."
        )

    # --------------------------------------------------------
    # Create assignment
    # --------------------------------------------------------

    assignment = StudentSubject(
        student_id=student_id,
        subject_id=subject_id,
        academic_term_id=academic_term_id,
    )

    db.add(assignment)

    db.commit()

    db.refresh(assignment)

    return assignment


# ============================================================
# GET STUDENT SUBJECTS FOR A TERM
# ============================================================

def get_student_subjects(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    """
    Get all subjects a student takes during a term.
    """

    query = (
        select(StudentSubject)
        .where(
            StudentSubject.student_id == student_id,
            StudentSubject.academic_term_id == academic_term_id,
        )
        .order_by(Subject.name)
    )

    return list(
        db.scalars(
            query
        ).all()
    )


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
    Remove a subject assignment.
    """

    assignment = db.scalar(
        select(StudentSubject).where(
            StudentSubject.student_id == student_id,
            StudentSubject.subject_id == subject_id,
            StudentSubject.academic_term_id == academic_term_id,
        )
    )

    if assignment is None:
        raise ValueError(
            "Subject assignment does not exist."
        )

    db.delete(assignment)

    db.commit()

    return True


# ============================================================
# GET STUDENT CLASS NAME
# ============================================================

def get_student_class_name(
    db: Session,
    student_id: int,
):
    """
    Get the student's class name.

    The class name comes from SchoolClass.
    It is NOT stored separately in Student.
    """

    student = db.get(
        Student,
        student_id,
    )

    if student is None:
        raise ValueError(
            "Student does not exist."
        )

    return student.school_class.name


# ============================================================
# SEARCH STUDENTS
# ============================================================

def search_students(
    db: Session,
    school_id: int,
    search_text: str,
):
    """
    Search students by:
    - first name
    - middle name
    - last name
    - admission number
    """

    search = f"%{search_text.strip()}%"

    query = select(Student).where(
        Student.school_id == school_id,
        Student.active.is_(True),
    ).where(
        (
            Student.first_name.ilike(search)
        )
        |
        (
            Student.middle_name.ilike(search)
        )
        |
        (
            Student.last_name.ilike(search)
        )
        |
        (
            Student.admission_number.ilike(search)
        )
    ).order_by(
        Student.last_name,
        Student.first_name,
    )

    return list(
        db.scalars(query).all()
    )
