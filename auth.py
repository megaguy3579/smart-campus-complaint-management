import streamlit as st

from database.db import (
    register_user,
    authenticate_user
)


def logout_user():
    """Log the current user out."""

    st.session_state.logged_in = False
    st.session_state.user = None


def show_login():

    st.set_page_config(
        page_title="Smart Campus Login",
        page_icon="🏫",
        layout="centered"
    )

    st.title("🏫 Smart Campus")
    st.subheader("🔐 Login")

    st.write(
        "Sign in to access the Smart Campus Complaint System."
    )

    login_tab, register_tab = st.tabs([
        "🔑 Login",
        "📝 Student Registration"
    ])

    # -----------------------------------------
    # LOGIN
    # -----------------------------------------

    with login_tab:

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "🔑 Login",
            use_container_width=True
        ):

            if not email or not password:

                st.warning(
                    "⚠️ Please enter your email and password."
                )

            else:

                user = authenticate_user(
                    email,
                    password
                )

                if user is None:

                    st.error(
                        "❌ Invalid email or password."
                    )

                else:

                    st.session_state.logged_in = True
                    st.session_state.user = user

                    st.success(
                        "✅ Login successful!"
                    )

                    st.rerun()

    # -----------------------------------------
    # REGISTRATION
    # -----------------------------------------

    with register_tab:

        st.write(
            "Create a student account."
        )

        name = st.text_input(
            "Full Name",
            placeholder="Enter your name",
            key="register_name"
        )

        new_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="register_email"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Enter password again",
            key="confirm_password"
        )

        if st.button(
            "📝 Create Student Account",
            use_container_width=True
        ):

            if not name or not new_email or not new_password:
                st.warning(
                    "⚠️ Please fill in all fields."
                )

            elif "@" not in new_email:
                st.warning(
                    "⚠️ Please enter a valid email address."
                )

            elif len(new_password) < 6:
                st.warning(
                    "⚠️ Password must contain at least 6 characters."
                )

            elif new_password != confirm_password:
                st.error(
                    "❌ Passwords do not match."
                )

            else:

                success = register_user(
                    name,
                    new_email,
                    new_password
                )

                if success:

                    st.success(
                        "✅ Account created successfully! "
                        "You can now login."
                    )

                else:

                    st.error(
                        "❌ An account with this email already exists."
                    )

    st.divider()

    st.caption("Hackathon Admin Account")

    st.write(
        "👨‍💼 Email: `admin@campus.com`"
    )

    st.write(
        "🔑 Password: `admin123`"
    )