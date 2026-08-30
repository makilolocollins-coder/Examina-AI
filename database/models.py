from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database.database import Base


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
        String(200),
        nullable=False,
    )

    registration_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    local_government: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    school_badge: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    registration_certificate: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    academic_sessions: Mapped[list["AcademicSession"]] = relationship(
        back_populates="school",
        cascade="all, delete-orphan",
    )

    classes: Mapped[list["SchoolClass"]] = relationship(
        back_populates="school",
        cascade="all, delete-orphan",
    )

    teachers: Mapped[list["Teacher"]] = relationship(
        back_populates="school",
        cascade="all, delete-orphan",
    )

    students: Mapped[list["Student"]] = relationship(
        back_populates="school",
        cascade="all, delete-orphan",
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

    school_id: Mapped[int] = mapped_column(
        ForeignKey(
            "schools.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    curriculum_version: Mapped[str] = mapped_column(
        String(100),
        default="Nigeria Curriculum",
        nullable=False,
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    school: Mapped["School"] = relationship(
        back_populates="academic_sessions",
    )

    terms: Mapped[list["AcademicTerm"]] = relationship(
        back_populates="academic_session",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "school_id",
            "name",
            name="uq_school_academic_session",
        ),
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
        ForeignKey(
            "academic_sessions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    term_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    academic_session: Mapped["AcademicSession"] = relationship(
        back_populates="terms",
    )

    results: Mapped[list["Result"]] = relationship(
        back_populates="academic_term",
        cascade="all, delete-orphan",
    )

    reports: Mapped[list["StudentTermReport"]] = relationship(
        back_populates="academic_term",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "academic_session_id",
            "term_number",
            name="uq_session_term_number",
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

    school_id: Mapped[int] = mapped_column(
        ForeignKey(
            "schools.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    education_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    stream: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    school: Mapped["School"] = relationship(
        back_populates="classes",
    )

    students: Mapped[list["Student"]] = relationship(
        back_populates="school_class",
    )

    __table_args__ = (
        UniqueConstraint(
            "school_id",
            "name",
            name="uq_school_class",
        ),
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

    school_id: Mapped[int] = mapped_column(
        ForeignKey(
            "schools.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    employee_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    school: Mapped["School"] = relationship(
        back_populates="teachers",
    )

    __table_args__ = (
        UniqueConstraint(
            "school_id",
            "email",
            name="uq_school_teacher_email",
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

    school_id: Mapped[int] = mapped_column(
        ForeignKey(
            "schools.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    class_id: Mapped[int] = mapped_column(
        ForeignKey(
            "school_classes.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    admission_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
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

    education_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    field: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    school: Mapped["School"] = relationship(
        back_populates="students",
    )

    school_class: Mapped["SchoolClass"] = relationship(
        back_populates="students",
    )

    results: Mapped[list["Result"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
    )

    reports: Mapped[list["StudentTermReport"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "school_id",
            "admission_number",
            name="uq_school_admission_number",
        ),
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
    )

    code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    education_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    results: Mapped[list["Result"]] = relationship(
        back_populates="subject",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "education_level",
            name="uq_subject_name_education_level",
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
        ForeignKey(
            "students.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey(
            "subjects.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    academic_term_id: Mapped[int] = mapped_column(
        ForeignKey(
            "academic_terms.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    first_test: Mapped[float] = mapped_column(
        Numeric(5, 2),
        default=0,
        nullable=False,
    )

    second_test: Mapped[float] = mapped_column(
        Numeric(5, 2),
        default=0,
        nullable=False,
    )

    exam: Mapped[float] = mapped_column(
        Numeric(5, 2),
        default=0,
        nullable=False,
    )

    total: Mapped[float] = mapped_column(
        Numeric(5, 2),
        default=0,
        nullable=False,
    )

    grade: Mapped[str | None] = mapped_column(
        String(5),
        nullable=True,
    )

    position: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    student: Mapped["Student"] = relationship(
        back_populates="results",
    )

    subject: Mapped["Subject"] = relationship(
        back_populates="results",
    )

    academic_term: Mapped["AcademicTerm"] = relationship(
        back_populates="results",
    )

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "subject_id",
            "academic_term_id",
            name="uq_student_subject_term_result",
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

    student_id: Mapped[int] = mapped_column(
        ForeignKey(
            "students.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    academic_term_id: Mapped[int] = mapped_column(
        ForeignKey(
            "academic_terms.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    teachers_remark: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    principal_remark: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    principal_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "teachers.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    principal_approved: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    published: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    year_average: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    promotion_status: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    student: Mapped["Student"] = relationship(
        back_populates="reports",
    )

    academic_term: Mapped["AcademicTerm"] = relationship(
        back_populates="reports",
    )

    principal: Mapped["Teacher | None"] = relationship(
        foreign_keys=[principal_id],
    )

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "academic_term_id",
            name="uq_student_term_report",
        ),
    )
