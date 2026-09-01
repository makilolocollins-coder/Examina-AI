# ============================================================
# EXAMINA AI
# AUTHENTICATION SERVICE
# ============================================================

from database.supabase_client import get_supabase_client


# ============================================================
# LOGIN
# ============================================================

def login_user(email, password):

    supabase = get_supabase_client()

    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password,
    })

    return response


# ============================================================
# LOGOUT
# ============================================================

def logout_user():

    supabase = get_supabase_client()

    supabase.auth.sign_out()


# ============================================================
# CURRENT USER
# ============================================================

def get_current_user():

    supabase = get_supabase_client()

    try:
        response = supabase.auth.get_user()

        if response and response.user:
            return response.user

    except Exception:
        pass

    return None


# ============================================================
# CHECK ADMIN
# ============================================================

def get_admin_profile(user_id):

    supabase = get_supabase_client()

    response = (
        supabase
        .table("admin_users")
        .select("*")
        .eq("id", user_id)
        .eq("is_active", True)
        .limit(1)
        .execute()
    )

    data = response.data or []

    return data[0] if data else None


# ============================================================
# CHECK SCHOOL USER
# ============================================================

def get_school_user_profile(user_id):

    supabase = get_supabase_client()

    response = (
        supabase
        .table("school_users")
        .select(
            "*, schools(*)"
        )
        .eq("id", user_id)
        .eq("is_active", True)
        .limit(1)
        .execute()
    )

    data = response.data or []

    return data[0] if data else None
