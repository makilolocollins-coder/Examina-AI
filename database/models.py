# ============================================================
# EXAMINA AI
# DATABASE MODELS
# ============================================================

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


# ============================================================
# BASE CLASS
# ============================================================

class Base(DeclarativeBase):
    pass


# ============================================================
# SCHOOL
# ============================================================

class School(Base):

    __tablename__ = "schools"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    address: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    local_government: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    registration_certificate: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    school_badge: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # --------------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------------

    students = relationship(
        "Student",
        back_populates="school",
    )

    teachers = relationship(
        "Teacher",
        back_populates="school",
    )

    classes = relationship(
        "SchoolClass",
        back_populates="school",
    )


# ============================================================
# ACADEMIC SESSION
# ============================================================

class AcademicSession(Base):

    __tablename__ = "academic_sessions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    curriculum_version: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # --------------------------------------------------------
    # RELATIONSHIP
    # --------------------------------------------------------

    terms = relationship(
        "AcademicTerm",
        back_populates="academic_session",
        cascade="all, delete-orphan",
    )


# ============================================================
# ACADEMIC TERM
# ============================================================

class AcademicTerm(Base):

    __tablename__ = "academic_terms"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    academic_session_id: Mapped[int] = mapped_column(
        ForeignKey("academic_sessions.id"),
        nullable=False,
    )

    # --------------------------------------------------------
    # TERM NUMBER
    #
    # 1 = 1st Term
    # 2 = 2nd Term
    # 3 = 3rd Term
    # --------------------------------------------------------

    term_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # --------------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------------

    academic_session = relationship(
        "AcademicSession",
        back_populates="terms",
    )

    student_subjects = relationship(
        "StudentSubject",
        back_populates="academic_term",
        cascade="all, delete-orphan",
    )

    results = relationship(
        "Result",
        back_populates="academic_term",
        cascade="all, delete-orphan",
    )

    term_reports = relationship(
        "StudentTermReport",
        back_populates="academic_term",
        cascade="all, delete-orphan",
    )

    # --------------------------------------------------------
    # PREVENT DUPLICATE TERMS
    # --------------------------------------------------------

    __table_args__ = (

        UniqueConstraint(
            "academic_session_id",
            "term_number",
            name="unique_term_number_per_session",
        ),

        UniqueConstraint(
            "academic_session_id",
            "name",
            name="unique_term_name_per_session",
        ),
    )


# ============================================================
# SCHOOL CLASS
# ============================================================

class SchoolClass(Base):

    __tablename__ = "school_classes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    education_level: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    field: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    school_id: Mapped[int] = mapped_column(
        ForeignKey("schools.id"),
        nullable=False,
    )

    # --------------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------------

    school = relationship(
        "School",
        back_populates="classes",
    )

    students = relationship(
        "Student",
        back_populates="school_class",
    )

    # --------------------------------------------------------
    # PREVENT DUPLICATE CLASS
    # --------------------------------------------------------

    __table_args__ = (

        UniqueConstraint(
            "name",
            "school_id",
            name="unique_class_per_school",
        ),
    )


# ============================================================
# STUDENT
# ============================================================

class Student(Base):

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    admission_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    middle_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # --------------------------------------------------------
    # SCHOOL
    # --------------------------------------------------------

    school_id: Mapped[int] = mapped_column(
        ForeignKey("schools.id"),
        nullable=False,
    )

    # --------------------------------------------------------
    # CLASS
    #
    # class_id is the single source of truth.
    #
    # Class name is accessed with:
    #
    # student.school_class.name
    # --------------------------------------------------------

    class_id: Mapped[int] = mapped_column(
        ForeignKey("school_classes.id"),
        nullable=False,
    )

    # --------------------------------------------------------
    # EDUCATION LEVEL
    # --------------------------------------------------------

    education_level: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # --------------------------------------------------------
    # FIELD / STREAM
    # --------------------------------------------------------

    field: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # --------------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------------

    school = relationship(
        "School",
        back_populates="students",
    )

    school_class = relationship(
        "SchoolClass",
        back_populates="students",
    )

    subjects = relationship(
        "StudentSubject",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    results = relationship(
        "Result",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    term_reports = relationship(
        "StudentTermReport",
        back_populates="student",
        cascade="all, delete-orphan",
    )


# ============================================================
# TEACHER / PRINCIPAL
# ============================================================

class Teacher(Base):

    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    school_id: Mapped[int] = mapped_column(
        ForeignKey("schools.id"),
        nullable=False,
    )

    verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # --------------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------------

    school = relationship(
        "School",
        back_populates="teachers",
    )

    approved_reports = relationship(
        "StudentTermReport",
        back_populates="approving_principal",
        foreign_keys="StudentTermReport.principal_id",
    )


# ============================================================
# SUBJECT
# ============================================================

class Subject(Base):

    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # --------------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------------

    student_subjects = relationship(
        "StudentSubject",
        back_populates="subject",
    )

    results = relationship(
        "Result",
        back_populates="subject",
    )


# ============================================================
# STUDENT SUBJECT
# ============================================================

class StudentSubject(Base):

    __tablename__ = "student_subjects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id"),
        nullable=False,
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id"),
        nullable=False,
    )

    academic_term_id: Mapped[int] = mapped_column(
        ForeignKey("academic_terms.id"),
        nullable=False,
    )

    # --------------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------------

    student = relationship(
        "Student",
        back_populates="subjects",
    )

    subject = relationship(
        "Subject",
        back_populates="student_subjects",
    )

    academic_term = relationship(
        "AcademicTerm",
        back_populates="student_subjects",
    )

    # --------------------------------------------------------
    # PREVENT DUPLICATE SUBJECT REGISTRATION
    # --------------------------------------------------------

    __table_args__ = (

        UniqueConstraint(
            "student_id",
            "subject_id",
            "academic_term_id",
            name="unique_student_subject_term",
        ),
    )


# ============================================================
# RESULT
# ============================================================

class Result(Base):

    __tablename__ = "results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id"),
        nullable=False,
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id"),
        nullable=False,
    )

    academic_term_id: Mapped[int] = mapped_column(
        ForeignKey("academic_terms.id"),
        nullable=False,
    )

    # --------------------------------------------------------
    # SCORES
    # --------------------------------------------------------

    first_test: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    second_test: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    exam: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    total: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    # --------------------------------------------------------
    # GRADE
    # --------------------------------------------------------

    grade: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    # --------------------------------------------------------
    # SUBJECT POSITION
    # --------------------------------------------------------

    position: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # --------------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------------

    student = relationship(
        "Student",
        back_populates="results",
    )

    subject = relationship(
        "Subject",
        back_populates="results",
    )

    academic_term = relationship(
        "AcademicTerm",
        back_populates="results",
    )

    # --------------------------------------------------------
    # PREVENT DUPLICATE RESULT
    # --------------------------------------------------------

    __table_args__ = (

        UniqueConstraint(
            "student_id",
            "subject_id",
            "academic_term_id",
            name="unique_student_subject_result_term",
        ),
    )


# ============================================================
# STUDENT TERM REPORT
# ============================================================

class StudentTermReport(Base):

    __tablename__ = "student_term_reports"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # --------------------------------------------------------
    # STUDENT
    # --------------------------------------------------------

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id"),
        nullable=False,
    )

    # --------------------------------------------------------
    # ACADEMIC TERM
    # --------------------------------------------------------

    academic_term_id: Mapped[int] = mapped_column(
        ForeignKey("academic_terms.id"),
        nullable=False,
    )

    # ========================================================
    # TEACHER'S REMARK
    # ========================================================

    teachers_remark: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ========================================================
    # PRINCIPAL'S REMARK
    # ========================================================

    principal_remark: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ========================================================
    # YEAR AVERAGE
    # ========================================================
    #
    # Only calculated for 3rd Term.
    #
    # Formula:
    #
    # (1st Term Average
    #  + 2nd Term Average
    #  + 3rd Term Average) / 3
    #
    # ========================================================

    year_average: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # ========================================================
    # FINAL DECISION
    # ========================================================
    #
    # Examples:
    #
    # PASS
    # FAIL
    # ========================================================

    final_decision: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # ========================================================
    # PRINCIPAL APPROVAL
    # ========================================================

    principal_approved: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ========================================================
    # PRINCIPAL ID
    # ========================================================

    principal_id: Mapped[int | None] = mapped_column(
        ForeignKey("teachers.id"),
        nullable=True,
    )

    # ========================================================
    # APPROVAL DATE
    # ========================================================

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # ========================================================
    # PUBLISHED
    # ========================================================
    #
    # A student cannot download/view the official report
    # until the principal has approved and published it.
    #
    # ========================================================

    published: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ========================================================
    # RELATIONSHIPS
    # ========================================================

    student = relationship(
        "Student",
        back_populates="term_reports",
    )

    academic_term = relationship(
        "AcademicTerm",
        back_populates="term_reports",
    )

    approving_principal = relationship(
        "Teacher",
        back_populates="approved_reports",
        foreign_keys=[principal_id],
    )

    # ========================================================
    # PREVENT DUPLICATE REPORT
    # ========================================================

    __table_args__ = (

        UniqueConstraint(
            "student_id",
            "academic_term_id",
            name="unique_student_term_report",
        ),
    )
