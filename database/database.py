# ============================================================
# EXAMINA AI
# DATABASE SERVICE
# ============================================================

from database.supabase_client import get_supabase_client


# ============================================================
# GET DATABASE CLIENT
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
# GET LGAS
# ============================================================

def get_lgas(state_id):

    supabase = get_db()

    response = (
        supabase
        .table("local_governments")
        .select(
            "id,name,code,state_id"
        )
        .eq(
            "state_id",
            state_id
        )
        .order("name")
        .execute()
    )

    return response.data or []


# ============================================================
# REGISTER SCHOOL
# ============================================================

def create_school(
    name,
    short_name,
    school_type,
    state_id,
    lga_id,
    address,
    phone,
    email,
):

    supabase = get_db()

    school_data = {
        "name": name,
        "short_name": short_name,
        "school_type": school_type,
        "state_id": state_id,
        "lga_id": lga_id,
        "address": address,
        "phone": phone,
        "email": email,
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
        .eq(
            "id",
            school_id
        )
        .limit(1)
        .execute()
    )

    data = response.data or []

    if not data:
        return None

    return data[0]
