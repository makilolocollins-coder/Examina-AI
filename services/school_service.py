# ============================================================
# EXAMINA AI
# SCHOOL SERVICE
# ============================================================
#
# This file contains the business logic for schools.
#
# app.py should NOT directly contain all the database logic.
#
# Instead:
#
# app.py
#    ↓
# school_service.py
#    ↓
# database.py
#    ↓
# models.py
#    ↓
# SQLite
#
# ============================================================


from sqlalchemy.orm import Session

from database.models import School


# ============================================================
# CREATE SCHOOL
# ============================================================

def create_school(
    db: Session,
    name: str,
    phone: str,
    local_government: str,
    state: str,
    email: str | None = None,
    registration_certificate: str | None = None,
    school_badge: str | None = None,
) -> School:
    """
    Creates a new school in the database.

    Parameters
    ----------
    db:
        Active SQLAlchemy database session.

    name:
        Registered name of the school.

    phone:
        School's phone number.

    local_government:
        Local Government Area where the school is located.

    state:
        State where the school is located.

    email:
        Optional school email.

    registration_certificate:
        Path or reference to the school's registration certificate.

    school_badge:
        Path or reference to the school's badge/logo.

    Returns
    -------
    School
        The newly created School object.
    """

    school = School(
        name=name.strip(),
        phone=phone.strip(),
        email=email.strip() if email else None,
        local_government=local_government.strip(),
        state=state.strip(),
        registration_certificate=registration_certificate,
        school_badge=school_badge,
        verified=False,
    )

    db.add(school)

    db.commit()

    db.refresh(school)

    return school


# ============================================================
# GET SCHOOL BY ID
# ============================================================

def get_school(
    db: Session,
    school_id: int,
) -> School | None:
    """
    Retrieves a school using its database ID.
    """

    return db.get(School, school_id)


# ============================================================
# GET SCHOOL BY PHONE
# ============================================================

def get_school_by_phone(
    db: Session,
    phone: str,
) -> School | None:
    """
    Finds a school using its phone number.
    """

    return (
        db.query(School)
        .filter(School.phone == phone.strip())
        .first()
    )


# ============================================================
# GET SCHOOL BY EMAIL
# ============================================================

def get_school_by_email(
    db: Session,
    email: str,
) -> School | None:
    """
    Finds a school using its email address.
    """

    return (
        db.query(School)
        .filter(School.email == email.strip())
        .first()
    )


# ============================================================
# CHECK IF SCHOOL EXISTS
# ============================================================

def school_exists(
    db: Session,
    name: str,
    phone: str,
) -> bool:
    """
    Checks whether a school with the same name and phone
    already exists.
    """

    school = (
        db.query(School)
        .filter(
            School.name == name.strip(),
            School.phone == phone.strip(),
        )
        .first()
    )

    return school is not None


# ============================================================
# UPDATE SCHOOL INFORMATION
# ============================================================

def update_school(
    db: Session,
    school_id: int,
    name: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    local_government: str | None = None,
    state: str | None = None,
) -> School | None:
    """
    Updates school information.

    Only fields supplied to the function are changed.
    """

    school = db.get(School, school_id)

    if school is None:
        return None

    if name is not None:
        school.name = name.strip()

    if phone is not None:
        school.phone = phone.strip()

    if email is not None:
        school.email = email.strip()

    if local_government is not None:
        school.local_government = local_government.strip()

    if state is not None:
        school.state = state.strip()

    db.commit()

    db.refresh(school)

    return school


# ============================================================
# UPLOAD REGISTRATION CERTIFICATE
# ============================================================

def add_registration_certificate(
    db: Session,
    school_id: int,
    certificate_reference: str,
) -> School | None:
    """
    Stores the reference/path to a school's registration
    certificate.
    """

    school = db.get(School, school_id)

    if school is None:
        return None

    school.registration_certificate = certificate_reference

    db.commit()

    db.refresh(school)

    return school


# ============================================================
# ADD SCHOOL BADGE
# ============================================================

def add_school_badge(
    db: Session,
    school_id: int,
    badge_reference: str,
) -> School | None:
    """
    Stores the reference/path to a school's badge.
    """

    school = db.get(School, school_id)

    if school is None:
        return None

    school.school_badge = badge_reference

    db.commit()

    db.refresh(school)

    return school


# ============================================================
# VERIFY SCHOOL
# ============================================================

def verify_school(
    db: Session,
    school_id: int,
) -> School | None:
    """
    Marks a school as verified.

    IMPORTANT:
    This function should only be called by an authorized
    administrator after checking the school's documents.
    """

    school = db.get(School, school_id)

    if school is None:
        return None

    school.verified = True

    db.commit()

    db.refresh(school)

    return school


# ============================================================
# UNVERIFY SCHOOL
# ============================================================

def unverify_school(
    db: Session,
    school_id: int,
) -> School | None:
    """
    Removes a school's verified status.
    """

    school = db.get(School, school_id)

    if school is None:
        return None

    school.verified = False

    db.commit()

    db.refresh(school)

    return school


# ============================================================
# CHECK VERIFICATION STATUS
# ============================================================

def is_school_verified(
    db: Session,
    school_id: int,
) -> bool:
    """
    Returns True if the school is verified.
    """

    school = db.get(School, school_id)

    if school is None:
        return False

    return school.verified


# ============================================================
# GET SCHOOLS BY LGA
# ============================================================

def get_schools_by_lga(
    db: Session,
    local_government: str,
    state: str,
) -> list[School]:
    """
    Returns schools registered in a particular LGA and state.

    This will later be useful for the Nigerian school
    directory and school verification system.
    """

    return (
        db.query(School)
        .filter(
            School.local_government == local_government.strip(),
            School.state == state.strip(),
        )
        .order_by(School.name.asc())
        .all()
    )


# ============================================================
# GET VERIFIED SCHOOLS BY LGA
# ============================================================

def get_verified_schools_by_lga(
    db: Session,
    local_government: str,
    state: str,
) -> list[School]:
    """
    Returns only verified schools within an LGA.
    """

    return (
        db.query(School)
        .filter(
            School.local_government == local_government.strip(),
            School.state == state.strip(),
            School.verified.is_(True),
        )
        .order_by(School.name.asc())
        .all()
    )


# ============================================================
# GET ALL VERIFIED SCHOOLS
# ============================================================

def get_verified_schools(
    db: Session,
) -> list[School]:
    """
    Returns all verified schools.
    """

    return (
        db.query(School)
        .filter(
            School.verified.is_(True)
        )
        .order_by(School.name.asc())
        .all()
    )


# ============================================================
# DELETE SCHOOL
# ============================================================

def delete_school(
    db: Session,
    school_id: int,
) -> bool:
    """
    Deletes a school.

    Returns:
        True  → school deleted
        False → school not found
    """

    school = db.get(School, school_id)

    if school is None:
        return False

    db.delete(school)

    db.commit()

    return True
