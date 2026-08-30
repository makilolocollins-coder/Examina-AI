# ============================================================
# EXAMINA AI
# REPORT SERVICE
# ============================================================

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import (
    AcademicSession,
    AcademicTerm,
    Result,
    School,
    Student,
    StudentTermReport,
    Subject,
)
from services.result_service import calculate_overall_positions


# ============================================================
# GET / CREATE TERM REPORT
# ============================================================

def get_or_create_term_report(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    report = db.scalar(
        select(StudentTermReport).where(
            StudentTermReport.student_id == student_id,
            StudentTermReport.academic_term_id == academic_term_id,
        )
    )

    if report is None:
        report = StudentTermReport(
            student_id=student_id,
            academic_term_id=academic_term_id,
            principal_approved=False,
            published=False,
        )

        db.add(report)
        db.commit()
        db.refresh(report)

    return report


# ============================================================
# TERM AVERAGE
# ============================================================

def calculate_term_average(
    db: Session,
    student_id: int,
    academic_term_id: int,
) -> float:

    results = db.scalars(
        select(Result).where(
            Result.student_id == student_id,
            Result.academic_term_id == academic_term_id,
        )
    ).all()

    if not results:
        return 0.0

    valid_results = [
        result
        for result in results
        if result.total is not None
    ]

    if not valid_results:
        return 0.0

    total = sum(
        float(result.total)
        for result in valid_results
    )

    return round(
        total / len(valid_results),
        2,
    )


# ============================================================
# YEAR AVERAGE
# ============================================================

def calculate_year_average(
    db: Session,
    student_id: int,
    academic_session_id: int,
):

    terms = db.scalars(
        select(AcademicTerm)
        .where(
            AcademicTerm.academic_session_id
            == academic_session_id
        )
        .order_by(AcademicTerm.term_number)
    ).all()

    if len(terms) < 3:
        return None

    averages = []

    for term in terms[:3]:

        results = db.scalars(
            select(Result).where(
                Result.student_id == student_id,
                Result.academic_term_id == term.id,
            )
        ).all()

        if not results:
            return None

        average = calculate_term_average(
            db,
            student_id,
            term.id,
        )

        averages.append(average)

    if len(averages) != 3:
        return None

    return round(
        sum(averages) / 3,
        2,
    )


# ============================================================
# TEACHER REMARK
# ============================================================

def save_teachers_remark(
    db: Session,
    student_id: int,
    academic_term_id: int,
    remark: str,
):

    report = get_or_create_term_report(
        db,
        student_id,
        academic_term_id,
    )

    if report.principal_approved:
        raise PermissionError(
            "This report has already been approved by the principal."
        )

    report.teachers_remark = (
        remark.strip()
        if remark
        else None
    )

    db.commit()
    db.refresh(report)

    return report


# ============================================================
# PRINCIPAL APPROVAL
# ============================================================

def approve_student_report(
    db: Session,
    student_id: int,
    academic_term_id: int,
    principal_remark: str,
    promotion_status: str | None = None,
    principal_id: int | None = None,
):

    report = get_or_create_term_report(
        db,
        student_id,
        academic_term_id,
    )

    term = db.get(
        AcademicTerm,
        academic_term_id,
    )

    if term is None:
        raise ValueError(
            "Academic term not found."
        )

    if report.principal_approved:
        raise ValueError(
            "This report has already been approved."
        )

    # --------------------------------------------------------
    # THIRD TERM
    # --------------------------------------------------------

    if term.term_number == 3:

        if promotion_status not in {
            "PROMOTED",
            "NOT_PROMOTED",
        }:
            raise ValueError(
                "Third Term requires a valid promotion status."
            )

        year_average = calculate_year_average(
            db,
            student_id,
            term.academic_session_id,
        )

        if year_average is None:
            raise ValueError(
                "Results for all three terms are required "
                "before calculating the year average."
            )

        report.year_average = year_average
        report.promotion_status = promotion_status

    else:

        report.year_average = None
        report.promotion_status = None

    # --------------------------------------------------------
    # APPROVAL
    # --------------------------------------------------------

    report.principal_remark = (
        principal_remark.strip()
        if principal_remark
        else None
    )

    report.principal_approved = True
    report.principal_id = principal_id
    report.approved_at = datetime.utcnow()

    db.commit()
    db.refresh(report)

    return report


# ============================================================
# PUBLISH REPORT
# ============================================================

def publish_report(
    db: Session,
    student_id: int,
    academic_term_id: int,
):

    report = get_or_create_term_report(
        db,
        student_id,
        academic_term_id,
    )

    if not report.principal_approved:
        raise PermissionError(
            "The report must be approved by the principal before publication."
        )

    report.published = True

    db.commit()
    db.refresh(report)

    return report


# ============================================================
# UNPUBLISH REPORT
# ============================================================

def unpublish_report(
    db: Session,
    student_id: int,
    academic_term_id: int,
):

    report = get_or_create_term_report(
        db,
        student_id,
        academic_term_id,
    )

    report.published = False

    db.commit()
    db.refresh(report)

    return report


# ============================================================
# BUILD STUDENT REPORT
# ============================================================

def build_student_report(
    db: Session,
    student_id: int,
    academic_term_id: int,
):

    student = db.get(
        Student,
        student_id,
    )

    if student is None:
        raise ValueError(
            "Student not found."
        )

    term = db.get(
        AcademicTerm,
        academic_term_id,
    )

    if term is None:
        raise ValueError(
            "Academic term not found."
        )

    academic_session = db.get(
        AcademicSession,
        term.academic_session_id,
    )

    if academic_session is None:
        raise ValueError(
            "Academic session not found."
        )

    school = db.get(
        School,
        student.school_id,
    )

    if school is None:
        raise ValueError(
            "School not found."
        )

    report = get_or_create_term_report(
        db,
        student_id,
        academic_term_id,
    )

    results = db.scalars(
        select(Result)
        .join(
            Subject,
            Result.subject_id == Subject.id,
        )
        .where(
            Result.student_id == student_id,
            Result.academic_term_id == academic_term_id,
        )
        .order_by(Subject.name)
    ).all()

    subjects = []

    for result in results:

        subjects.append(
            {
                "subject_id": result.subject_id,
                "subject": result.subject.name,
                "first_test": result.first_test,
                "second_test": result.second_test,
                "exam": result.exam,
                "total": result.total,
                "grade": result.grade,
                "position": result.position,
            }
        )

    valid_results = [
        result
        for result in results
        if result.total is not None
    ]

    total_score = sum(
        float(result.total)
        for result in valid_results
    )

    subject_count = len(valid_results)

    average = (
        round(
            total_score / subject_count,
            2,
        )
        if subject_count
        else 0.0
    )

    # --------------------------------------------------------
    # OVERALL POSITION
    # --------------------------------------------------------

    rankings = calculate_overall_positions(
        db=db,
        school_id=student.school_id,
        class_id=student.class_id,
        academic_term_id=academic_term_id,
    )

    overall_position = None

    for item in rankings:

        ranked_student = item.get("student")

        if ranked_student is not None:
            if ranked_student.id == student.id:
                overall_position = item.get("position")
                break

    # --------------------------------------------------------
    # YEAR AVERAGE
    # --------------------------------------------------------

    year_average = None

    if term.term_number == 3:

        year_average = calculate_year_average(
            db,
            student_id,
            academic_session.id,
        )

    return {
        "school": {
            "name": school.name,
            "badge": school.school_badge,
            "address": school.address,
            "email": school.email,
            "phone": school.phone,
            "local_government": school.local_government,
            "state": school.state,
        },

        "academic": {
            "session": academic_session.name,
            "term": term.name,
            "term_number": term.term_number,
            "curriculum_version": (
                academic_session.curriculum_version
            ),
        },

        "student": {
            "id": student.id,
            "admission_number": student.admission_number,
            "first_name": student.first_name,
            "middle_name": student.middle_name,
            "last_name": student.last_name,
            "class": student.school_class.name,
            "education_level": student.education_level,
            "field": student.field,
        },

        "subjects": subjects,

        "summary": {
            "total_score": round(
                total_score,
                2,
            ),
            "subject_count": subject_count,
            "average": average,
            "overall_position": overall_position,
            "year_average": year_average,
        },

        "teachers_remark": report.teachers_remark,
        "principal_remark": report.principal_remark,
        "principal_approved": report.principal_approved,
        "approved_at": report.approved_at,
        "promotion_status": report.promotion_status,
        "published": report.published,
    }


# ============================================================
# DOWNLOAD CHECK
# ============================================================

def can_download_report(
    db: Session,
    student_id: int,
    academic_term_id: int,
):

    report = db.scalar(
        select(StudentTermReport).where(
            StudentTermReport.student_id == student_id,
            StudentTermReport.academic_term_id
            == academic_term_id,
        )
    )

    if report is None:
        return False

    return bool(
        report.principal_approved
        and report.published
    )


# ============================================================
# REQUIRE DOWNLOAD PERMISSION
# ============================================================

def require_report_approval(
    db: Session,
    student_id: int,
    academic_term_id: int,
):

    if not can_download_report(
        db,
        student_id,
        academic_term_id,
    ):
        raise PermissionError(
            "This report cannot be downloaded until "
            "it has been approved and published by "
            "the principal."
        )

    return True
