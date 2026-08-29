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
#
# Example:
#
# 2026/2027
#
# One academic session contains three terms:
#
# 1st Term
# 2nd Term
# 3rd Term
#
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
    # RELATIONSHIP TO TERMS
    # --------------------------------------------------------

    terms = relationship(
        "AcademicTerm",
        back_populates="academic_session",
        cascade="all, delete-orphan",
    )


# ============================================================
# ACADEMIC TERM
# ============================================================
#
# Each academic session has:
#
# 1st Term
# 2nd Term
# 3rd Term
#
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

    # --------------------------------------------------------
    # PREVENT DUPLICATE TERMS
    # --------------------------------------------------------

    __table_args__ = (
        UniqueConstraint(
            "academic_session_id",
            "name",
            name="unique_term_per_session",
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

    school = relationship(
        "School",
        back_populates="classes",
    )

    students = relationship(
        "Student",
        back_populates="school_class",
    )

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
    # --------------------------------------------------------
    #
    # No class_name here.
    #
    # The class is obtained through:
    #
    # student.school_class.name
    #
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
    #
    # Examples:
    #
    # Science
    # Humanities
    # Business
    #
    # Can be NULL for Primary and JSS.
    #
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


# ============================================================
# TEACHER
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

    school = relationship(
        "School",
        back_populates="teachers",
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
#
# Records which subjects a student takes in a particular term.
#
# Example:
#
# Student: John
# Session: 2026/2027
# Term: 1st Term
# Subject: Mathematics
#
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
    # PREVENT DUPLICATES
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
#
# Each result belongs to:
#
# Student
# Subject
# Academic Term
#
# Example:
#
# John
# Mathematics
# 2026/2027
# 1st Term
#
# First Test = 18
# Second Test = 17
# Exam = 55
# Total = 90
# Grade = A
# Position = 2
#
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
    # GRADE AND POSITION
    # --------------------------------------------------------

    grade: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

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
