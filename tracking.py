import streamlit as st

from database.db import get_complaint


def tracking_page():

    st.title("🔍 Track Complaint")

    st.write(
        "Enter your complaint ID to check the current status of your complaint."
    )

    complaint_id = st.text_input(
        "Complaint ID",
        placeholder="Example: CMP-A82F19CD"
    )

    if st.button("🔎 Track Complaint", use_container_width=True):

        if not complaint_id:
            st.warning("⚠️ Please enter your complaint ID.")
            return

        complaint_id = complaint_id.strip().upper()

        complaint = get_complaint(complaint_id)

        if complaint is None:

            st.error(
                "❌ Complaint not found. Please check your Complaint ID."
            )

            return

        # Database columns:
        # 0  = id
        # 1  = complaint_id
        # 2  = student_name
        # 3  = email
        # 4  = title
        # 5  = description
        # 6  = category
        # 7  = priority
        # 8  = department
        # 9  = status
        # 10 = image_path
        # 11 = created_at

        (
            db_id,
            complaint_id,
            student_name,
            email,
            title,
            description,
            category,
            priority,
            department,
            status,
            image_path,
            created_at
        ) = complaint

        st.success("✅ Complaint found!")

        st.subheader("📋 Complaint Details")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Complaint ID:** `{complaint_id}`")
            st.write(f"**Title:** {title}")
            st.write(f"**Category:** {category}")
            st.write(f"**Priority:** {priority}")

        with col2:
            st.write(f"**Department:** {department}")
            st.write(f"**Status:** {status}")
            st.write(f"**Submitted:** {created_at}")

        st.divider()

        st.subheader("📝 Description")

        st.write(description)

        # Show complaint status
        st.subheader("📊 Current Status")

        if status == "Pending":
            st.info("🕐 Your complaint is waiting to be processed.")

        elif status == "In Progress":
            st.warning(
                "🔧 Your complaint is currently being worked on."
            )

        elif status == "Resolved":
            st.success(
                "✅ Your complaint has been resolved."
            )

        elif status == "Rejected":
            st.error(
                "❌ Your complaint has been rejected."
            )

        # Show image if available
        if image_path and image_path.strip():

            st.divider()

            st.subheader("📷 Complaint Image")

            try:
                st.image(
                    image_path,
                    caption="Uploaded Complaint Image",
                    use_container_width=True
                )

            except Exception:
                st.warning("⚠️ Complaint image could not be displayed.")