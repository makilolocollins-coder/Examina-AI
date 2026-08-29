# ============================================================
# EXAMINA AI
# TEACHER PORTAL
# ============================================================

import streamlit as st
from sqlalchemy import select

from database.database import SessionLocal
from database.models import (
    AcademicSession,
    AcademicTerm,
    SchoolClass,
    Student,
    Subject,
    StudentSubject,
    Result,
    StudentTermReport,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_db():
    return SessionLocal()


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


def calculate_total(
    first_test: float,
    second_test: float,
    exam: float,
) -> float:
    """
    Add first test, second test and examination score.
    """

    return round(
        first_test + second_test + exam,
        2,
    )


# ============================================================
# TEACHER PORTAL
# ============================================================

def show_teacher_portal():

    st.title("👨‍🏫 Teacher Portal")

    st.write(
        "Enter and manage student academic results."
    )

    db = get_db()

    try:

        # ====================================================
        # SELECT ACADEMIC SESSION
        # ====================================================

        sessions = db.scalars(
            select(AcademicSession)
            .order_by(AcademicSession.name.desc())
        ).all()

        if not sessions:
            st.warning(
                "No academic sessions have been created yet."
            )
            return

        session_options = {
            session.name: session
            for session in sessions
        }

        selected_session_name = st.selectbox(
            "Academic Session",
            list(session_options.keys()),
        )

        selected_session = session_options[
            selected_session_name
        ]

        # ====================================================
        # SELECT TERM
        # ====================================================

        terms = db.scalars(
            select(AcademicTerm)
            .where(
                AcademicTerm.academic_session_id
                == selected_session.id
            )
            .order_by(
                AcademicTerm.term_number
            )
        ).all()

        if not terms:
            st.warning(
                "No terms exist for this academic session."
            )
            return

        term_options = {
            term.name: term
            for term in terms
        }

        selected_term_name = st.selectbox(
            "Academic Term",
            list(term_options.keys()),
        )

        selected_term = term_options[
            selected_term_name
        ]

        # ====================================================
        # SELECT SCHOOL
        # ====================================================
        #
        # For now the teacher's school is selected from
        # session state.
        #
        # Later this will come directly from teacher login.
        #
        # ====================================================

        school_id = st.session_state.get(
            "school_id"
        )

        if school_id is None:

            st.info(
                "Teacher school is not connected to "
                "authentication yet."
            )

            st.stop()

        # ====================================================
        # SELECT CLASS
        # ====================================================

        classes = db.scalars(
            select(SchoolClass)
            .where(
                SchoolClass.school_id
                == school_id
            )
            .order_by(
                SchoolClass.name
            )
        ).all()

        if not classes:
            st.warning(
                "No classes have been created."
            )
            return

        class_options = {
            school_class.name: school_class
            for school_class in classes
        }

        selected_class_name = st.selectbox(
            "Class",
            list(class_options.keys()),
        )

        selected_class = class_options[
            selected_class_name
        ]

        # ====================================================
        # GET STUDENTS
        # ====================================================

        students = db.scalars(
            select(Student)
            .where(
                Student.school_id
                == school_id,

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

        if not students:

            st.info(
                "No students are registered in this class."
            )

            return

        st.success(
            f"{len(students)} student(s) found."
        )

        # ====================================================
        # SELECT STUDENT
        # ====================================================

        student_options = {}

        for student in students:

            full_name = (
                f"{student.first_name} "
                f"{student.middle_name or ''} "
                f"{student.last_name}"
            ).replace(
                "  ",
                " ",
            ).strip()

            student_options[
                f"{student.admission_number} - {full_name}"
            ] = student

        selected_student_label = st.selectbox(
            "Student",
            list(student_options.keys()),
        )

        student = student_options[
            selected_student_label
        ]

        st.divider()

        st.subheader(
            f"Results: {student.first_name} "
            f"{student.last_name}"
        )

        # ====================================================
        # GET STUDENT SUBJECTS
        # ====================================================

        student_subjects = db.scalars(
            select(StudentSubject)
            .where(
                StudentSubject.student_id
                == student.id,

                StudentSubject.academic_term_id
                == selected_term.id,
            )
            .join(
                Subject,
                StudentSubject.subject_id
                == Subject.id,
            )
            .order_by(
                Subject.name
            )
        ).all()

        if not student_subjects:

            st.warning(
                "No subjects have been assigned "
                "to this student for this term."
            )

            return

        # ====================================================
        # RESULT ENTRY
        # ====================================================

        entered_results = []

        for student_subject in student_subjects:

            subject = db.get(
                Subject,
                student_subject.subject_id,
            )

            if subject is None:
                continue

            st.markdown(
                f"### {subject.name}"
            )

            existing_result = db.scalar(
                select(Result)
                .where(
                    Result.student_id
                    == student.id,

                    Result.subject_id
                    == subject.id,

                    Result.academic_term_id
                    == selected_term.id,
                )
            )

            first_test_default = (
                existing_result.first_test
                if existing_result
                else 0.0
            )

            second_test_default = (
                existing_result.second_test
                if existing_result
                else 0.0
            )

            exam_default = (
                existing_result.exam
                if existing_result
                else 0.0
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                first_test = st.number_input(
                    "1st Test",
                    min_value=0.0,
                    max_value=30.0,
                    value=float(
                        first_test_default
                    ),
                    step=1.0,
                    key=f"first_{student.id}_{subject.id}",
                )

            with col2:

                second_test = st.number_input(
                    "2nd Test",
                    min_value=0.0,
                    max_value=30.0,
                    value=float(
                        second_test_default
                    ),
                    step=1.0,
                    key=f"second_{student.id}_{subject.id}",
                )

            with col3:

                exam = st.number_input(
                    "Exam",
                    min_value=0.0,
                    max_value=70.0,
                    value=float(
                        exam_default
                    ),
                    step=1.0,
                    key=f"exam_{student.id}_{subject.id}",
                )

            total = calculate_total(
                first_test,
                second_test,
                exam,
            )

            grade = calculate_grade(
                total
            )

            st.write(
                f"**Total:** {total:.2f}  |  "
                f"**Grade:** {grade}"
            )

            entered_results.append(
                {
                    "subject_id": subject.id,
                    "first_test": first_test,
                    "second_test": second_test,
                    "exam": exam,
                    "total": total,
                    "grade": grade,
                }
            )

        # ====================================================
        # TEACHER'S REMARK
        # ====================================================

        existing_report = db.scalar(
            select(StudentTermReport)
            .where(
                StudentTermReport.student_id
                == student.id,

                StudentTermReport.academic_term_id
                == selected_term.id,
            )
        )

        existing_remark = (
            existing_report.teachers_remark
            if existing_report
            else ""
        )

        teachers_remark = st.text_area(
            "Teacher's Remark",
            value=existing_remark or "",
            placeholder=(
                "Enter teacher's remark for this student..."
            ),
        )

        # ====================================================
        # SAVE RESULTS
        # ====================================================

        if st.button(
            "💾 Save Student Results",
            type="primary",
            use_container_width=True,
        ):

            try:

                # --------------------------------------------
                # SAVE EACH SUBJECT RESULT
                # --------------------------------------------

                for item in entered_results:

                    result = db.scalar(
                        select(Result)
                        .where(
                            Result.student_id
                            == student.id,

                            Result.subject_id
                            == item["subject_id"],

                            Result.academic_term_id
                            == selected_term.id,
                        )
                    )

                    if result is None:

                        result = Result(
                            student_id=student.id,
                            subject_id=item["subject_id"],
                            academic_term_id=selected_term.id,
                        )

                        db.add(result)

                    result.first_test = (
                        item["first_test"]
                    )

                    result.second_test = (
                        item["second_test"]
                    )

                    result.exam = (
                        item["exam"]
                    )

                    result.total = (
                        item["total"]
                    )

                    result.grade = (
                        item["grade"]
                    )

                # --------------------------------------------
                # CREATE / UPDATE TERM REPORT
                # --------------------------------------------

                report = db.scalar(
                    select(StudentTermReport)
                    .where(
                        StudentTermReport.student_id
                        == student.id,

                        StudentTermReport.academic_term_id
                        == selected_term.id,
                    )
                )

                if report is None:

                    report = StudentTermReport(
                        student_id=student.id,
                        academic_term_id=selected_term.id,
                    )

                    db.add(report)

                report.teachers_remark = (
                    teachers_remark
                )

                # --------------------------------------------
                # NEW RESULTS REQUIRE PRINCIPAL APPROVAL
                # --------------------------------------------

                report.principal_approved = False
                report.published = False
                report.principal_id = None
                report.approved_at = None

                db.commit()

                st.success(
                    "Student results saved successfully."
                )

                st.info(
                    "The result is now awaiting principal approval."
                )

            except Exception as error:

                db.rollback()

                st.error(
                    f"Could not save results: {error}"
                )

    finally:

        db.close()
