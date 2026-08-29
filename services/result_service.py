# ============================================================
# EXAMINA AI
# RESULT SERVICE
# ============================================================

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from database import (
    Student,
    Subject,
    Result,
)


# ============================================================
# GRADE CONFIGURATION
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

    return "F"


# ============================================================
# CALCULATE RESULT TOTAL
# ============================================================

def calculate_total(
    first_test: float,
    second_test: float,
    exam: float,
) -> float:
    """
    Calculate total score.

    Total =
        First Test
        + Second Test
        + Exam
    """

    total = (
        float(first_test)
        + float(second_test)
        + float(exam)
    )

    return round(total, 2)


# ============================================================
# UPDATE ONE RESULT
# ============================================================

def update_result(
    db: Session,
    result_id: int,
    first_test: float,
    second_test: float,
    exam: float,
):
    """
    Update a student's result.

    Automatically calculates:
        total
        grade
    """

    result = db.get(
        Result,
        result_id,
    )

    if result is None:
        raise ValueError(
            f"Result with ID {result_id} was not found."
        )

    # --------------------------------------------------------
    # Validate scores
    # --------------------------------------------------------

    if first_test < 0:
        raise ValueError(
            "First test score cannot be negative."
        )

    if second_test < 0:
        raise ValueError(
            "Second test score cannot be negative."
        )

    if exam < 0:
        raise ValueError(
            "Exam score cannot be negative."
        )

    # --------------------------------------------------------
    # Save scores
    # --------------------------------------------------------

    result.first_test = float(first_test)
    result.second_test = float(second_test)
    result.exam = float(exam)

    # --------------------------------------------------------
    # Calculate total
    # --------------------------------------------------------

    result.total = calculate_total(
        first_test=first_test,
        second_test=second_test,
        exam=exam,
    )

    # --------------------------------------------------------
    # Calculate grade
    # --------------------------------------------------------

    result.grade = calculate_grade(
        result.total
    )

    db.commit()

    db.refresh(result)

    return result


# ============================================================
# CREATE RESULT
# ============================================================

def create_result(
    db: Session,
    student_id: int,
    subject_id: int,
    academic_term_id: int,
    first_test: float = 0.0,
    second_test: float = 0.0,
    exam: float = 0.0,
):
    """
    Create a new result for:

        Student
        Subject
        Academic Term
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
    # Prevent duplicate result
    # --------------------------------------------------------

    existing = db.scalar(
        select(Result).where(
            Result.student_id == student_id,
            Result.subject_id == subject_id,
            Result.academic_term_id == academic_term_id,
        )
    )

    if existing is not None:
        raise ValueError(
            "A result already exists for this "
            "student, subject and academic term."
        )

    # --------------------------------------------------------
    # Calculate total
    # --------------------------------------------------------

    total = calculate_total(
        first_test,
        second_test,
        exam,
    )

    # --------------------------------------------------------
    # Create result
    # --------------------------------------------------------

    result = Result(
        student_id=student_id,
        subject_id=subject_id,
        academic_term_id=academic_term_id,
        first_test=float(first_test),
        second_test=float(second_test),
        exam=float(exam),
        total=total,
        grade=calculate_grade(total),
    )

    db.add(result)

    db.commit()

    db.refresh(result)

    return result


# ============================================================
# GET STUDENT RESULTS
# ============================================================

def get_student_results(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    """
    Get all results belonging to one student
    in one academic term.
    """

    query = (
        select(Result)
        .where(
            Result.student_id == student_id,
            Result.academic_term_id == academic_term_id,
        )
        .order_by(
            Result.subject_id
        )
    )

    return list(
        db.scalars(query).all()
    )


# ============================================================
# CALCULATE STUDENT TOTAL
# ============================================================

def calculate_student_total(
    db: Session,
    student_id: int,
    academic_term_id: int,
) -> float:
    """
    Add all subject totals for one student
    during one academic term.
    """

    result = db.scalar(
        select(
            func.coalesce(
                func.sum(Result.total),
                0,
            )
        ).where(
            Result.student_id == student_id,
            Result.academic_term_id == academic_term_id,
        )
    )

    return round(
        float(result or 0),
        2,
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
    Calculate average score across the subjects
    for one student in one academic term.

    Example:

        Mathematics = 80
        Chemistry  = 70
        Physics    = 90

        Average = 80
    """

    results = get_student_results(
        db=db,
        student_id=student_id,
        academic_term_id=academic_term_id,
    )

    if not results:
        return 0.0

    total = sum(
        float(result.total)
        for result in results
    )

    average = total / len(results)

    return round(
        average,
        2,
    )


# ============================================================
# CALCULATE SUBJECT POSITIONS
# ============================================================

def calculate_subject_positions(
    db: Session,
    subject_id: int,
    academic_term_id: int,
    school_id: int,
    class_id: int,
):
    """
    Rank students in one subject.

    Ranking is restricted to:

        SAME SCHOOL
        SAME CLASS
        SAME ACADEMIC TERM

    Highest score = Position 1.

    Students with equal scores receive
    the same position.
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
            Student.school_id == school_id,
            Student.class_id == class_id,
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

    for index, result in enumerate(
        results,
        start=1,
    ):

        current_score = float(
            result.total
        )

        # ----------------------------------------------------
        # Competition ranking
        #
        # 95 → 1st
        # 95 → 1st
        # 90 → 3rd
        # ----------------------------------------------------

        if (
            previous_score is None
            or current_score != previous_score
        ):
            position = index

        result.position = position

        previous_score = current_score

    db.commit()

    return results


# ============================================================
# CALCULATE OVERALL POSITIONS
# ============================================================

def calculate_overall_positions(
    db: Session,
    academic_term_id: int,
    school_id: int,
    class_id: int,
):
    """
    Rank students according to their overall
    average.

    Ranking is restricted to:

        SAME SCHOOL
        SAME CLASS
        SAME ACADEMIC TERM

    Highest average = Position 1.
    """

    # --------------------------------------------------------
    # Get students in this school and class
    # --------------------------------------------------------

    students_query = (
        select(Student)
        .where(
            Student.school_id == school_id,
            Student.class_id == class_id,
            Student.active.is_(True),
        )
        .order_by(
            Student.last_name,
            Student.first_name,
        )
    )

    students = list(
        db.scalars(
            students_query
        ).all()
    )

    rankings = []

    # --------------------------------------------------------
    # Calculate average for every student
    # --------------------------------------------------------

    for student in students:

        results = get_student_results(
            db=db,
            student_id=student.id,
            academic_term_id=academic_term_id,
        )

        # ----------------------------------------------------
        # Ignore students without results
        # ----------------------------------------------------

        if not results:
            continue

        total = sum(
            float(result.total)
            for result in results
        )

        subject_count = len(results)

        average = total / subject_count

        rankings.append(
            {
                "student_id": student.id,
                "student_name": (
                    f"{student.first_name} "
                    f"{student.middle_name + ' ' if student.middle_name else ''}"
                    f"{student.last_name}"
                ),
                "total": round(
                    total,
                    2,
                ),
                "subjects": subject_count,
                "average": round(
                    average,
                    2,
                ),
            }
        )

    # --------------------------------------------------------
    # Highest average first
    # --------------------------------------------------------

    rankings.sort(
        key=lambda item: item["average"],
        reverse=True,
    )

    # --------------------------------------------------------
    # Assign positions
    # --------------------------------------------------------

    previous_average = None
    position = 0

    for index, student in enumerate(
        rankings,
        start=1,
    ):

        current_average = student[
            "average"
        ]

        if (
            previous_average is None
            or current_average != previous_average
        ):
            position = index

        student["position"] = position

        previous_average = current_average

    return rankings


# ============================================================
# CALCULATE ALL POSITIONS
# ============================================================

def calculate_all_positions(
    db: Session,
    academic_term_id: int,
    school_id: int,
    class_id: int,
):
    """
    Calculate:

        1. Subject positions
        2. Overall class positions

    Everything is restricted to:

        School
        Class
        Academic Term
    """

    # --------------------------------------------------------
    # Find subjects used by this class and term
    # --------------------------------------------------------

    subjects_query = (
        select(
            Result.subject_id
        )
        .join(
            Student,
            Result.student_id == Student.id,
        )
        .where(
            Result.academic_term_id
            == academic_term_id,

            Student.school_id
            == school_id,

            Student.class_id
            == class_id,

            Student.active.is_(True),
        )
        .distinct()
    )

    subject_ids = list(
        db.scalars(
            subjects_query
        ).all()
    )

    # --------------------------------------------------------
    # Calculate each subject's positions
    # --------------------------------------------------------

    for subject_id in subject_ids:

        calculate_subject_positions(
            db=db,
            subject_id=subject_id,
            academic_term_id=academic_term_id,
            school_id=school_id,
            class_id=class_id,
        )

    # --------------------------------------------------------
    # Calculate overall positions
    # --------------------------------------------------------

    overall_rankings = (
        calculate_overall_positions(
            db=db,
            academic_term_id=academic_term_id,
            school_id=school_id,
            class_id=class_id,
        )
    )

    return overall_rankings


# ============================================================
# GET COMPLETE CLASS RESULTS
# ============================================================

def get_class_results(
    db: Session,
    academic_term_id: int,
    school_id: int,
    class_id: int,
):
    """
    Return a complete result sheet for a class.

    Includes:

        Student
        Subjects
        Test scores
        Exam
        Total
        Grade
        Subject position
        Overall average
        Overall position
    """

    # --------------------------------------------------------
    # Calculate positions first
    # --------------------------------------------------------

    rankings = calculate_all_positions(
        db=db,
        academic_term_id=academic_term_id,
        school_id=school_id,
        class_id=class_id,
    )

    # --------------------------------------------------------
    # Create quick lookup
    # --------------------------------------------------------

    ranking_lookup = {
        item["student_id"]: item
        for item in rankings
    }

    # --------------------------------------------------------
    # Get students
    # --------------------------------------------------------

    students_query = (
        select(Student)
        .where(
            Student.school_id == school_id,
            Student.class_id == class_id,
            Student.active.is_(True),
        )
        .order_by(
            Student.last_name,
            Student.first_name,
        )
    )

    students = list(
        db.scalars(
            students_query
        ).all()
    )

    output = []

    # --------------------------------------------------------
    # Build result sheet
    # --------------------------------------------------------

    for student in students:

        student_results = get_student_results(
            db=db,
            student_id=student.id,
            academic_term_id=academic_term_id,
        )

        ranking = ranking_lookup.get(
            student.id
        )

        subjects = []

        for result in student_results:

            subject = db.get(
                Subject,
                result.subject_id,
            )

            subjects.append(
                {
                    "subject_id": result.subject_id,
                    "subject": (
                        subject.name
                        if subject
                        else "Unknown"
                    ),
                    "first_test": result.first_test,
                    "second_test": result.second_test,
                    "exam": result.exam,
                    "total": result.total,
                    "grade": result.grade,
                    "position": result.position,
                }
            )

        output.append(
            {
                "student_id": student.id,

                "admission_number":
                    student.admission_number,

                "student_name": (
                    f"{student.first_name} "
                    f"{student.middle_name + ' ' if student.middle_name else ''}"
                    f"{student.last_name}"
                ),

                "subjects": subjects,

                "total": (
                    ranking["total"]
                    if ranking
                    else 0
                ),

                "average": (
                    ranking["average"]
                    if ranking
                    else 0
                ),

                "overall_position": (
                    ranking["position"]
                    if ranking
                    else None
                ),
            }
        )

    # --------------------------------------------------------
    # Highest average first
    # --------------------------------------------------------

    output.sort(
        key=lambda item: (
            item["average"]
            if item["average"] is not None
            else 0
        ),
        reverse=True,
    )

    return output


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
    during a particular academic term.
    """

    query = (
        select(Result)
        .join(
            Subject,
            Result.subject_id == Subject.id,
        )
        .where(
            Result.student_id == student_id,
            Result.academic_term_id == academic_term_id,
        )
        .order_by(
            Subject.name
        )
    )

    return list(
        db.scalars(
            query
        ).all()
    )
