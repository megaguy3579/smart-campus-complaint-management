import streamlit as st
import os
import uuid
from datetime import datetime

from database.db import add_complaint
from utils.classifier import detect_category, detect_priority


UPLOAD_FOLDER = "uploads"

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def assign_department(category):
    """Assign complaint to the appropriate department."""

    departments = {
        "Wi-Fi / Internet": "IT Department",
        "Electrical": "Electrical Department",
        "Classroom Equipment": "IT / Lab Support",
        "Sanitation": "Housekeeping",
        "Plumbing": "Maintenance",
        "Infrastructure": "Civil / Maintenance",
        "Security": "Security Department",
        "General": "Administration"
    }

    return departments.get(category, "Administration")


def student_page():

    # -----------------------------------------
    # PAGE HEADER
    # -----------------------------------------

    st.title("📝 Submit a Complaint")

    st.write(
        "Report any problem or issue on campus."
    )

    # -----------------------------------------
    # GET LOGGED-IN USER
    # -----------------------------------------

    user = st.session_state.get("user", {})

    student_name = user.get("name", "")
    email = user.get("email", "")

    # -----------------------------------------
    # STUDENT INFORMATION
    # -----------------------------------------

    st.subheader("👤 Student Information")

    st.text_input(
        "Student Name",
        value=student_name,
        disabled=True
    )

    st.text_input(
        "Email",
        value=email,
        disabled=True
    )

    # -----------------------------------------
    # COMPLAINT FORM
    # -----------------------------------------

    st.subheader("📋 Complaint Details")

    title = st.text_input(
        "Complaint Title",
        placeholder="Example: Wi-Fi not working in Block B"
    )

    description = st.text_area(
        "Complaint Description",
        placeholder="Describe the problem in detail...",
        height=150
    )

    # -----------------------------------------
    # IMAGE UPLOAD
    # -----------------------------------------

    uploaded_image = st.file_uploader(
        "📷 Upload Complaint Image (Optional)",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image:

        st.image(
            uploaded_image,
            caption="Uploaded Complaint Image",
            width="stretch"
        )

    # -----------------------------------------
    # SUBMIT BUTTON
    # -----------------------------------------

    if st.button(
        "🚀 Submit Complaint",
        use_container_width=True
    ):

        # Validate fields
        if not student_name:

            st.error(
                "❌ Student information not found. Please login again."
            )
            return

        if not title:

            st.warning(
                "⚠️ Please enter a complaint title."
            )
            return

        if not description:

            st.warning(
                "⚠️ Please describe the complaint."
            )
            return

        # -------------------------------------
        # COMBINE TEXT
        # -------------------------------------

        complaint_text = (
            title + " " + description
        )

        # -------------------------------------
        # AI / SMART CLASSIFICATION
        # -------------------------------------

        category = detect_category(
            complaint_text
        )

        priority = detect_priority(
            complaint_text
        )

        department = assign_department(
            category
        )

        # -------------------------------------
        # GENERATE COMPLAINT ID
        # -------------------------------------

        complaint_id = (
            "CMP-" + uuid.uuid4().hex[:8].upper()
        )

        # -------------------------------------
        # SAVE IMAGE
        # -------------------------------------

        image_path = ""

        if uploaded_image:

            file_extension = os.path.splitext(
                uploaded_image.name
            )[1]

            image_filename = (
                complaint_id + file_extension
            )

            image_path = os.path.join(
                UPLOAD_FOLDER,
                image_filename
            )

            with open(
                image_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_image.getbuffer()
                )

        # -------------------------------------
        # CURRENT TIME
        # -------------------------------------

        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # -------------------------------------
        # SAVE COMPLAINT
        # -------------------------------------

        add_complaint(
            complaint_id,
            student_name,
            email,
            title,
            description,
            category,
            priority,
            department,
            image_path,
            created_at
        )

        # -------------------------------------
        # SUCCESS MESSAGE
        # -------------------------------------

        st.success(
            "✅ Complaint submitted successfully!"
        )

        st.balloons()

        # -------------------------------------
        # SHOW RESULT
        # -------------------------------------

        st.subheader(
            "🎫 Complaint Information"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Complaint ID",
                complaint_id
            )

        with col2:

            st.metric(
                "Category",
                category
            )

        with col3:

            st.metric(
                "Priority",
                priority
            )

        st.info(
            f"🏢 Assigned Department: **{department}**"
        )

        st.warning(
            "📌 Please save your Complaint ID so you can track your complaint."
        )