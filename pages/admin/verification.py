# ============================================================
# EXAMINA AI
# ADMIN — SCHOOL VERIFICATION
# ============================================================

import streamlit as st

from database.supabase_client import get_supabase_client


# ============================================================
# ADMIN ACCESS
# ============================================================

def check_admin_access():

    admin = st.session_state.get("admin_user")

    if not admin:
        st.error("Unauthorized access.")
        st.stop()

    if not admin.get("is_active", False):
        st.error("Admin account is inactive.")
        st.stop()

    return admin


# ============================================================
# GET PENDING SCHOOLS
# ============================================================

def get_pending_schools():

    supabase = get_supabase_client()

    response = (
        supabase
        .table("schools")
        .select(
            "id,"
            "name,"
            "registration_number,"
            "local_government,"
            "state,"
            "address,"
            "phone,"
            "email,"
            "motto,"
            "logo_url,"
            "ministry_certificate_url,"
            "verification_status,"
            "is_active,"
            "created_at"
        )
        .eq("verification_status", "pending")
        .order("created_at", desc=False)
        .execute()
    )

    return response.data or []


# ============================================================
# APPROVE SCHOOL — DIAGNOSTIC VERSION
# ============================================================

def approve_school(school_id):

    supabase = get_supabase_client()

    # Read the school first
    before_response = (
        supabase
        .table("schools")
        .select(
            "id,name,verification_status,is_active"
        )
        .eq("id", school_id)
        .single()
        .execute()
    )

    st.write(
        "BEFORE UPDATE:",
        before_response.data
    )

    # Force the exact value allowed by the database
    payload = {
        "verification_status": "approved"
    }

    st.write(
        "PAYLOAD:",
        payload
    )

    # Perform the update
    response = (
        supabase
        .table("schools")
        .update(payload)
        .eq("id", school_id)
        .execute()
    )

    st.write(
        "AFTER UPDATE:",
        response.data
    )

    return response.data


# ============================================================
# REJECT SCHOOL
# ============================================================

def reject_school(school_id):

    supabase = get_supabase_client()

    response = (
        supabase
        .table("schools")
        .update(
            {
                "verification_status": "rejected",
                "is_active": False
            }
        )
        .eq("id", school_id)
        .execute()
    )

    return response.data


# ============================================================
# VERIFICATION PAGE
# ============================================================

def show_verification():

    check_admin_access()

    st.title("School Verification")

    st.caption(
        "Review schools waiting for approval."
    )

    st.divider()

    try:

        schools = get_pending_schools()

    except Exception as error:

        st.error(
            f"Could not load schools: {error}"
        )

        return

    if not schools:

        st.success(
            "No schools are currently waiting for verification."
        )

        return

    st.metric(
        "Schools Awaiting Verification",
        len(schools)
    )

    st.divider()

    for school in schools:

        school_id = school["id"]

        with st.container(border=True):

            st.subheader(
                school.get(
                    "name",
                    "Unnamed School"
                )
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "**Registration Number:**",
                    school.get(
                        "registration_number",
                        "N/A"
                    )
                )

                st.write(
                    "**State:**",
                    school.get(
                        "state",
                        "N/A"
                    )
                )

                st.write(
                    "**LGA:**",
                    school.get(
                        "local_government",
                        "N/A"
                    )
                )

                st.write(
                    "**Address:**",
                    school.get(
                        "address",
                        "N/A"
                    )
                )

            with col2:

                st.write(
                    "**Phone:**",
                    school.get(
                        "phone",
                        "N/A"
                    )
                )

                st.write(
                    "**Email:**",
                    school.get(
                        "email",
                        "N/A"
                    )
                )

                st.write(
                    "**Motto:**",
                    school.get(
                        "motto",
                        "N/A"
                    )
                )

                st.write(
                    "**Status:**",
                    school.get(
                        "verification_status",
                        "N/A"
                    ).upper()
                )

            st.divider()

            st.write("### Documents")

            certificate_url = school.get(
                "ministry_certificate_url"
            )

            logo_url = school.get(
                "logo_url"
            )

            if certificate_url:

                st.link_button(
                    "View Ministry Certificate",
                    certificate_url,
                    use_container_width=True
                )

            else:

                st.info(
                    "No ministry certificate was uploaded."
                )

            if logo_url:

                st.link_button(
                    "View School Logo",
                    logo_url,
                    use_container_width=True
                )

            else:

                st.info(
                    "No school logo was uploaded."
                )

            st.divider()

            approve_col, reject_col = st.columns(2)

            with approve_col:

                if st.button(
                    "Approve School",
                    key=f"approve_{school_id}",
                    type="primary",
                    use_container_width=True
                ):

                    try:

                        approve_school(
                            school_id
                        )

                        st.success(
                            "School approved successfully."
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"Could not approve school: {error}"
                        )

            with reject_col:

                if st.button(
                    "Reject School",
                    key=f"reject_{school_id}",
                    use_container_width=True
                ):

                    try:

                        reject_school(
                            school_id
                        )

                        st.warning(
                            "School rejected."
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"Could not reject school: {error}"
                        )


# ============================================================
# PAGE ENTRY
# ============================================================

if __name__ == "__main__":

    show_verification()
