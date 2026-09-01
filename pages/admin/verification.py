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
        .eq(
            "verification_status",
            "pending"
        )
        .order(
            "created_at",
            desc=False
        )
        .execute()
    )

    return response.data or []


# ============================================================
# UPDATE SCHOOL STATUS
# ============================================================

def update_school_status(school_id, status):

    supabase = get_supabase_client()

    st.write("SCHOOL ID:", repr(school_id))
    st.write("STATUS:", repr(status))
    st.write("STATUS TYPE:", type(status))

    # First READ the exact row
    before = (
        supabase
        .table("schools")
        .select("id,name,verification_status,is_active")
        .eq("id", school_id)
        .single()
        .execute()
    )

    st.write("BEFORE UPDATE:", before.data)

    # Update ONLY verification_status
    response = (
        supabase
        .table("schools")
        .update({
            "verification_status": "approved"
        })
        .eq("id", school_id)
        .execute()
    )

    st.write("AFTER UPDATE:", response.data)

    return response.data

        response = (
            supabase
            .table("schools")
            .update({
                "verification_status": "approved",
                "is_active": True,
            })
            .eq(
                "id",
                school_id
            )
            .execute()
        )

        return response.data

    if status == "rejected":

        response = (
            supabase
            .table("schools")
            .update({
                "verification_status": "rejected",
                "is_active": False,
            })
            .eq(
                "id",
                school_id
            )
            .execute()
        )

        return response.data

    raise ValueError(
        "Invalid school verification status."
    )


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

    schools = get_pending_schools()

    # ========================================================
    # NO PENDING SCHOOLS
    # ========================================================

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

    # ========================================================
    # SCHOOL LIST
    # ========================================================

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
                    "**Status:** PENDING"
                )

            # =================================================
            # DOCUMENTS
            # =================================================

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

            # =================================================
            # ACTION BUTTONS
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
                            "approved"
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


# ============================================================
# PAGE ENTRY
# ============================================================

if __name__ == "__main__":

    show_verification()
