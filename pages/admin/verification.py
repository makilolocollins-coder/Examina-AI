# ============================================================
# EXAMINA AI
# ADMIN — SCHOOL VERIFICATION
# ============================================================

import streamlit as st

from database.supabase_client import get_supabase_client


# ============================================================
# SECURITY CHECK
# ============================================================

def check_admin_access():

    admin = st.session_state.get("admin_user")

    if not admin:
        st.error("Unauthorized access.")
        st.stop()

    if not admin.get("is_active", False):
        st.error("Your admin account is inactive.")
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
            "id,name,registration_number,"
            "local_government,state,address,phone,"
            "email,motto,logo_url,"
            "ministry_certificate_url,"
            "verification_status,is_active,created_at"
        )
        .eq("verification_status", "pending")
        .order("created_at", desc=False)
        .execute()
    )

    return response.data or []


# ============================================================
# UPDATE SCHOOL STATUS
# ============================================================

def update_school_status(
    school_id,
    status
):

    supabase = get_supabase_client()

    if status == "verified":

        response = (
            supabase
            .table("schools")
            .update({
                "verification_status": "verified",
                "is_active": True,
            })
            .eq("id", school_id)
            .execute()
        )

    elif status == "rejected":

        response = (
            supabase
            .table("schools")
            .update({
                "verification_status": "rejected",
                "is_active": False,
            })
            .eq("id", school_id)
            .execute()
        )

    else:

        raise ValueError(
            "Invalid verification status."
        )

    return response.data


# ============================================================
# ADMIN VERIFICATION PAGE
# ============================================================

def show_verification():

    admin = check_admin_access()

    st.title("School Verification")

    st.caption(
        "Review and verify schools registered on Examina AI."
    )

    st.divider()

    pending_schools = get_pending_schools()

    # ========================================================
    # NO PENDING SCHOOLS
    # ========================================================

    if not pending_schools:

        st.success(
            "There are no schools waiting for verification."
        )

        return

    # ========================================================
    # SUMMARY
    # ========================================================

    st.metric(
        "Schools Awaiting Verification",
        len(pending_schools)
    )

    st.divider()

    # ========================================================
    # DISPLAY SCHOOLS
    # ========================================================

    for school in pending_schools:

        school_id = school["id"]

        with st.container(border=True):

            st.subheader(
                school.get("name", "Unnamed School")
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
                    "**Status:** `PENDING`"
                )

            # =================================================
            # DOCUMENTS
            # =================================================

            st.divider()

            st.write("### Registration Documents")

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

                st.warning(
                    "No ministry certificate uploaded."
                )

            if logo_url:

                st.link_button(
                    "View School Logo",
                    logo_url,
                    use_container_width=True
                )

            # =================================================
            # ACTIONS
            # =================================================

            st.divider()

            approve_col, reject_col = st.columns(2)

            with approve_col:

                if st.button(
                    "Approve School",
                    key=f"approve_{school_id}",
                    type="primary",
                    use_container_width=True,
                ):

                    try:

                        update_school_status(
                            school_id,
                            "verified"
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
                    use_container_width=True,
                ):

                    try:

                        update_school_status(
                            school_id,
                            "rejected"
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
