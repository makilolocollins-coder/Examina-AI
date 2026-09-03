# ============================================================
# EXAMINA AI
# AUTHENTICATION SERVICE
# ============================================================

from database.supabase_client import get_supabase_client


# ============================================================
# ADMIN AUTHENTICATION
# ============================================================

def login_user(email, password):

    supabase = get_supabase_client()

    return supabase.auth.sign_in_with_password(
        {
            "email": email.strip().lower(),
            "password": password,
        }
    )


# ============================================================
# ADMIN LOGOUT
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

    if not data:
        return None

    return data[0]


# ============================================================
# SCHOOL LOOKUP
# ============================================================
#
# Schools do NOT use Supabase Auth.
#
# Access is granted only when:
#
# registration_number matches
# AND verification_status = approved
# AND is_active = true
#
# ============================================================

def get_school_by_registration_number(
    registration_number
):

    supabase = get_supabase_client()

    registration_number = (
        registration_number.strip()
    )

    if not registration_number:
        return None

    response = (
        supabase
        .table("schools")
        .select("*")
        .eq(
            "registration_number",
            registration_number
        )
        .eq(
            "verification_status",
            "approved"
        )
        .eq(
            "is_active",
            True
        )
        .limit(1)
        .execute()
    )

    data = response.data or []

    if not data:
        return None

    return data[0]
