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

    response = supabase.auth.sign_in_with_password(
        {
            "email": email.strip().lower(),
            "password": password,
        }
    )

    return response


# ============================================================
# ADMIN LOGOUT
# ============================================================

def logout_user():

    supabase = get_supabase_client()

    supabase.auth.sign_out()


# ============================================================
# CURRENT AUTHENTICATED USER
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
# SCHOOL ACCESS
# ============================================================
#
# A school does NOT create an account.
#
# The school must:
#
# 1. Register
# 2. Wait for admin verification
# 3. Be approved
# 4. Be active
# 5. Use its registration number to access the portal
#
# ============================================================

def get_school_by_registration_number(
    registration_number
):

    supabase = get_supabase_client()

    registration_number = (
        registration_number
        .strip()
    )

    if not registration_number:

        return None

    response = (
        supabase
        .table("schools")
        .select(
            """
            id,
            name,
            registration_number,
            local_government,
            state,
            address,
            phone,
            email,
            motto,
            logo_url,
            ministry_certificate_url,
            verification_status,
            is_active,
            lga_id,
            administrative_area_id,
            created_at,
            updated_at
            """
        )
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

    school = data[0]

    # --------------------------------------------------------
    # Return a consistent school object
    # --------------------------------------------------------

    return {
        "school_id": school["id"],
        "school_name": school["name"],
        "registration_number":
            school["registration_number"],
        "local_government":
            school["local_government"],
        "state":
            school["state"],
        "address":
            school["address"],
        "phone":
            school["phone"],
        "email":
            school["email"],
        "motto":
            school["motto"],
        "logo_url":
            school["logo_url"],
        "ministry_certificate_url":
            school["ministry_certificate_url"],
        "verification_status":
            school["verification_status"],
        "is_active":
            school["is_active"],
        "lga_id":
            school["lga_id"],
        "administrative_area_id":
            school["administrative_area_id"],
    }


# ============================================================
# CHECK SCHOOL STATUS
# ============================================================

def get_school_status(registration_number):

    supabase = get_supabase_client()

    registration_number = (
        registration_number
        .strip()
    )

    if not registration_number:

        return None

    response = (
        supabase
        .table("schools")
        .select(
            """
            id,
            name,
            registration_number,
            verification_status,
            is_active
            """
        )
        .eq(
            "registration_number",
            registration_number
        )
        .limit(1)
        .execute()
    )

    data = response.data or []

    if not data:

        return None

    return data[0]


# ============================================================
# SCHOOL SESSION
# ============================================================

def create_school_session(school):

    return {
        "id": None,

        "school_id":
            school["school_id"],

        "full_name":
            school["school_name"],

        "role":
            "school_admin",

        "is_active":
            True,

        "school": {
            "id":
                school["school_id"],

            "name":
                school["school_name"],

            "registration_number":
                school["registration_number"],

            "state":
                school["state"],

            "local_government":
                school["local_government"],

            "address":
                school["address"],

            "phone":
                school["phone"],

            "email":
                school["email"],

            "motto":
                school["motto"],

            "logo_url":
                school["logo_url"],

            "ministry_certificate_url":
                school[
                    "ministry_certificate_url"
                ],

            "verification_status":
                school[
                    "verification_status"
                ],

            "is_active":
                school["is_active"],

            "lga_id":
                school["lga_id"],

            "administrative_area_id":
                school[
                    "administrative_area_id"
                ],
        },
    }
