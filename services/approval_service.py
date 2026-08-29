# ============================================================
# EXAMINA AI
# PRINCIPAL APPROVAL SERVICE
# ============================================================
#
# Handles:
#
# 1. Checking result approval status
# 2. Principal approval
# 3. Principal rejection
# 4. Principal remarks
# 5. 3rd-term PASS / FAIL decision
# 6. Student download permission
#
# ============================================================

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import (
    AcademicTerm,
    Result,
    Student,
    Teacher,
)


# ============================================================
# CHECK PRINCIPAL
# ============================================================

def verify_principal(
    db: Session,
    principal_id: int,
    school_id: int,
):
    """
    Verify that the user approving a result belongs
    to the same school.

    IMPORTANT:
    At this stage Principal is represented by a Teacher.

    Later we can create a dedicated Principal model
    and role-based authentication.
    """

    principal = db.get(
        Teacher,
        principal_id,
    )

    if principal is None:
        raise ValueError(
            "Principal account not found."
        )

    if principal.school_id != school_id:
        raise PermissionError(
            "This principal does not belong to this school."
        )

    if not principal.verified:
        raise PermissionError(
            "Principal account has not been verified."
        )

    return principal


# ============================================================
# CHECK RESULT EXISTS
# ============================================================

def get_student_term_results(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    """
    Get all results for a student in a particular term.
    """

    query = (
        select(Result)
        .where(
            Result.student_id == student_id,
            Result.academic_term_id
            == academic_term_id,
        )
    )

    return list(
        db.scalars(query).all()
    )


# ============================================================
# APPROVE STUDENT RESULT
# ============================================================

def approve_student_result(
    db: Session,
    student_id: int,
    academic_term_id: int,
    principal_id: int,
    principal_remark: str | None = None,
):
    """
    Approve all subject results for one student
    in one academic term.

    Once approved, the student is allowed to
    download the result.
    """

    # --------------------------------------------------------
    # GET STUDENT
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
    # VERIFY PRINCIPAL
    # --------------------------------------------------------

    verify_principal(
        db=db,
        principal_id=principal_id,
        school_id=student.school_id,
    )

    # --------------------------------------------------------
    # GET TERM
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
    # GET RESULTS
    # --------------------------------------------------------

    results = get_student_term_results(
        db=db,
        student_id=student_id,
        academic_term_id=academic_term_id,
    )

    if not results:
        raise ValueError(
            "This student has no results for this term."
        )

    # --------------------------------------------------------
    # CHECK IF ALREADY APPROVED
    # --------------------------------------------------------

    if all(
        result.principal_approved
        for result in results
    ):
        raise ValueError(
            "This result has already been approved."
        )

    # --------------------------------------------------------
    # APPROVE RESULTS
    # --------------------------------------------------------

    approval_time = datetime.utcnow()

    for result in results:

        result.principal_approved = True

        result.principal_approved_at = (
            approval_time
        )

        result.principal_id = principal_id

        result.principal_remark = (
            principal_remark
        )

        db.add(result)

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    db.commit()

    return {
        "success": True,
        "student_id": student_id,
        "academic_term_id": academic_term_id,
        "approved": True,
        "approved_at": approval_time,
        "principal_id": principal_id,
    }


# ============================================================
# REJECT RESULT
# ============================================================

def reject_student_result(
    db: Session,
    student_id: int,
    academic_term_id: int,
    principal_id: int,
    principal_remark: str,
):
    """
    Reject a student's result.

    Rejection keeps the result locked.

    The teacher can correct the result and submit
    it again for principal approval.
    """

    if not principal_remark.strip():

        raise ValueError(
            "A reason must be provided when rejecting a result."
        )

    # --------------------------------------------------------
    # GET STUDENT
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
    # VERIFY PRINCIPAL
    # --------------------------------------------------------

    verify_principal(
        db=db,
        principal_id=principal_id,
        school_id=student.school_id,
    )

    # --------------------------------------------------------
    # GET RESULTS
    # --------------------------------------------------------

    results = get_student_term_results(
        db=db,
        student_id=student_id,
        academic_term_id=academic_term_id,
    )

    if not results:

        raise ValueError(
            "This student has no results for this term."
        )

    # --------------------------------------------------------
    # KEEP RESULT UNAPPROVED
    # --------------------------------------------------------

    for result in results:

        result.principal_approved = False

        result.principal_approved_at = None

        result.principal_id = principal_id

        result.principal_remark = (
            principal_remark
        )

        db.add(result)

    db.commit()

    return {
        "success": True,
        "student_id": student_id,
        "academic_term_id": academic_term_id,
        "approved": False,
        "principal_id": principal_id,
        "remark": principal_remark,
    }


# ============================================================
# CHECK DOWNLOAD PERMISSION
# ============================================================

def can_download_result(
    db: Session,
    student_id: int,
    academic_term_id: int,
) -> bool:
    """
    Determine whether a student is allowed to
    download a report.

    ALL subject results must be approved.

    If even one result is not approved,
    downloading is blocked.
    """

    results = get_student_term_results(
        db=db,
        student_id=student_id,
        academic_term_id=academic_term_id,
    )

    if not results:
        return False

    return all(
        result.principal_approved
        for result in results
    )


# ============================================================
# GET APPROVAL STATUS
# ============================================================

def get_approval_status(
    db: Session,
    student_id: int,
    academic_term_id: int,
):
    """
    Return the approval status of a student's
    complete term result.
    """

    results = get_student_term_results(
        db=db,
        student_id=student_id,
        academic_term_id=academic_term_id,
    )

    if not results:

        return {
            "has_results": False,
            "approved": False,
        }

    approved_count = sum(
        1
        for result in results
        if result.principal_approved
    )

    total_results = len(results)

    fully_approved = (
        approved_count == total_results
    )

    return {

        "has_results":
            True,

        "approved":
            fully_approved,

        "approved_subjects":
            approved_count,

        "total_subjects":
            total_results,

        "pending_subjects":
            total_results - approved_count,
    }


# ============================================================
# GET RESULTS FOR PRINCIPAL
# ============================================================

def get_school_results_for_principal(
    db: Session,
    school_id: int,
    academic_term_id: int,
):
    """
    Return all student results belonging to
    a school for a particular term.

    This will power the Principal Portal.
    """

    query = (
        select(Result)
        .join(
            Student,
            Result.student_id
            == Student.id,
        )
        .where(
            Student.school_id == school_id,
            Result.academic_term_id
            == academic_term_id,
        )
        .order_by(
            Student.class_id,
            Student.last_name,
            Student.first_name,
        )
    )

    return list(
        db.scalars(query).all()
    )


# ============================================================
# PRINCIPAL APPROVE ENTIRE CLASS
# ============================================================

def approve_class_results(
    db: Session,
    school_id: int,
    class_id: int,
    academic_term_id: int,
    principal_id: int,
):
    """
    Approve all student results in a class.

    This will be useful for the Principal Portal.
    """

    # --------------------------------------------------------
    # VERIFY PRINCIPAL
    # --------------------------------------------------------

    verify_principal(
        db=db,
        principal_id=principal_id,
        school_id=school_id,
    )

    # --------------------------------------------------------
    # GET STUDENTS
    # --------------------------------------------------------

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

    if not students:

        raise ValueError(
            "No active students found in this class."
        )

    # --------------------------------------------------------
    # APPROVE EACH STUDENT
    # --------------------------------------------------------

    approved_students = 0

    for student in students:

        results = get_student_term_results(
            db=db,
            student_id=student.id,
            academic_term_id=academic_term_id,
        )

        if not results:
            continue

        approval_time = datetime.utcnow()

        for result in results:

            result.principal_approved = True

            result.principal_approved_at = (
                approval_time
            )

            result.principal_id = principal_id

            db.add(result)

        approved_students += 1

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    db.commit()

    return {
        "success": True,
        "school_id": school_id,
        "class_id": class_id,
        "academic_term_id": academic_term_id,
        "approved_students": approved_students,
    }
