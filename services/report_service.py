# ============================================================
# EXAMINA AI
# REPORT SERVICE
# ============================================================

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import (
    Student,
    Subject,
    Result,
    AcademicTerm,
    AcademicSession,
    School,
    StudentTermReport,
)

from services.result_service import (
    calculate_overall_positions,
)


# ============================================================
# CALCULATE TERM AVERAGE
# ============================================================

def calculate_term_average(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    """
    Calculate a student's average for one term.

    Average =
        Sum of subject totals / Number of subjects
    """

    results = db.scalars(
        select(Result).where(
            Result.student_id == student_id,
            Result.academic_term_id == academic_term_id,
        )
    ).all()

    if not results:
        return 0.0

    total_score = sum(
        result.total
        for result in results
    )

    return round(
        total_score / len(results),
        2,
    )


# ============================================================
# CALCULATE YEAR AVERAGE
# ============================================================

def calculate_year_average(
    db: Session,
    student_id: int,
    academic_session_id: int,
):
    """
    Calculate the student's yearly average.

    This is only calculated when all three terms
    have results.

    Formula:

        (1st Term Average
         + 2nd Term Average
         + 3rd Term Average) / 3
    """

    # --------------------------------------------------------
    # Get all three terms
    # --------------------------------------------------------

    terms = db.scalars(
        select(AcademicTerm)
        .where(
            AcademicTerm.academic_session_id
            == academic_session_id
        )
        .order_by(
            AcademicTerm.term_number
        )
    ).all()

    # --------------------------------------------------------
    # We require exactly the three academic terms
    # --------------------------------------------------------

    if len(terms) < 3:
        return None

    term_averages = []

    for term in terms:

        average = calculate_term_average(
            db=db,
            student_id=student_id,
            academic_term_id=term.id,
        )

        # ----------------------------------------------------
        # If a student has no result for a term,
        # yearly average is not yet available.
        # ----------------------------------------------------

        results_exist = db.scalar(
            select(Result.id).where(
                Result.student_id == student_id,
                Result.academic_term_id == term.id,
            )
        )

        if results_exist is None:
            return None

        term_averages.append(
            average
        )

    # --------------------------------------------------------
    # YEAR AVERAGE
    # --------------------------------------------------------

    year_average = (
        sum(term_averages) / 3
    )

    return round(
        year_average,
        2,
    )


# ============================================================
# GET OR CREATE TERM REPORT
# ============================================================

def get_or_create_term_report(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    """
    Get the student's term report.

    If it doesn't exist, create it.
    """

    report = db.scalar(
        select(StudentTermReport).where(
            StudentTermReport.student_id
            == student_id,

            StudentTermReport.academic_term_id
            == academic_term_id,
        )
    )

    if report is None:

        report = StudentTermReport(
            student_id=student_id,
            academic_term_id=academic_term_id,
            principal_approved=False,
        )

        db.add(report)
        db.commit()
        db.refresh(report)

    return report


# ============================================================
# SAVE TEACHER'S REMARK
# ============================================================

def save_teachers_remark(
    db: Session,
    student_id: int,
    academic_term_id: int,
    remark: str,
):
    """
    Save or update the class teacher's remark.
    """

    report = get_or_create_term_report(
        db,
        student_id,
        academic_term_id,
    )

    # --------------------------------------------------------
    # Do not allow editing an approved report
    # --------------------------------------------------------

    if report.principal_approved:
        raise PermissionError(
            "This report has already been approved "
            "by the principal."
        )

    report.teachers_remark = remark

    db.commit()
    db.refresh(report)

    return report


# ============================================================
# PRINCIPAL APPROVES REPORT
# ============================================================

def approve_student_report(
    db: Session,
    student_id: int,
    academic_term_id: int,
    principals_remark: str,
    promotion_status: str | None = None,
):
    """
    Principal approves a student's complete report.

    For 3rd Term, promotion_status is required.
    """

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

    # --------------------------------------------------------
    # Don't approve twice
    # --------------------------------------------------------

    if report.principal_approved:
        raise ValueError(
            "This report has already been approved."
        )

    # --------------------------------------------------------
    # 3rd TERM
    # --------------------------------------------------------

    if term.term_number == 3:

        if promotion_status not in (
            "PROMOTED",
            "NOT_PROMOTED",
        ):
            raise ValueError(
                "A 3rd Term report must have a valid "
                "promotion status."
            )

        # ----------------------------------------------------
        # Calculate year average
        # ----------------------------------------------------

        session = db.get(
            AcademicSession,
            term.academic_session_id,
        )

        if session is None:
            raise ValueError(
                "Academic session not found."
            )

        year_average = calculate_year_average(
            db=db,
            student_id=student_id,
            academic_session_id=session.id,
        )

        if year_average is None:
            raise ValueError(
                "The student's results for all three "
                "terms are required before calculating "
                "the year average."
            )

        report.year_average = year_average

        report.promotion_status = (
            promotion_status
        )

    else:

        # ----------------------------------------------------
        # No promotion decision in 1st or 2nd Term
        # ----------------------------------------------------

        report.promotion_status = None
        report.year_average = None

    # --------------------------------------------------------
    # Principal's remark
    # --------------------------------------------------------

    report.principals_remark = (
        principals_remark
    )

    # --------------------------------------------------------
    # Approve
    # --------------------------------------------------------

    report.principal_approved = True

    report.approved_at = datetime.utcnow()

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
    """
    Build a complete ExaminA AI report card.
    """

    # ========================================================
    # GET STUDENT
    # ========================================================

    student = db.get(
        Student,
        student_id,
    )

    if student is None:
        raise ValueError(
            "Student not found."
        )

    # ========================================================
    # GET TERM
    # ========================================================

    term = db.get(
        AcademicTerm,
        academic_term_id,
    )

    if term is None:
        raise ValueError(
            "Academic term not found."
        )

    # ========================================================
    # GET SESSION
    # ========================================================

    session = db.get(
        AcademicSession,
        term.academic_session_id,
    )

    if session is None:
        raise ValueError(
            "Academic session not found."
        )

    # ========================================================
    # GET SCHOOL
    # ========================================================

    school = db.get(
        School,
        student.school_id,
    )

    if school is None:
        raise ValueError(
            "School not found."
        )

    # ========================================================
    # GET TERM REPORT
    # ========================================================

    term_report = db.scalar(
        select(StudentTermReport).where(
            StudentTermReport.student_id
            == student_id,

            StudentTermReport.academic_term_id
            == academic_term_id,
        )
    )

    # ========================================================
    # GET RESULTS
    # ========================================================

    query = (
        select(Result)
        .join(
            Subject,
            Result.subject_id
            == Subject.id,
        )
        .where(
            Result.student_id
            == student_id,

            Result.academic_term_id
            == academic_term_id,
        )
        .order_by(
            Subject.name
        )
    )

    results = list(
        db.scalars(query).all()
    )

    # ========================================================
    # SUBJECT RESULTS
    # ========================================================

    subjects = []

    for result in results:

        subjects.append(
            {
                "subject_id":
                    result.subject_id,

                "subject":
                    result.subject.name,

                "first_test":
                    result.first_test,

                "second_test":
                    result.second_test,

                "exam":
                    result.exam,

                "total":
                    result.total,

                "grade":
                    result.grade,

                "position":
                    result.position,
            }
        )

    # ========================================================
    # TERM TOTAL
    # ========================================================

    total_score = sum(
        result.total
        for result in results
    )

    subject_count = len(results)

    if subject_count > 0:

        average = round(
            total_score / subject_count,
            2,
        )

    else:

        average = 0.0

    # ========================================================
    # OVERALL CLASS POSITION
    # ========================================================

    rankings = calculate_overall_positions(
        db=db,
        school_id=student.school_id,
        class_id=student.class_id,
        academic_term_id=academic_term_id,
    )

    overall_position = None

    for item in rankings:

        if item["student"].id == student.id:

            overall_position = (
                item["position"]
            )

            break

    # ========================================================
    # YEAR AVERAGE
    # ========================================================

    year_average = None

    if term.term_number == 3:

        year_average = calculate_year_average(
            db=db,
            student_id=student_id,
            academic_session_id=session.id,
        )

    # ========================================================
    # APPROVAL STATUS
    # ========================================================

    principal_approved = False

    if term_report:

        principal_approved = (
            term_report.principal_approved
        )

    # ========================================================
    # BUILD REPORT
    # ========================================================

    return {

        # ====================================================
        # SCHOOL
        # ====================================================

        "school": {

            "name":
                school.name,

            "badge":
                school.school_badge,

            "address":
                school.address,

            "email":
                school.email,

            "phone":
                school.phone,

            "local_government":
                school.local_government,

            "state":
                school.state,
        },

        # ====================================================
        # ACADEMIC
        # ====================================================

        "academic": {

            "session":
                session.name,

            "term":
                term.name,

            "term_number":
                term.term_number,

            "curriculum_version":
                session.curriculum_version,
        },

        # ====================================================
        # STUDENT
        # ====================================================

        "student": {

            "id":
                student.id,

            "admission_number":
                student.admission_number,

            "first_name":
                student.first_name,

            "middle_name":
                student.middle_name,

            "last_name":
                student.last_name,

            "class":
                student.school_class.name,

            "education_level":
                student.education_level,

            "field":
                student.field,
        },

        # ====================================================
        # SUBJECTS
        # ====================================================

        "subjects":
            subjects,

        # ====================================================
        # SUMMARY
        # ====================================================

        "summary": {

            "total_score":
                round(
                    total_score,
                    2,
                ),

            "subject_count":
                subject_count,

            "average":
                average,

            "overall_position":
                overall_position,

            "year_average":
                year_average,
        },

        # ====================================================
        # REMARKS
        # ====================================================

        "teachers_remark": (
            term_report.teachers_remark
            if term_report
            else None
        ),

        "principals_remark": (
            term_report.principals_remark
            if term_report
            else None
        ),

        # ====================================================
        # THIRD TERM PROMOTION
        # ====================================================

        "promotion_status": (
            term_report.promotion_status
            if term_report
            else None
        ),

        # ====================================================
        # APPROVAL
        # ====================================================

        "principal_approved":
            principal_approved,

        "approved_at": (
            term_report.approved_at
            if term_report
            else None
        ),
    }


# ============================================================
# DOWNLOAD CHECK
# ============================================================

def can_download_report(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    """
    Determine whether a student report can be downloaded.

    Download is allowed ONLY after principal approval.
    """

    report = db.scalar(
        select(StudentTermReport).where(
            StudentTermReport.student_id
            == student_id,

            StudentTermReport.academic_term_id
            == academic_term_id,
        )
    )

    if report is None:
        return False

    return report.principal_approved


# ============================================================
# REQUIRE APPROVAL BEFORE DOWNLOAD
# ============================================================

def require_report_approval(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    """
    Stop report generation/download if the principal
    has not approved the report.
    """

    if not can_download_report(
        db,
        student_id,
        academic_term_id,
    ):

        raise PermissionError(
            "This report cannot be downloaded yet. "
            "The principal has not approved it."
        )

    return True
