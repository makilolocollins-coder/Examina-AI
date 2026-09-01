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
# TEST CONNECTION
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
# GET LGAS
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
# REGISTER SCHOOL
# ============================================================

def create_school(
    name,
    registration_number,
    state,
    local_government,
    lga_id,
    address="",
    phone="",
    email="",
    motto="",
):

    supabase = get_db()

    school_data = {
        "name": name,
        "registration_number": registration_number,
        "state": state,
        "local_government": local_government,
        "lga_id": lga_id,
        "address": address,
        "phone": phone,
        "email": email,
        "motto": motto,
        "verification_status": "pending",
        "is_active": True,
    }

    response = (
        supabase
        .table("schools")
        .insert(school_data)
        .execute()
    )

    return response.data or []


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
