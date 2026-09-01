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

    supabase.auth.sign_out()


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
# SCHOOL USER PROFILE
# ============================================================

def get_school_user_profile(user_id):

    supabase = get_supabase_client()

    response = (
        supabase
        .table("school_users")
        .select("id,school_id,full_name,role,is_active")
        .eq("id", user_id)
        .eq("is_active", True)
        .limit(1)
        .execute()
    )

    data = response.data or []

    if not data:
        return None

    profile = data[0]

    school_response = (
        supabase
        .table("schools")
        .select("*")
        .eq("id", profile["school_id"])
        .eq("verification_status", "approved")
        .eq("is_active", True)
        .limit(1)
        .execute()
    )

    schools = school_response.data or []

    if not schools:
        return None

    profile["school"] = schools[0]

    return profile


# ============================================================
# SCHOOL ACCOUNT ELIGIBILITY
# ============================================================

def get_school_account_eligibility(
    registration_number,
    email
):

    supabase = get_supabase_client()

    response = supabase.rpc(
        "get_school_account_eligibility",
        {
            "p_registration_number": registration_number.strip(),
            "p_email": email.strip().lower(),
        }
    ).execute()

    data = response.data or []

    if not data:
        return None

    return data[0]


# ============================================================
# SCHOOL ACCOUNT CREATION
# ============================================================

def create_school_account(
    email,
    password,
    school_id,
    full_name
):

    supabase = get_supabase_client()

    response = supabase.auth.sign_up({
        "email": email.strip().lower(),
        "password": password,
        "options": {
            "data": {
                "account_type": "school",
                "school_id": school_id,
                "full_name": full_name.strip(),
            }
        }
    })

    return response


# ============================================================
# SCHOOL LOGIN
# ============================================================

def login_school(email, password):

    supabase = get_supabase_client()

    response = supabase.auth.sign_in_with_password({
        "email": email.strip().lower(),
        "password": password,
    })

    return response
