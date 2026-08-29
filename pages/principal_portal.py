# ============================================================
# EXAMINA AI
# PRINCIPAL PORTAL
# ============================================================
#
# Principal workflow:
#
#   Session
#      ↓
#   Term
#      ↓
#   Class
#      ↓
#   Student
#      ↓
#   Review complete result
#      ↓
#   Approve OR Reject
#
# Each student is approved individually.
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
    SchoolClass,
    Student,
    Subject,
)

from services.approval_service import (
    approve_student_result,
    reject_student_result,
    get_approval_status,
    verify_principal,
)

from services.result_service import (
    calculate_student_average,
    calculate_year_average,
    calculate_overall_positions,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Examina AI | Principal Portal",
    page_icon="🏫",
    layout="wide",
)


# ============================================================
# DATABASE
# ============================================================

db = SessionLocal()


# ============================================================
# SESSION STATE
# ============================================================

if "principal_logged_in" not in st.session_state:
    st.session_state.principal_logged_in = False

if "principal_id" not in st.session_state:
    st.session_state.principal_id = None

if "principal_school_id" not in st.session_state:
    st.session_state.principal_school_id = None


# ============================================================
# DEVELOPMENT LOGIN
# ============================================================
#
# This will later be replaced by proper authentication.
#
# ============================================================

if not st.session_state.principal_logged_in:

    st.title("🏫 Examina AI")

    st.subheader(
        "Principal Portal"
    )

    st.info(
        "Principal authentication is currently "
        "in development mode."
    )

    col1, col2 = st.columns(2)

    with col1:

        principal_id = st.number_input(
            "Principal ID",
            min_value=1,
            step=1,
        )

    with col2:

        school_id = st.number_input(
            "School ID",
            min_value=1,
            step=1,
        )

    if st.button(
        "Enter Principal Portal",
        type="primary",
        use_container_width=True,
    ):

        try:

            principal = verify_principal(
                db=db,
                principal_id=principal_id,
                school_id=school_id,
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

    db.close()

    st.stop()


# ============================================================
# GET SCHOOL
# ============================================================

school = db.get(
    School,
    st.session_state.principal_school_id,
)

if school is None:

    st.error(
        "School account not found."
    )

    db.close()

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("Examina AI")

    st.caption(
        "Principal Portal"
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


# ============================================================
# SCHOOL HEADER
# ============================================================

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


# ============================================================
# ACADEMIC SESSION
# ============================================================

st.subheader(
    "1. Select Academic Session"
)

session_query = (
    select(AcademicSession)
    .order_by(
        AcademicSession.name.desc()
    )
)

sessions = list(
    db.scalars(
        session_query
    ).all()
)


if not sessions:

    st.warning(
        "No academic sessions available."
    )

    db.close()

    st.stop()


selected_session = st.selectbox(
    "Academic Session",
    sessions,
    format_func=lambda item:
        item.name,
)


# ============================================================
# TERM
# ============================================================

st.subheader(
    "2. Select Term"
)

term_query = (
    select(AcademicTerm)
    .where(
        AcademicTerm.academic_session_id
        == selected_session.id
    )
    .order_by(
        AcademicTerm.id
    )
)

terms = list(
    db.scalars(
        term_query
    ).all()
)


if not terms:

    st.warning(
        "No terms exist for this session."
    )

    db.close()

    st.stop()


selected_term = st.selectbox(
    "Term",
    terms,
    format_func=lambda item:
        item.name,
)


# ============================================================
# CLASS
# ============================================================

st.subheader(
    "3. Select Class"
)

class_query = (
    select(SchoolClass)
    .where(
        SchoolClass.school_id
        == school.id
    )
    .order_by(
        SchoolClass.name
    )
)

classes = list(
    db.scalars(
        class_query
    ).all()
)


if not classes:

    st.warning(
        "No classes have been registered."
    )

    db.close()

    st.stop()


selected_class = st.selectbox(
    "Class",
    classes,
    format_func=lambda item:
        item.name,
)


st.divider()


# ============================================================
# GET STUDENTS
# ============================================================

student_query = (
    select(Student)
    .where(
        Student.school_id == school.id,
        Student.class_id == selected_class.id,
        Student.active == True,
    )
    .order_by(
        Student.last_name,
        Student.first_name,
    )
)

students = list(
    db.scalars(
        student_query
    ).all()
)


# ============================================================
# CLASS SUMMARY
# ============================================================

approved_count = 0
pending_count = 0
no_result_count = 0


for student in students:

    status = get_approval_status(
        db=db,
        student_id=student.id,
        academic_term_id=selected_term.id,
    )

    if not status["has_results"]:

        no_result_count += 1

    elif status["approved"]:

        approved_count += 1

    else:

        pending_count += 1


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
        "No Results",
        no_result_count,
    )


st.divider()


# ============================================================
# STUDENT LIST
# ============================================================

st.subheader(
    "4. Select Student to Review"
)


if not students:

    st.info(
        "No active students found in this class."
    )

    db.close()

    st.stop()


student_options = {
    (
        f"{student.last_name}, "
        f"{student.first_name}"
        + (
            f" {student.middle_name}"
            if student.middle_name
            else ""
        )
        + f" — {student.admission_number}"
    ): student
    for student in students
}


selected_student_label = st.selectbox(
    "Student",
    list(student_options.keys()),
)


selected_student = student_options[
    selected_student_label
]


st.divider()


# ============================================================
# STUDENT INFORMATION
# ============================================================

st.subheader(
    "Student Information"
)


student_col1, student_col2, student_col3 = st.columns(
    3
)


with student_col1:

    st.write(
        "**Name**"
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


with student_col2:

    st.write(
        "**Admission Number**"
    )

    st.write(
        selected_student.admission_number
    )


with student_col3:

    st.write(
        "**Class**"
    )

    st.write(
        selected_student.school_class.name
    )


# ============================================================
# APPROVAL STATUS
# ============================================================

status = get_approval_status(
    db=db,
    student_id=selected_student.id,
    academic_term_id=selected_term.id,
)


if not status["has_results"]:

    st.error(
        "This student has no results for "
        f"{selected_term.name}."
    )

    db.close()

    st.stop()


if status["approved"]:

    st.success(
        "✅ THIS RESULT HAS BEEN APPROVED"
    )

else:

    st.warning(
        "⏳ THIS RESULT IS WAITING FOR "
        "PRINCIPAL APPROVAL"
    )


# ============================================================
# GET RESULTS
# ============================================================

result_query = (
    select(Result)
    .join(
        Subject,
        Result.subject_id == Subject.id,
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
)

results = list(
    db.scalars(
        result_query
    ).all()
)


# ============================================================
# RESULT TABLE
# ============================================================

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


if result_rows:

    st.dataframe(
        result_rows,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# TERM SUMMARY
# ============================================================

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

    if item["student"].id == selected_student.id:

        overall_position = item["position"]

        break


summary1, summary2, summary3 = st.columns(3)


with summary1:

    st.metric(
        "Term Average",
        f"{average:.2f}",
    )


with summary2:

    if overall_position:

        st.metric(
            "Overall Position",
            f"{overall_position}",
        )

    else:

        st.metric(
            "Overall Position",
            "N/A",
        )


with summary3:

    st.metric(
        "Subjects",
        len(results),
    )


# ============================================================
# YEAR AVERAGE
# ============================================================

if selected_term.name == "3rd Term":

    st.divider()

    st.subheader(
        "Annual Performance"
    )

    year_average = calculate_year_average(
        db=db,
        student_id=selected_student.id,
        academic_session_id=
            selected_session.id,
    )

    if year_average is not None:

        st.metric(
            "Year Average",
            f"{year_average:.2f}",
        )

    else:

        st.warning(
            "Year average cannot be calculated "
            "until all three term results are available."
        )


# ============================================================
# TEACHER'S REMARK
# ============================================================

st.divider()

st.subheader(
    "Teacher's Remark"
)


teacher_remarks = []

for result in results:

    # The current Result model does not yet contain
    # a teacher_remark field.
    #
    # This section is reserved for the teacher remark
    # once that field is added.

    pass


st.info(
    "Teacher's remark will appear here after the "
    "teacher remark field is connected."
)


# ============================================================
# PRINCIPAL REMARK
# ============================================================

st.subheader(
    "Principal's Remark"
)


existing_principal_remark = None

for result in results:

    if result.principal_remark:

        existing_principal_remark = (
            result.principal_remark
        )

        break


principal_remark = st.text_area(
    "Enter principal's remark",
    value=existing_principal_remark or "",
    key=(
        f"principal_remark_"
        f"{selected_student.id}_"
        f"{selected_term.id}"
    ),
    height=120,
    disabled=status["approved"],
)


# ============================================================
# 3RD TERM PASS / FAIL
# ============================================================
#
# This is displayed only for 3rd Term.
#
# The final database field for PASS/FAIL will be added
# to the report/approval model.
#
# ============================================================

if selected_term.name == "3rd Term":

    st.subheader(
        "Final Academic Decision"
    )

    if status["approved"]:

        st.info(
            "The final decision has already been approved."
        )

    else:

        final_decision = st.radio(
            "Principal's Decision",
            [
                "PASS",
                "FAIL",
            ],
            horizontal=True,
            key=(
                f"decision_"
                f"{selected_student.id}_"
                f"{selected_term.id}"
            ),
        )

        st.caption(
            "The final PASS/FAIL decision will be "
            "stored with the approved 3rd-term report."
        )


# ============================================================
# APPROVAL ACTIONS
# ============================================================

st.divider()

st.subheader(
    "Principal Decision"
)


if status["approved"]:

    st.success(
        "🔒 Result locked after approval."
    )

    st.caption(
        "Students can download this result "
        "after approval."
    )

else:

    approve_col, reject_col = st.columns(2)

    # --------------------------------------------------------
    # APPROVE
    # --------------------------------------------------------

    with approve_col:

        if st.button(
            "✅ APPROVE THIS STUDENT RESULT",
            type="primary",
            use_container_width=True,
        ):

            try:

                approve_student_result(
                    db=db,
                    student_id=
                        selected_student.id,

                    academic_term_id=
                        selected_term.id,

                    principal_id=
                        st.session_state.principal_id,

                    principal_remark=
                        principal_remark,
                )

                st.success(
                    "Student result approved successfully."
                )

                st.rerun()

            except Exception as error:

                st.error(
                    str(error)
                )

    # --------------------------------------------------------
    # REJECT
    # --------------------------------------------------------

    with reject_col:

        if st.button(
            "❌ REJECT THIS STUDENT RESULT",
            use_container_width=True,
        ):

            if not principal_remark.strip():

                st.error(
                    "A reason is required when rejecting "
                    "a result."
                )

            else:

                try:

                    reject_student_result(
                        db=db,
                        student_id=
                            selected_student.id,

                        academic_term_id=
                            selected_term.id,

                        principal_id=
                            st.session_state.principal_id,

                        principal_remark=
                            principal_remark,
                    )

                    st.warning(
                        "Student result rejected."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        str(error)
                    )


# ============================================================
# APPROVAL INFORMATION
# ============================================================

if status["approved"]:

    st.divider()

    st.subheader(
        "Approval Information"
    )

    approval_col1, approval_col2 = st.columns(2)

    approved_at = None

    principal_name = None

    for result in results:

        if result.principal_approved:

            approved_at = (
                result.principal_approved_at
            )

            if result.principal_id:

                principal = db.get(
                    __import__(
                        "database.models",
                        fromlist=["Teacher"],
                    ).Teacher,
                    result.principal_id,
                )

                if principal:

                    principal_name = (
                        f"{principal.first_name} "
                        f"{principal.last_name}"
                    )

            break

    with approval_col1:

        st.write(
            "**Approved By**"
        )

        st.write(
            principal_name
            or "Principal"
        )

    with approval_col2:

        st.write(
            "**Approved At**"
        )

        st.write(
            str(
                approved_at
            )
            if approved_at
            else "N/A"
        )


# ============================================================
# CLOSE DATABASE
# ============================================================

db.close()
