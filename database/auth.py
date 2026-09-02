# ============================================================
# EXAMINA AI
# AUTHENTICATION SERVICE
# ============================================================

from database.supabase_client import get_supabase_client


# ============================================================
# ADMIN LOGIN
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

    try:
        supabase.auth.sign_out()
    except Exception:
        pass


# ============================================================
# CURRENT AUTH USER
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
# ADMIN PROFILE
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
# SCHOOL ACCESS BY REGISTRATION NUMBER
# ============================================================

def get_school_by_registration_number(
    registration_number
):

    supabase = get_supabase_client()

    response = supabase.rpc(
        "get_school_by_registration_number",
        {
            "p_registration_number":
                registration_number.strip(),
        }
    ).execute()

    data = response.data or []

    if not data:
        return None

    return data[0]


# ============================================================
# SCHOOL LOGOUT
# ============================================================

def logout_school():

    return None
