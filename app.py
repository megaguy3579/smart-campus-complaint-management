import streamlit as st

from database.db import init_database
from utils.auth import show_login, logout_user
from views.student import student_page
from views.tracking import tracking_page
from views.admin import admin_page


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="Smart Campus Complaint System",
    page_icon="🏫",
    layout="wide"
)


# -----------------------------------
# INITIALIZE DATABASE
# -----------------------------------

init_database()


# -----------------------------------
# INITIALIZE SESSION STATE
# -----------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# -----------------------------------
# LOGIN CHECK
# -----------------------------------

if not st.session_state.logged_in:

    show_login()

    st.stop()


# -----------------------------------
# CURRENT USER
# -----------------------------------

user = st.session_state.user


# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("🏫 Smart Campus")

st.sidebar.success(
    f"Logged in as\n\n{user['name']}"
)

st.sidebar.write(
    f"Role: **{user['role'].title()}**"
)

st.sidebar.divider()


# -----------------------------------
# STUDENT NAVIGATION
# -----------------------------------

if user["role"] == "student":

    page = st.sidebar.radio(
        "Navigation",
        [
            "Submit Complaint",
            "Track Complaint"
        ]
    )

    if page == "Submit Complaint":

        student_page()

    elif page == "Track Complaint":

        tracking_page()


# -----------------------------------
# ADMIN NAVIGATION
# -----------------------------------

elif user["role"] == "admin":

    page = st.sidebar.radio(
        "Navigation",
        [
            "Admin Dashboard"
        ]
    )

    if page == "Admin Dashboard":

        admin_page()


# -----------------------------------
# LOGOUT
# -----------------------------------

st.sidebar.divider()

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    logout_user()

    st.rerun()