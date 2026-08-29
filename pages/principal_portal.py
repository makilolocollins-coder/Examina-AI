# ============================================================
# EXAMINA AI
# PRINCIPAL PORTAL
# ============================================================
#
# Principal workflow:
#
#   Login
#      ↓
#   Academic Session
#      ↓
#   Term
#      ↓
#   Class
#      ↓
#   Student
#      ↓
#   Review Result
#      ↓
#   Add Principal Remark
#      ↓
#   3rd Term: PASS / FAIL
#      ↓
#   Approve
#      ↓
#   Publish
#      ↓
#   Student Can Download
#
# ============================================================

import streamlit as st

from datetime import datetime

from sqlalchemy import select

from database.database import SessionLocal

from database.models import (
    AcademicSession,
    AcademicTerm,
    Result,
    School,
    SchoolClass,
    Student,
    StudentTermReport,
    Subject,
    Teacher,
)

from services.result_service import (
    calculate_student_average,
    calculate_year_average,
    calculate_overall_positions,
)


# ============================================================
# HELPER
# ============================================================

def get_or_create_report(
    db,
    student_id: int,
    academic_term_id: int,
):
    """
    Get a student's complete term report.

    If it does not exist, create it.
    """

    report = db.scalar(
        select(StudentTermReport).where(
            StudentTermReport.student_id == student_id,
            StudentTermReport.academic_term_id
            == academic_term_id,
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
        db.flush()

    return report


# ============================================================
# PRINCIPAL VERIFICATION
# ============================================================

def verify_principal(
    db,
    principal_id: int,
    school_id: int,
):
    """
    Verify that the principal belongs to the school
    and has been verified.

    For now, Principal is represented by Teacher.
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
# MAIN PORTAL
# ============================================================

def show_principal_portal():

    # ========================================================
    # PAGE TITLE
    # ========================================================

    st.title("🏫 Principal Portal")

    st.caption(
        "Review, approve and publish student results."
    )

    # ========================================================
    # DATABASE
    # ========================================================

    db = SessionLocal()

    try:

        # ====================================================
        # SESSION STATE
        # ====================================================

        if "principal_logged_in" not in st.session_state:
            st.session_state.principal_logged_in = False

        if "principal_id" not in st.session_state:
            st.session_state.principal_id = None

        if "principal_school_id" not in st.session_state:
            st.session_state.principal_school_id = None

        # ====================================================
        # DEVELOPMENT LOGIN
        # ====================================================
        #
        # Later this will be replaced with proper
        # authentication.
        #
        # ====================================================

        if not st.session_state.principal_logged_in:

            st.subheader(
                "Principal Login"
            )

            st.info(
                "Development login: enter the verified "
                "teacher ID being used as the principal "
                "and the school ID."
            )

            col1, col2 = st.columns(2)

            with col1:

                principal_id = st.number_input(
                    "Principal ID",
                    min_value=1,
                    step=1,
                    value=1,
                )

            with col2:

                school_id = st.number_input(
                    "School ID",
                    min_value=1,
                    step=1,
                    value=1,
                )

            if st.button(
                "Enter Principal Portal",
                type="primary",
                use_container_width=True,
            ):

                try:

                    principal = verify_principal(
                        db=db,
                        principal_id=int(
                            principal_id
                        ),
                        school_id=int(
                            school_id
                        ),
                    )

                    st.session_state.principal_logged_in = True

                    st.session_state.principal_id = (
                        principal.id
                    )

                    st.session_state.principal_school_id = (
                        principal.school_id
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        str(error)
                    )

            return

        # ====================================================
        # GET PRINCIPAL
        # ====================================================

        principal = db.get(
            Teacher,
            st.session_state.principal_id,
        )

        if principal is None:

            st.error(
                "Principal account not found."
            )

            st.session_state.principal_logged_in = False

            return

        # ====================================================
        # GET SCHOOL
        # ====================================================

        school = db.get(
            School,
            st.session_state.principal_school_id,
        )

        if school is None:

            st.error(
                "School account not found."
            )

            return

        # ====================================================
        # SIDEBAR
        # ====================================================

        with st.sidebar:

            st.title("Examina AI")

            st.caption(
                "Principal Portal"
            )

            st.divider()

            st.write(
                f"**Principal:** "
                f"{principal.first_name} "
                f"{principal.last_name}"
            )

            st.write(
                f"**School:** {school.name}"
            )

            st.divider()

            if st.button(
                "Logout",
                use_container_width=True,
            ):

                st.session_state.principal_logged_in = False
                st.session_state.principal_id = None
                st.session_state.principal_school_id = None

                st.rerun()

        # ====================================================
        # SCHOOL HEADER
        # ====================================================

        header_left, header_right = st.columns(
            [1, 5]
        )

        with header_left:

            if school.school_badge:

                st.image(
                    school.school_badge,
                    width=110,
                )

        with header_right:

            st.title(
                school.name
            )

            st.write(
                f"{school.local_government}, "
                f"{school.state}"
            )

            if school.address:

                st.write(
                    f"📍 {school.address}"
                )

            if school.email:

                st.write(
                    f"📧 {school.email}"
                )

            st.write(
                f"📞 {school.phone}"
            )

        st.divider()

        # ====================================================
        # SESSION
        # ====================================================

        st.subheader(
            "1. Select Academic Session"
        )

        sessions = list(
            db.scalars(
                select(AcademicSession)
                .order_by(
                    AcademicSession.name.desc()
                )
            ).all()
        )

        if not sessions:

            st.warning(
                "No academic sessions available."
            )

            return

        selected_session = st.selectbox(
            "Academic Session",
            sessions,
            format_func=lambda item: item.name,
        )

        # ====================================================
        # TERM
        # ====================================================

        st.subheader(
            "2. Select Term"
        )

        terms = list(
            db.scalars(
                select(AcademicTerm)
                .where(
                    AcademicTerm.academic_session_id
                    == selected_session.id
                )
                .order_by(
                    AcademicTerm.term_number
                )
            ).all()
        )

        if not terms:

            st.warning(
                "No terms exist for this academic session."
            )

            return

        selected_term = st.selectbox(
            "Academic Term",
            terms,
            format_func=lambda item: item.name,
        )

        # ====================================================
        # CLASS
        # ====================================================

        st.subheader(
            "3. Select Class"
        )

        classes = list(
            db.scalars(
                select(SchoolClass)
                .where(
                    SchoolClass.school_id
                    == school.id
                )
                .order_by(
                    SchoolClass.name
                )
            ).all()
        )

        if not classes:

            st.warning(
                "No classes have been registered."
            )

            return

        selected_class = st.selectbox(
            "Class",
            classes,
            format_func=lambda item: item.name,
        )

        # ====================================================
        # STUDENTS
        # ====================================================

        students = list(
            db.scalars(
                select(Student)
                .where(
                    Student.school_id
                    == school.id,

                    Student.class_id
                    == selected_class.id,

                    Student.active
                    == True,
                )
                .order_by(
                    Student.last_name,
                    Student.first_name,
                )
            ).all()
        )

        if not students:

            st.info(
                "No active students are registered "
                "in this class."
            )

            return

        # ====================================================
        # CLASS SUMMARY
        # ====================================================

        approved_count = 0
        published_count = 0
        pending_count = 0
        no_result_count = 0

        for student in students:

            report = db.scalar(
                select(StudentTermReport)
                .where(
                    StudentTermReport.student_id
                    == student.id,

                    StudentTermReport.academic_term_id
                    == selected_term.id,
                )
            )

            result_exists = db.scalar(
                select(Result.id)
                .where(
                    Result.student_id
                    == student.id,

                    Result.academic_term_id
                    == selected_term.id,
                )
            )

            if result_exists is None:

                no_result_count += 1

            elif report and report.principal_approved:

                approved_count += 1

                if report.published:
                    published_count += 1

            else:

                pending_count += 1

        st.divider()

        st.subheader(
            f"{selected_class.name} • "
            f"{selected_term.name}"
        )

        stat1, stat2, stat3, stat4 = st.columns(4)

        with stat1:

            st.metric(
                "Students",
                len(students),
            )

        with stat2:

            st.metric(
                "Approved",
                approved_count,
            )

        with stat3:

            st.metric(
                "Pending",
                pending_count,
            )

        with stat4:

            st.metric(
                "Published",
                published_count,
            )

        # ====================================================
        # STUDENT
        # ====================================================

        st.divider()

        st.subheader(
            "4. Select Student"
        )

        student_options = {}

        for student in students:

            full_name = " ".join(
                filter(
                    None,
                    [
                        student.first_name,
                        student.middle_name,
                        student.last_name,
                    ],
                )
            )

            label = (
                f"{student.last_name}, "
                f"{full_name} "
                f"— {student.admission_number}"
            )

            student_options[label] = student

        selected_student_label = st.selectbox(
            "Student",
            list(student_options.keys()),
        )

        selected_student = student_options[
            selected_student_label
        ]

        # ====================================================
        # STUDENT INFORMATION
        # ====================================================

        st.divider()

        st.subheader(
            "Student Information"
        )

        info1, info2, info3 = st.columns(3)

        with info1:

            st.write(
                "**Student**"
            )

            st.write(
                " ".join(
                    filter(
                        None,
                        [
                            selected_student.first_name,
                            selected_student.middle_name,
                            selected_student.last_name,
                        ],
                    )
                )
            )

        with info2:

            st.write(
                "**Admission Number**"
            )

            st.write(
                selected_student.admission_number
            )

        with info3:

            st.write(
                "**Class**"
            )

            st.write(
                selected_student.school_class.name
            )

        # ====================================================
        # GET RESULTS
        # ====================================================

        results = list(
            db.scalars(
                select(Result)
                .join(
                    Subject,
                    Result.subject_id
                    == Subject.id,
                )
                .where(
                    Result.student_id
                    == selected_student.id,

                    Result.academic_term_id
                    == selected_term.id,
                )
                .order_by(
                    Subject.name
                )
            ).all()
        )

        if not results:

            st.warning(
                "This student has no results for "
                f"{selected_term.name}."
            )

            return

        # ====================================================
        # GET REPORT
        # ====================================================

        report = get_or_create_report(
            db=db,
            student_id=selected_student.id,
            academic_term_id=selected_term.id,
        )

        db.commit()

        # ====================================================
        # APPROVAL STATUS
        # ====================================================

        if report.principal_approved:

            if report.published:

                st.success(
                    "✅ APPROVED AND PUBLISHED"
                )

            else:

                st.success(
                    "✅ APPROVED"
                )

                st.warning(
                    "The report has been approved but "
                    "is not yet published."
                )

        else:

            st.warning(
                "⏳ RESULT AWAITING PRINCIPAL APPROVAL"
            )

        # ====================================================
        # RESULT TABLE
        # ====================================================

        st.subheader(
            "Student Result"
        )

        result_rows = []

        for result in results:

            result_rows.append(
                {
                    "Subject":
                        result.subject.name,

                    "1st Test":
                        result.first_test,

                    "2nd Test":
                        result.second_test,

                    "Exam":
                        result.exam,

                    "Total":
                        result.total,

                    "Grade":
                        result.grade or "",

                    "Position":
                        result.position or "",
                }
            )

        st.dataframe(
            result_rows,
            use_container_width=True,
            hide_index=True,
        )

        # ====================================================
        # TERM AVERAGE
        # ====================================================

        average = calculate_student_average(
            db=db,
            student_id=selected_student.id,
            academic_term_id=selected_term.id,
        )

        rankings = calculate_overall_positions(
            db=db,
            school_id=school.id,
            class_id=selected_class.id,
            academic_term_id=selected_term.id,
        )

        overall_position = None

        for item in rankings:

            if (
                item["student"].id
                == selected_student.id
            ):

                overall_position = item[
                    "position"
                ]

                break

        summary1, summary2, summary3 = st.columns(3)

        with summary1:

            st.metric(
                "Term Average",
                f"{average:.2f}",
            )

        with summary2:

            st.metric(
                "Overall Position",
                (
                    str(overall_position)
                    if overall_position
                    else "N/A"
                ),
            )

        with summary3:

            st.metric(
                "Subjects",
                len(results),
            )

        # ====================================================
        # 3RD TERM YEAR AVERAGE
        # ====================================================

        if selected_term.term_number == 3:

            st.divider()

            st.subheader(
                "Annual Performance"
            )

            year_average = calculate_year_average(
                db=db,
                student_id=selected_student.id,
                academic_session_id=selected_session.id,
            )

            if year_average is None:

                st.warning(
                    "Year average cannot be calculated "
                    "until results for all three terms "
                    "are available."
                )

            else:

                st.metric(
                    "Year Average",
                    f"{year_average:.2f}",
                )

                # Save calculated year average
                # to the report.

                report.year_average = (
                    year_average
                )

                db.commit()

        # ====================================================
        # TEACHER'S REMARK
        # ====================================================

        st.divider()

        st.subheader(
            "Teacher's Remark"
        )

        if report.teachers_remark:

            st.info(
                report.teachers_remark
            )

        else:

            st.info(
                "No teacher's remark has been entered."
            )

        # ====================================================
        # PRINCIPAL'S REMARK
        # ====================================================

        st.subheader(
            "Principal's Remark"
        )

        principal_remark = st.text_area(
            "Principal's Remark",
            value=(
                report.principal_remark
                or ""
            ),
            height=120,
            disabled=report.principal_approved,
            key=(
                f"principal_remark_"
                f"{selected_student.id}_"
                f"{selected_term.id}"
            ),
        )

        # ====================================================
        # FINAL DECISION
        # ====================================================

        final_decision = None

        if selected_term.term_number == 3:

            st.subheader(
                "Final Academic Decision"
            )

            if report.final_decision:

                st.info(
                    f"Current Decision: "
                    f"**{report.final_decision}**"
                )

            if not report.principal_approved:

                final_decision = st.radio(
                    "Student's Final Decision",
                    [
                        "PROMOTED",
                        "NOT PROMOTED",
                    ],
                    horizontal=True,
                    key=(
                        f"final_decision_"
                        f"{selected_student.id}_"
                        f"{selected_term.id}"
                    ),
                )

        # ====================================================
        # APPROVAL ACTIONS
        # ====================================================

        st.divider()

        st.subheader(
            "Principal Decision"
        )

        if report.principal_approved:

            st.success(
                "🔒 This student's report has been approved."
            )

            if report.approved_at:

                st.caption(
                    "Approved at: "
                    f"{report.approved_at}"
                )

            # ----------------------------------------------
            # PUBLISH
            # ----------------------------------------------

            if not report.published:

                if st.button(
                    "📢 Publish Result",
                    type="primary",
                    use_container_width=True,
                ):

                    report.published = True

                    db.commit()

                    st.success(
                        "Result published successfully."
                    )

                    st.rerun()

            else:

                st.success(
                    "📢 Result is published."
                )

        else:

            approve_col, reject_col = st.columns(2)

            # ----------------------------------------------
            # APPROVE
            # ----------------------------------------------

            with approve_col:

                if st.button(
                    "✅ APPROVE RESULT",
                    type="primary",
                    use_container_width=True,
                ):

                    try:

                        # 3rd Term must have a decision
                        if (
                            selected_term.term_number == 3
                            and final_decision is None
                        ):

                            st.error(
                                "A final promotion decision "
                                "is required for 3rd Term."
                            )

                        else:

                            report.principal_remark = (
                                principal_remark.strip()
                                or None
                            )

                            if (
                                selected_term.term_number
                                == 3
                            ):

                                report.final_decision = (
                                    final_decision
                                )

                                # Make sure the latest
                                # year average is stored.

                                year_average = (
                                    calculate_year_average(
                                        db=db,
                                        student_id=(
                                            selected_student.id
                                        ),
                                        academic_session_id=(
                                            selected_session.id
                                        ),
                                    )
                                )

                                if year_average is None:

                                    st.error(
                                        "All three term results "
                                        "are required before "
                                        "approving the 3rd Term."
                                    )

                                    db.rollback()

                                    st.stop()

                                report.year_average = (
                                    year_average
                                )

                            else:

                                report.final_decision = None
                                report.year_average = None

                            report.principal_approved = True

                            report.principal_id = (
                                st.session_state.principal_id
                            )

                            report.approved_at = (
                                datetime.utcnow()
                            )

                            # Approval does NOT automatically
                            # publish the report.

                            report.published = False

                            db.commit()

                            st.success(
                                "Student result approved successfully."
                            )

                            st.rerun()

                    except Exception as error:

                        db.rollback()

                        st.error(
                            f"Could not approve result: {error}"
                        )

            # ----------------------------------------------
            # REJECT
            # ----------------------------------------------

            with reject_col:

                if st.button(
                    "❌ REJECT RESULT",
                    use_container_width=True,
                ):

                    if not principal_remark.strip():

                        st.error(
                            "A principal's remark is required "
                            "when rejecting a result."
                        )

                    else:

                        report.principal_remark = (
                            principal_remark.strip()
                        )

                        report.principal_approved = False

                        report.published = False

                        report.principal_id = (
                            st.session_state.principal_id
                        )

                        report.approved_at = None

                        db.commit()

                        st.warning(
                            "Result rejected and returned "
                            "for correction."
                        )

                        st.rerun()

        # ====================================================
        # APPROVAL INFORMATION
        # ====================================================

        if report.principal_approved:

            st.divider()

            st.subheader(
                "Approval Information"
            )

            approved_principal = None

            if report.principal_id:

                approved_principal = db.get(
                    Teacher,
                    report.principal_id,
                )

            approval_col1, approval_col2 = st.columns(2)

            with approval_col1:

                st.write(
                    "**Approved By**"
                )

                if approved_principal:

                    st.write(
                        f"{approved_principal.first_name} "
                        f"{approved_principal.last_name}"
                    )

                else:

                    st.write(
                        "Principal"
                    )

            with approval_col2:

                st.write(
                    "**Approved At**"
                )

                st.write(
                    str(
                        report.approved_at
                    )
                    if report.approved_at
                    else "N/A"
                )

    finally:

        db.close()
