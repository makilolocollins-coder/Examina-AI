# ============================================================
# EXAMINA AI
# RESULT SERVICE
# ============================================================

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import (
    Student,
    Subject,
    Result,
    AcademicTerm,
    StudentSubject,
)


# ============================================================
# GRADE CALCULATION
# ============================================================

def calculate_grade(total: float) -> str:
    """
    Convert a total score into a grade.

    70 - 100 = A
    60 - 69  = B
    50 - 59  = C
    45 - 49  = D
    40 - 44  = E
    0  - 39  = F
    """

    if total >= 70:
        return "A"

    if total >= 60:
        return "B"

    if total >= 50:
        return "C"

    if total >= 45:
        return "D"

    if total >= 40:
        return "E"

    return "F"


# ============================================================
# CALCULATE TOTAL
# ============================================================

def calculate_total(
    first_test: float,
    second_test: float,
    exam: float,
) -> float:
    """
    Calculate the student's total score.
    """

    return (
        float(first_test)
        + float(second_test)
        + float(exam)
    )


# ============================================================
# CREATE OR UPDATE RESULT
# ============================================================

def save_result(
    db: Session,
    student_id: int,
    subject_id: int,
    academic_term_id: int,
    first_test: float = 0.0,
    second_test: float = 0.0,
    exam: float = 0.0,
):
    """
    Create a new result or update an existing result.
    """

    # --------------------------------------------------------
    # Validate student
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
    # Validate subject
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
    # Validate term
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
    # Make sure student takes subject
    # --------------------------------------------------------

    assignment = db.scalar(
        select(StudentSubject).where(
            StudentSubject.student_id == student_id,
            StudentSubject.subject_id == subject_id,
            StudentSubject.academic_term_id == academic_term_id,
        )
    )

    if assignment is None:
        raise ValueError(
            "This subject has not been assigned "
            "to this student for this term."
        )

    # --------------------------------------------------------
    # Validate scores
    # --------------------------------------------------------

    first_test = float(first_test)
    second_test = float(second_test)
    exam = float(exam)

    if first_test < 0 or first_test > 20:
        raise ValueError(
            "First test must be between 0 and 20."
        )

    if second_test < 0 or second_test > 20:
        raise ValueError(
            "Second test must be between 0 and 20."
        )

    if exam < 0 or exam > 60:
        raise ValueError(
            "Exam must be between 0 and 60."
        )

    # --------------------------------------------------------
    # Calculate total
    # --------------------------------------------------------

    total = calculate_total(
        first_test,
        second_test,
        exam,
    )

    grade = calculate_grade(total)

    # --------------------------------------------------------
    # Find existing result
    # --------------------------------------------------------

    result = db.scalar(
        select(Result).where(
            Result.student_id == student_id,
            Result.subject_id == subject_id,
            Result.academic_term_id == academic_term_id,
        )
    )

    # --------------------------------------------------------
    # Create result
    # --------------------------------------------------------

    if result is None:

        result = Result(
            student_id=student_id,
            subject_id=subject_id,
            academic_term_id=academic_term_id,
            first_test=first_test,
            second_test=second_test,
            exam=exam,
            total=total,
            grade=grade,
        )

        db.add(result)

    # --------------------------------------------------------
    # Update result
    # --------------------------------------------------------

    else:

        result.first_test = first_test
        result.second_test = second_test
        result.exam = exam
        result.total = total
        result.grade = grade

    db.commit()

    db.refresh(result)

    return result


# ============================================================
# GET ONE RESULT
# ============================================================

def get_result(
    db: Session,
    student_id: int,
    subject_id: int,
    academic_term_id: int,
):
    """
    Get one student's result for one subject and term.
    """

    return db.scalar(
        select(Result).where(
            Result.student_id == student_id,
            Result.subject_id == subject_id,
            Result.academic_term_id == academic_term_id,
        )
    )


# ============================================================
# GET STUDENT RESULTS
# ============================================================

def get_student_results(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    """
    Get all results belonging to a student
    for a particular term.
    """

    query = (
        select(Result)
        .where(
            Result.student_id == student_id,
            Result.academic_term_id == academic_term_id,
        )
        .join(
            Subject,
            Result.subject_id == Subject.id,
        )
        .order_by(
            Subject.name
        )
    )

    return list(
        db.scalars(query).all()
    )


# ============================================================
# CALCULATE STUDENT AVERAGE
# ============================================================

def calculate_student_average(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    """
    Calculate the student's average score
    across all subjects for a term.
    """

    results = get_student_results(
        db,
        student_id,
        academic_term_id,
    )

    if not results:
        return 0.0

    total = sum(
        result.total
        for result in results
    )

    return total / len(results)


# ============================================================
# CALCULATE SUBJECT POSITIONS
# ============================================================

def calculate_subject_positions(
    db: Session,
    subject_id: int,
    academic_term_id: int,
):
    """
    Rank students in a subject from highest
    score to lowest score.

    Equal scores receive the same position.
    """

    query = (
        select(Result)
        .join(
            Student,
            Result.student_id == Student.id,
        )
        .where(
            Result.subject_id == subject_id,
            Result.academic_term_id == academic_term_id,
            Student.active.is_(True),
        )
        .order_by(
            Result.total.desc()
        )
    )

    results = list(
        db.scalars(query).all()
    )

    previous_score = None
    position = 0

    for index, result in enumerate(results, start=1):

        if result.total != previous_score:
            position = index

        result.position = position

        previous_score = result.total

    db.commit()

    return results


# ============================================================
# CALCULATE OVERALL POSITIONS
# ============================================================

def calculate_overall_positions(
    db: Session,
    academic_term_id: int,
):
    """
    Rank students according to their average score
    across their subjects.

    Highest average = position 1.
    """

    students_query = select(Student).where(
        Student.active.is_(True)
    )

    students = list(
        db.scalars(students_query).all()
    )

    student_averages = []

    for student in students:

        average = calculate_student_average(
            db,
            student.id,
            academic_term_id,
        )

        if average > 0:

            student_averages.append(
                (
                    student,
                    average,
                )
            )

    # --------------------------------------------------------
    # Highest average first
    # --------------------------------------------------------

    student_averages.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    rankings = []

    previous_average = None
    position = 0

    for index, (student, average) in enumerate(
        student_averages,
        start=1,
    ):

        if average != previous_average:
            position = index

        rankings.append(
            {
                "student_id": student.id,
                "student_name": (
                    f"{student.first_name} "
                    f"{student.last_name}"
                ),
                "average": round(
                    average,
                    2,
                ),
                "position": position,
            }
        )

        previous_average = average

    return rankings


# ============================================================
# CALCULATE EVERYTHING
# ============================================================

def calculate_all_positions(
    db: Session,
    academic_term_id: int,
):
    """
    Calculate subject positions for every subject
    and overall student positions.
    """

    # --------------------------------------------------------
    # Get subjects used in this term
    # --------------------------------------------------------

    subjects_query = (
        select(Result.subject_id)
        .where(
            Result.academic_term_id == academic_term_id
        )
        .distinct()
    )

    subject_ids = list(
        db.scalars(subjects_query).all()
    )

    # --------------------------------------------------------
    # Subject rankings
    # --------------------------------------------------------

    for subject_id in subject_ids:

        calculate_subject_positions(
            db,
            subject_id,
            academic_term_id,
        )

    # --------------------------------------------------------
    # Overall rankings
    # --------------------------------------------------------

    overall_rankings = calculate_overall_positions(
        db,
        academic_term_id,
    )

    return overall_rankings
