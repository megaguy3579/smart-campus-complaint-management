import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from database.db import (
    get_all_complaints,
    update_complaint_status
)


# -----------------------------------------
# SLA RULES
# -----------------------------------------

SLA_HOURS = {
    "Critical": 2,
    "High": 6,
    "Medium": 24,
    "Low": 72
}


def get_sla_deadline(created_at, priority):
    """Calculate SLA deadline."""

    try:
        created_time = datetime.strptime(
            created_at,
            "%Y-%m-%d %H:%M:%S"
        )

        hours = SLA_HOURS.get(
            priority,
            72
        )

        return created_time + timedelta(
            hours=hours
        )

    except Exception:
        return None


def is_overdue(created_at, priority, status):
    """Check whether a complaint has breached its SLA."""

    if status in ["Resolved", "Rejected"]:
        return False

    deadline = get_sla_deadline(
        created_at,
        priority
    )

    if deadline is None:
        return False

    return datetime.now() > deadline


def admin_page():

    st.title("📊 Smart Campus Admin Dashboard")

    st.write(
        "Monitor, prioritize, and resolve campus complaints."
    )

    # -----------------------------------------
    # GET COMPLAINTS
    # -----------------------------------------

    complaints = get_all_complaints()

    if not complaints:

        st.info(
            "📭 No complaints have been submitted yet."
        )

        return

    # -----------------------------------------
    # DATAFRAME
    # -----------------------------------------

    columns = [
        "id",
        "complaint_id",
        "student_name",
        "email",
        "title",
        "description",
        "category",
        "priority",
        "department",
        "status",
        "image_path",
        "created_at"
    ]

    df = pd.DataFrame(
        complaints,
        columns=columns
    )

    # -----------------------------------------
    # SLA CALCULATION
    # -----------------------------------------

    df["overdue"] = df.apply(
        lambda row: is_overdue(
            row["created_at"],
            row["priority"],
            row["status"]
        ),
        axis=1
    )

    # -----------------------------------------
    # METRICS
    # -----------------------------------------

    total = len(df)

    pending = len(
        df[df["status"] == "Pending"]
    )

    in_progress = len(
        df[df["status"] == "In Progress"]
    )

    resolved = len(
        df[df["status"] == "Resolved"]
    )

    critical = len(
        df[df["priority"] == "Critical"]
    )

    overdue = int(
        df["overdue"].sum()
    )

    # -----------------------------------------
    # DASHBOARD CARDS
    # -----------------------------------------

    st.subheader("📈 Complaint Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📋 Total Complaints",
            total
        )

    with col2:
        st.metric(
            "⏳ Pending",
            pending
        )

    with col3:
        st.metric(
            "🔧 In Progress",
            in_progress
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            "✅ Resolved",
            resolved
        )

    with col5:
        st.metric(
            "🚨 Critical",
            critical
        )

    with col6:
        st.metric(
            "⚠️ SLA Breached",
            overdue
        )

    # -----------------------------------------
    # SLA ALERT
    # -----------------------------------------

    if overdue > 0:

        st.error(
            f"🚨 **{overdue} complaint(s) have breached their SLA!** "
            "Immediate attention is required."
        )

    else:

        st.success(
            "✅ No active complaints have breached their SLA."
        )

    st.divider()

    # -----------------------------------------
    # ANALYTICS
    # -----------------------------------------

    st.subheader("📊 Complaint Analytics")

    col1, col2 = st.columns(2)

    with col1:

        st.write("### 🏷️ By Category")

        category_counts = (
            df["category"]
            .value_counts()
        )

        st.bar_chart(
            category_counts
        )

    with col2:

        st.write("### 🚦 By Priority")

        priority_counts = (
            df["priority"]
            .value_counts()
        )

        st.bar_chart(
            priority_counts
        )

    st.write("### 🏢 By Department")

    department_counts = (
        df["department"]
        .value_counts()
    )

    st.bar_chart(
        department_counts
    )

    st.divider()

    # -----------------------------------------
    # FILTERS
    # -----------------------------------------

    st.subheader("🔎 Search & Filter")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        search = st.text_input(
            "Search",
            placeholder="ID, title, student..."
        )

    with col2:

        status_filter = st.selectbox(
            "Status",
            [
                "All",
                "Pending",
                "In Progress",
                "Resolved",
                "Rejected"
            ]
        )

    with col3:

        priority_filter = st.selectbox(
            "Priority",
            [
                "All",
                "Critical",
                "High",
                "Medium",
                "Low"
            ]
        )

    with col4:

        sla_filter = st.selectbox(
            "SLA",
            [
                "All",
                "Overdue Only",
                "Within SLA"
            ]
        )

    filtered_df = df.copy()

    # Search
    if search:

        search_lower = search.lower()

        filtered_df = filtered_df[
            filtered_df.apply(
                lambda row:
                search_lower in str(
                    row["complaint_id"]
                ).lower()
                or search_lower in str(
                    row["title"]
                ).lower()
                or search_lower in str(
                    row["student_name"]
                ).lower()
                or search_lower in str(
                    row["email"]
                ).lower(),
                axis=1
            )
        ]

    # Status
    if status_filter != "All":

        filtered_df = filtered_df[
            filtered_df["status"] == status_filter
        ]

    # Priority
    if priority_filter != "All":

        filtered_df = filtered_df[
            filtered_df["priority"] == priority_filter
        ]

    # SLA
    if sla_filter == "Overdue Only":

        filtered_df = filtered_df[
            filtered_df["overdue"] == True
        ]

    elif sla_filter == "Within SLA":

        filtered_df = filtered_df[
            filtered_df["overdue"] == False
        ]

    st.write(
        f"Showing **{len(filtered_df)}** complaint(s)"
    )

    st.divider()

    # -----------------------------------------
    # COMPLAINTS
    # -----------------------------------------

    st.subheader("📋 Complaint Management")

    for _, complaint in filtered_df.iterrows():

        complaint_id = complaint["complaint_id"]

        overdue_flag = complaint["overdue"]

        if overdue_flag:

            header = (
                f"🚨 SLA BREACHED | "
                f"{complaint_id} | "
                f"{complaint['title']}"
            )

        elif complaint["priority"] == "Critical":

            header = (
                f"🔴 CRITICAL | "
                f"{complaint_id} | "
                f"{complaint['title']}"
            )

        elif complaint["priority"] == "High":

            header = (
                f"🟠 HIGH | "
                f"{complaint_id} | "
                f"{complaint['title']}"
            )

        else:

            header = (
                f"🎫 {complaint_id} | "
                f"{complaint['title']}"
            )

        with st.expander(header):

            # ---------------------------------
            # INFORMATION
            # ---------------------------------

            col1, col2, col3 = st.columns(3)

            with col1:

                st.write(
                    f"**Student:** {complaint['student_name']}"
                )

                st.write(
                    f"**Email:** {complaint['email']}"
                )

            with col2:

                st.write(
                    f"**Category:** {complaint['category']}"
                )

                st.write(
                    f"**Priority:** {complaint['priority']}"
                )

            with col3:

                st.write(
                    f"**Department:** {complaint['department']}"
                )

                st.write(
                    f"**Status:** {complaint['status']}"
                )

            # ---------------------------------
            # SLA INFORMATION
            # ---------------------------------

            deadline = get_sla_deadline(
                complaint["created_at"],
                complaint["priority"]
            )

            st.write(
                f"**Submitted:** {complaint['created_at']}"
            )

            if deadline:

                st.write(
                    f"**SLA Deadline:** "
                    f"{deadline.strftime('%Y-%m-%d %H:%M:%S')}"
                )

            if overdue_flag:

                st.error(
                    "🚨 SLA BREACHED — "
                    "This complaint requires immediate attention."
                )

            elif complaint["status"] not in [
                "Resolved",
                "Rejected"
            ]:

                st.info(
                    "⏱️ Complaint is currently within its SLA."
                )

            # ---------------------------------
            # DESCRIPTION
            # ---------------------------------

            st.write("### 📝 Description")

            st.write(
                complaint["description"]
            )

            # ---------------------------------
            # IMAGE
            # ---------------------------------

            if complaint["image_path"]:

                try:

                    st.image(
                        complaint["image_path"],
                        caption="Complaint Image",
                        width=400
                    )

                except Exception:

                    st.warning(
                        "⚠️ Complaint image could not be displayed."
                    )

            st.divider()

            # ---------------------------------
            # STATUS UPDATE
            # ---------------------------------

            status_options = [
                "Pending",
                "In Progress",
                "Resolved",
                "Rejected"
            ]

            current_status = complaint["status"]

            selected_status = st.selectbox(
                "Update Status",
                status_options,
                index=status_options.index(
                    current_status
                ),
                key=f"status_{complaint_id}"
            )

            if st.button(
                "💾 Update Status",
                key=f"update_{complaint_id}",
                use_container_width=True
            ):

                update_complaint_status(
                    complaint_id,
                    selected_status
                )

                st.success(
                    f"✅ {complaint_id} updated to "
                    f"**{selected_status}**"
                )

                st.rerun()