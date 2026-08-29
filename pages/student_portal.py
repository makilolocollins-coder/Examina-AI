# ============================================================
# EXAMINA AI
# STUDENT PORTAL
# ============================================================
#
# Student workflow:
#
#   Student Login
#       ↓
#   Select Session
#       ↓
#   Select Term
#       ↓
#   Check Principal Approval
#       ↓
#   If NOT approved → Block result
#       ↓
#   If approved → Show result
#       ↓
#   If published → Allow download
#
# ============================================================

import streamlit as st

from sqlalchemy import select

from database.database import SessionLocal

from database.models import (
    AcademicSession,
    AcademicTerm,
    Result,
    School,
    Student,
    StudentTermReport,
    Subject,
)


# ============================================================
# MAIN PORTAL
# ============================================================

def show_student_portal():

    st.title("🎓 Student Portal")

    st.caption(
        "View your approved academic results."
    )

    db = SessionLocal()

    try:

        # ====================================================
        # SESSION STATE
        # ====================================================

        if "student_logged_in" not in st.session_state:

            st.session_state.student_logged_in = False

        if "student_id" not in st.session_state:

            st.session_state.student_id = None

        # ====================================================
        # DEVELOPMENT LOGIN
        # ====================================================
        #
        # Later replace with proper student authentication.
        #
        # ====================================================

        if not st.session_state.student_logged_in:

            st.subheader(
                "Student Login"
            )

            st.info(
                "Development login: enter the student's ID."
            )

            student_id = st.number_input(
                "Student ID",
                min_value=1,
                step=1,
                value=1,
            )

            if st.button(
                "Enter Student Portal",
                type="primary",
                use_container_width=True,
            ):

                student = db.get(
                    Student,
                    int(student_id),
                )

                if student is None:

                    st.error(
                        "Student account not found."
                    )

                elif not student.active:

                    st.error(
                        "This student account is inactive."
                    )

                else:

                    st.session_state.student_logged_in = True

                    st.session_state.student_id = (
                        student.id
                    )

                    st.rerun()

            return

        # ====================================================
        # GET STUDENT
        # ====================================================

        student = db.get(
            Student,
            st.session_state.student_id,
        )

        if student is None:

            st.error(
                "Student account not found."
            )

            st.session_state.student_logged_in = False
            st.session_state.student_id = None

            return

        # ====================================================
        # GET SCHOOL
        # ====================================================

        school = db.get(
            School,
            student.school_id,
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
                "Student Portal"
            )

            st.divider()

            st.write(
                f"**Student:** "
                f"{student.first_name} "
                f"{student.last_name}"
            )

            st.write(
                f"**Admission No.:** "
                f"{student.admission_number}"
            )

            st.divider()

            if st.button(
                "Logout",
                use_container_width=True,
            ):

                st.session_state.student_logged_in = False
                st.session_state.student_id = None

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
                    width=100,
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
        # STUDENT INFORMATION
        # ====================================================

        st.subheader(
            "Student Information"
        )

        info1, info2, info3 = st.columns(3)

        with info1:

            st.write(
                "**Name**"
            )

            st.write(
                " ".join(
                    filter(
                        None,
                        [
                            student.first_name,
                            student.middle_name,
                            student.last_name,
                        ],
                    )
                )
            )

        with info2:

            st.write(
                "**Admission Number**"
            )

            st.write(
                student.admission_number
            )

        with info3:

            st.write(
                "**Class**"
            )

            st.write(
                student.school_class.name
            )

        # ====================================================
        # SESSIONS
        # ====================================================

        sessions = list(
            db.scalars(
                select(AcademicSession)
                .order_by(
                    AcademicSession.name.desc()
                )
            ).all()
        )

        if not sessions:

            st.info(
                "No academic sessions are available."
            )

            return

        selected_session = st.selectbox(
            "Academic Session",
            sessions,
            format_func=lambda item: item.name,
        )

        # ====================================================
        # TERMS
        # ====================================================

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

            st.info(
                "No terms are available for this session."
            )

            return

        selected_term = st.selectbox(
            "Term",
            terms,
            format_func=lambda item: item.name,
        )

        # ====================================================
        # GET REPORT
        # ====================================================

        report = db.scalar(
            select(StudentTermReport)
            .where(
                StudentTermReport.student_id
                == student.id,

                StudentTermReport.academic_term_id
                == selected_term.id,
            )
        )

        st.divider()

        # ====================================================
        # NO REPORT
        # ====================================================

        if report is None:

            st.info(
                "No report has been created for this term yet."
            )

            return

        # ====================================================
        # APPROVAL CHECK
        # ====================================================

        if not report.principal_approved:

            st.warning(
                "🔒 RESULT NOT YET APPROVED"
            )

            st.write(
                "Your result is currently being reviewed "
                "by the school principal."
            )

            st.info(
                "You cannot view or download the official "
                "result until the principal approves it."
            )

            return

        # ====================================================
        # PUBLICATION CHECK
        # ====================================================

        if not report.published:

            st.success(
                "✅ RESULT APPROVED"
            )

            st.warning(
                "Your result has been approved by the "
                "principal but has not yet been published."
            )

            st.info(
                "Please check again when the school publishes "
                "the result."
            )

            return

        # ====================================================
        # RESULT IS AVAILABLE
        # ====================================================

        st.success(
            "✅ RESULT APPROVED AND PUBLISHED"
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
                    == student.id,

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
                "No subject results are available."
            )

            return

        # ====================================================
        # REPORT HEADER
        # ====================================================

        st.header(
            "Academic Report"
        )

        st.write(
            f"**Academic Session:** "
            f"{selected_session.name}"
        )

        st.write(
            f"**Term:** "
            f"{selected_term.name}"
        )

        st.write(
            f"**Student:** "
            f"{' '.join(filter(None, [student.first_name, student.middle_name, student.last_name]))}"
        )

        st.write(
            f"**Class:** "
            f"{student.school_class.name}"
        )

        # ====================================================
        # RESULTS TABLE
        # ====================================================

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
        # SUMMARY
        # ====================================================

        total_score = sum(
            result.total
            for result in results
        )

        subject_count = len(
            results
        )

        average = (
            round(
                total_score / subject_count,
                2,
            )
            if subject_count
            else 0.0
        )

        st.divider()

        summary1, summary2 = st.columns(2)

        with summary1:

            st.metric(
                "Total Score",
                f"{total_score:.2f}",
            )

        with summary2:

            st.metric(
                "Term Average",
                f"{average:.2f}",
            )

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

            st.write(
                "No teacher's remark."
            )

        # ====================================================
        # PRINCIPAL'S REMARK
        # ====================================================

        st.subheader(
            "Principal's Remark"
        )

        if report.principal_remark:

            st.info(
                report.principal_remark
            )

        else:

            st.write(
                "No principal's remark."
            )

        # ====================================================
        # THIRD TERM INFORMATION
        # ====================================================

        if selected_term.term_number == 3:

            st.divider()

            st.subheader(
                "Annual Performance"
            )

            if report.year_average is not None:

                st.metric(
                    "Year Average",
                    f"{report.year_average:.2f}",
                )

            else:

                st.info(
                    "Year average is not available."
                )

            if report.final_decision:

                if (
                    report.final_decision
                    == "PROMOTED"
                ):

                    st.success(
                        "🎉 PROMOTED"
                    )

                elif (
                    report.final_decision
                    == "NOT PROMOTED"
                ):

                    st.error(
                        "NOT PROMOTED"
                    )

                else:

                    st.write(
                        f"Final Decision: "
                        f"{report.final_decision}"
                    )

        # ====================================================
        # APPROVAL INFORMATION
        # ====================================================

        st.divider()

        st.subheader(
            "Approval Information"
        )

        st.success(
            "This report has been approved by the school."
        )

        if report.approved_at:

            st.caption(
                f"Approved at: {report.approved_at}"
            )
        
        if not report["principal_approved"]:
            st.warning(
                "Your result has not yet been approved by the Principal."
            )
            st.info(
                "You can view the result after it is released, "
                "but downloading is disabled until approval."
            )
        else:
        # Your existing download button goes here

        # ====================================================
        # DOWNLOAD
        # ====================================================

        st.divider()

        st.subheader(
            "Download Result"
        )

        # ----------------------------------------------------
        # Build downloadable text report.
        #
        # We deliberately do not show this button before
        # principal approval + publication.
        # ----------------------------------------------------

        lines = []

        lines.append(
            school.name
        )

        lines.append(
            school.address
        )

        if school.email:

            lines.append(
                f"Email: {school.email}"
            )

        lines.append(
            f"Academic Session: "
            f"{selected_session.name}"
        )

        lines.append(
            f"Term: "
            f"{selected_term.name}"
        )

        lines.append(
            ""
        )

        lines.append(
            f"Student: "
            f"{' '.join(filter(None, [student.first_name, student.middle_name, student.last_name]))}"
        )

        lines.append(
            f"Admission Number: "
            f"{student.admission_number}"
        )

        lines.append(
            f"Class: "
            f"{student.school_class.name}"
        )

        lines.append(
            ""
        )

        lines.append(
            "SUBJECT RESULTS"
        )

        lines.append(
            "-" * 70
        )

        for result in results:

            lines.append(
                (
                    f"{result.subject.name} | "
                    f"1st Test: {result.first_test} | "
                    f"2nd Test: {result.second_test} | "
                    f"Exam: {result.exam} | "
                    f"Total: {result.total} | "
                    f"Grade: {result.grade or ''} | "
                    f"Position: {result.position or ''}"
                )
            )

        lines.append(
            ""
        )

        lines.append(
            f"Total Score: "
            f"{total_score:.2f}"
        )

        lines.append(
            f"Term Average: "
            f"{average:.2f}"
        )

        if selected_term.term_number == 3:

            if report.year_average is not None:

                lines.append(
                    f"Year Average: "
                    f"{report.year_average:.2f}"
                )

            if report.final_decision:

                lines.append(
                    f"Final Decision: "
                    f"{report.final_decision}"
                )

        lines.append(
            ""
        )

        lines.append(
            f"Teacher's Remark: "
            f"{report.teachers_remark or ''}"
        )

        lines.append(
            f"Principal's Remark: "
            f"{report.principal_remark or ''}"
        )

        lines.append(
            ""
        )

        lines.append(
            "STATUS: APPROVED AND PUBLISHED"
        )

        report_text = "\n".join(
            lines
        )

        st.download_button(
            label="📥 Download Result",
            data=report_text,
            file_name=(
                f"{student.admission_number}_"
                f"{selected_session.name}_"
                f"{selected_term.name}_"
                f"result.txt"
            ),
            mime="text/plain",
            use_container_width=True,
        )

    finally:

        db.close()
