# ============================================================
# EXAMINA AI
# RESULT SERVICE
# ============================================================
#
# Handles:
#
# 1. Total score calculation
# 2. Grade calculation
# 3. Subject positions
# 4. Overall class positions
# 5. Student average
# 6. 3rd-term year average
#
# Ranking is always performed inside:
#
#       SCHOOL
#       CLASS
#       TERM
#
# ============================================================

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import (
    AcademicTerm,
    Result,
    Student,
    Subject,
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

    elif total >= 60:
        return "B"

    elif total >= 50:
        return "C"

    elif total >= 45:
        return "D"

    elif total >= 40:
        return "E"

    else:
        return "F"


# ============================================================
# CALCULATE RESULT TOTAL
# ============================================================

def calculate_result_total(
    first_test: float,
    second_test: float,
    exam: float,
) -> float:
    """
    Calculate the total score.

    Example:

        First Test  = 20
        Second Test = 20
        Exam        = 60

        Total = 100
    """

    total = (
        first_test
        + second_test
        + exam
    )

    return round(total, 2)


# ============================================================
# UPDATE SINGLE RESULT
# ============================================================

def update_result(
    db: Session,
    result: Result,
):
    """
    Calculate and save the total and grade
    for one student's subject result.
    """

    result.total = calculate_result_total(
        first_test=result.first_test,
        second_test=result.second_test,
        exam=result.exam,
    )

    result.grade = calculate_grade(
        result.total
    )

    db.add(result)

    db.commit()

    db.refresh(result)

    return result


# ============================================================
# GET TERM RESULTS
# ============================================================

def get_term_results(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    """
    Get all subject results belonging to
    one student during one term.
    """

    query = (
        select(Result)
        .where(
            Result.student_id == student_id,
            Result.academic_term_id
            == academic_term_id,
        )
        .order_by(Result.subject_id)
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
) -> float:
    """
    Calculate a student's average for one term.

    Average =
        Sum of subject totals
        ---------------------
        Number of subjects
    """

    results = get_term_results(
        db=db,
        student_id=student_id,
        academic_term_id=academic_term_id,
    )

    if not results:
        return 0.0

    total_score = sum(
        result.total
        for result in results
    )

    average = (
        total_score / len(results)
    )

    return round(average, 2)


# ============================================================
# CALCULATE SUBJECT POSITIONS
# ============================================================

def calculate_subject_positions(
    db: Session,
    subject_id: int,
    academic_term_id: int,
):
    """
    Rank students in one subject.

    Students are ranked only inside the same:

        School
        Class
        Term
        Subject

    Ties receive the same position.

    Example:

        Student A = 90 → 1
        Student B = 90 → 1
        Student C = 80 → 3
    """

    query = (
        select(Result)
        .join(
            Student,
            Result.student_id
            == Student.id,
        )
        .where(
            Result.subject_id == subject_id,
            Result.academic_term_id
            == academic_term_id,
            Student.active == True,
        )
        .order_by(
            Result.total.desc()
        )
    )

    results = list(
        db.scalars(query).all()
    )

    # --------------------------------------------------------
    # GROUP BY SCHOOL AND CLASS
    # --------------------------------------------------------

    groups = {}

    for result in results:

        key = (
            result.student.school_id,
            result.student.class_id,
        )

        if key not in groups:
            groups[key] = []

        groups[key].append(result)

    # --------------------------------------------------------
    # RANK EACH GROUP
    # --------------------------------------------------------

    for group_results in groups.values():

        previous_score = None
        position = 0

        for index, result in enumerate(
            group_results,
            start=1,
        ):

            if (
                previous_score is None
                or result.total
                != previous_score
            ):
                position = index

            result.position = position

            previous_score = result.total

            db.add(result)

    db.commit()

    return results


# ============================================================
# CALCULATE OVERALL POSITIONS
# ============================================================

def calculate_overall_positions(
    db: Session,
    school_id: int,
    class_id: int,
    academic_term_id: int,
):
    """
    Rank all active students inside:

        ONE SCHOOL
        ONE CLASS
        ONE TERM

    Ranking is based on average score.
    """

    students_query = (
        select(Student)
        .where(
            Student.school_id == school_id,
            Student.class_id == class_id,
            Student.active == True,
        )
    )

    students = list(
        db.scalars(
            students_query
        ).all()
    )

    ranking = []

    # --------------------------------------------------------
    # CALCULATE EACH STUDENT'S AVERAGE
    # --------------------------------------------------------

    for student in students:

        average = calculate_student_average(
            db=db,
            student_id=student.id,
            academic_term_id=academic_term_id,
        )

        ranking.append(
            {
                "student": student,
                "average": average,
            }
        )

    # --------------------------------------------------------
    # HIGHEST AVERAGE FIRST
    # --------------------------------------------------------

    ranking.sort(
        key=lambda item: item["average"],
        reverse=True,
    )

    # --------------------------------------------------------
    # ASSIGN POSITIONS
    # --------------------------------------------------------

    previous_average = None
    position = 0

    for index, item in enumerate(
        ranking,
        start=1,
    ):

        if (
            previous_average is None
            or item["average"]
            != previous_average
        ):
            position = index

        item["position"] = position

        previous_average = item["average"]

    return ranking


# ============================================================
# SAVE OVERALL POSITIONS
# ============================================================

def save_overall_positions(
    db: Session,
    school_id: int,
    class_id: int,
    academic_term_id: int,
):
    """
    Calculate the overall ranking and save
    the position into each student's Result records.
    """

    ranking = calculate_overall_positions(
        db=db,
        school_id=school_id,
        class_id=class_id,
        academic_term_id=academic_term_id,
    )

    for item in ranking:

        student = item["student"]

        position = item["position"]

        results = get_term_results(
            db=db,
            student_id=student.id,
            academic_term_id=academic_term_id,
        )

        for result in results:

            result.position = position

            db.add(result)

    db.commit()

    return ranking


# ============================================================
# GET PREVIOUS TERM AVERAGE
# ============================================================

def get_term_average(
    db: Session,
    student_id: int,
    academic_term_id: int,
) -> float:
    """
    Return a student's average for a specific term.
    """

    return calculate_student_average(
        db=db,
        student_id=student_id,
        academic_term_id=academic_term_id,
    )


# ============================================================
# CALCULATE YEAR AVERAGE
# ============================================================

def calculate_year_average(
    db: Session,
    student_id: int,
    academic_session_id: int,
) -> float | None:
    """
    Calculate the yearly average.

    Used primarily for 3rd Term.

    Formula:

        1st Term Average
              +
        2nd Term Average
              +
        3rd Term Average
        -----------------
                3

    Example:

        1st Term = 70
        2nd Term = 75
        3rd Term = 80

        Year Average =
            (70 + 75 + 80) / 3

        = 75
    """

    # --------------------------------------------------------
    # GET ALL THREE TERMS
    # --------------------------------------------------------

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

    terms = list(
        db.scalars(query).all()
    )

    if len(terms) < 3:
        return None

    # --------------------------------------------------------
    # GET EACH TERM AVERAGE
    # --------------------------------------------------------

    averages = []

    for term in terms[:3]:

        average = calculate_student_average(
            db=db,
            student_id=student_id,
            academic_term_id=term.id,
        )

        averages.append(average)

    # --------------------------------------------------------
    # CALCULATE YEAR AVERAGE
    # --------------------------------------------------------

    year_average = (
        sum(averages) / 3
    )

    return round(
        year_average,
        2,
    )


# ============================================================
# GET COMPLETE STUDENT TERM SUMMARY
# ============================================================

def get_student_term_summary(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    """
    Return a student's complete term summary.
    """

    term = db.get(
        AcademicTerm,
        academic_term_id,
    )

    if term is None:
        raise ValueError(
            "Academic term not found."
        )

    student = db.get(
        Student,
        student_id,
    )

    if student is None:
        raise ValueError(
            "Student not found."
        )

    average = calculate_student_average(
        db=db,
        student_id=student_id,
        academic_term_id=academic_term_id,
    )

    ranking = calculate_overall_positions(
        db=db,
        school_id=student.school_id,
        class_id=student.class_id,
        academic_term_id=academic_term_id,
    )

    position = None

    for item in ranking:

        if item["student"].id == student_id:

            position = item["position"]

            break

    # --------------------------------------------------------
    # YEAR AVERAGE
    # --------------------------------------------------------

    year_average = None

    # Determine whether this is 3rd term.
    if term.name == "3rd Term":

        year_average = calculate_year_average(
            db=db,
            student_id=student_id,
            academic_session_id=
                term.academic_session_id,
        )

    # --------------------------------------------------------
    # RETURN SUMMARY
    # --------------------------------------------------------

    return {

        "student_id":
            student_id,

        "academic_term_id":
            academic_term_id,

        "term":
            term.name,

        "average":
            average,

        "position":
            position,

        "year_average":
            year_average,
    }
