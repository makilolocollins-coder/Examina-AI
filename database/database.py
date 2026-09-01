# ============================================================
# EXAMINA AI
# DATABASE SERVICE
# ============================================================

from database.supabase_client import get_supabase_client


# ============================================================
# DATABASE CLIENT
# ============================================================

def get_db():
    return get_supabase_client()


# ============================================================
# TEST DATABASE CONNECTION
# ============================================================

def test_database_connection():

    try:
        supabase = get_db()

        response = (
            supabase
            .table("states")
            .select("id")
            .limit(1)
            .execute()
        )

        return True, response.data

    except Exception as error:
        return False, str(error)


# ============================================================
# GET STATES
# ============================================================

def get_states():

    supabase = get_db()

    response = (
        supabase
        .table("states")
        .select("id,name,code")
        .order("name")
        .execute()
    )

    return response.data or []


# ============================================================
# GET LGAs
# ============================================================

def get_lgas(state_id):

    supabase = get_db()

    response = (
        supabase
        .table("local_governments")
        .select("id,name,code,state_id")
        .eq("state_id", state_id)
        .order("name")
        .execute()
    )

    return response.data or []


# ============================================================
# CHECK SCHOOL REGISTRATION NUMBER
# ============================================================

def school_exists(registration_number):

    supabase = get_db()

    response = (
        supabase
        .table("schools")
        .select("id")
        .eq(
            "registration_number",
            registration_number
        )
        .limit(1)
        .execute()
    )

    return bool(response.data)


# ============================================================
# CREATE SCHOOL
# ============================================================

def create_school(
    name,
    registration_number,
    local_government,
    state,
    address="",
    phone="",
    email="",
    motto="",
    logo_url=None,
    ministry_certificate_url=None,
    verification_status="pending",
    is_active=False,
    lga_id=None,
    administrative_area_id=None,
):

    supabase = get_db()

    school_data = {
        "name": name,
        "registration_number": registration_number,
        "local_government": local_government,
        "state": state,
        "address": address or None,
        "phone": phone or None,
        "email": email or None,
        "motto": motto or None,
        "logo_url": logo_url,
        "ministry_certificate_url": ministry_certificate_url,
        "verification_status": verification_status,
        "is_active": is_active,
        "lga_id": lga_id,
        "administrative_area_id": administrative_area_id,
    }

    response = (
        supabase
        .table("schools")
        .insert(school_data)
        .execute()
    )

    return response.data


# ============================================================
# GET SCHOOL
# ============================================================

def get_school(school_id):

    supabase = get_db()

    response = (
        supabase
        .table("schools")
        .select("*")
        .eq("id", school_id)
        .limit(1)
        .execute()
    )

    data = response.data or []

    if not data:
        return None

    return data[0]
