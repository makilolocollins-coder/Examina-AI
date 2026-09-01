# ============================================================
# EXAMINA AI
# DATABASE SERVICE
# ============================================================

from database.supabase_client import get_supabase_client


# ============================================================
# GET SUPABASE
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
# GET LGAS BY STATE
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
