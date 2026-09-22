import streamlit as st
import Database
import pandas as pd


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Campus Maintenance Management System",
    page_icon="🏫",
    layout="wide"
)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

Database.create_tables()


# =========================================================
# TITLE
# =========================================================

st.title("🏫 Campus Maintenance Management System")

st.caption(
    "Complaint management, maintenance tracking and reporting"
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Complaints",
        "Add Complaint",
        "Update Complaint",
        "Maintenance Details"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.header("📊 Dashboard")

    complaints = Database.get_all_complaints()

    if complaints:

        columns = [
            "Complaint ID",
            "Student",
            "Department",
            "Building",
            "Room",
            "Category",
            "Priority",
            "Description",
            "Status",
            "Technician",
            "Maintenance Details",
            "Repair Cost",
            "Complaint Date",
            "Updated Date"
        ]

        df = pd.DataFrame(
            complaints,
            columns=columns
        )

        # -------------------------------------------------
        # SUMMARY METRICS
        # -------------------------------------------------

        total = len(df)

        pending = len(
            df[df["Status"] == "Pending"]
        )

        in_progress = len(
            df[df["Status"] == "In Progress"]
        )

        resolved = len(
            df[df["Status"] == "Resolved"]
        )

        total_cost = pd.to_numeric(
            df["Repair Cost"],
            errors="coerce"
        ).fillna(0).sum()

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "Total Complaints",
            total
        )

        col2.metric(
            "Pending",
            pending
        )

        col3.metric(
            "In Progress",
            in_progress
        )

        col4.metric(
            "Resolved",
            resolved
        )

        col5.metric(
            "Total Repair Cost",
            f"₹{total_cost:,.2f}"
        )

        st.divider()

        # -------------------------------------------------
        # STATUS & CATEGORY ANALYTICS
        # -------------------------------------------------

        st.subheader("Complaint Analytics")

        col1, col2 = st.columns(2)

        with col1:

            st.write("### Complaints by Status")

            status_data = (
                df["Status"]
                .value_counts()
                .rename_axis("Status")
                .reset_index(name="Complaints")
            )

            st.bar_chart(
                status_data.set_index("Status")
            )

        with col2:

            st.write()

# =========================================================
# COMPLAINTS
# =========================================================

elif page == "Complaints":

    st.header("Complaints")

    complaints = Database.get_all_complaints()

    if complaints:

        columns = [
            "Complaint ID",
            "Student",
            "Department",
            "Building",
            "Room",
            "Category",
            "Priority",
            "Description",
            "Status",
            "Technician",
            "Maintenance Details",
            "Repair Cost",
            "Complaint Date",
            "Updated Date"
        ]

        df = pd.DataFrame(
            complaints,
            columns=columns
        )

        # -------------------------------------------------
        # SEARCH
        # -------------------------------------------------

        st.subheader("Search & Filters")

        search_text = st.text_input(
            "🔎 Search complaints",
            placeholder="Search by ID, student, department, building, category..."
        )

        # -------------------------------------------------
        # FILTERS
        # -------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            status_filter = st.selectbox(
                "Status",
                ["All", "Pending", "In Progress", "Resolved"]
            )

        with col2:

            priority_filter = st.selectbox(
                "Priority",
                ["All", "Low", "Medium", "High", "Critical"]
            )

        with col3:

            category_options = ["All"] + sorted(
                df["Category"].dropna().unique().tolist()
            )

            category_filter = st.selectbox(
                "Category",
                category_options
            )

        with col4:

            building_options = ["All"] + sorted(
                df["Building"].dropna().unique().tolist()
            )

            building_filter = st.selectbox(
                "Building",
                building_options
            )

        # -------------------------------------------------
        # APPLY SEARCH
        # -------------------------------------------------

        filtered_df = df.copy()

        if search_text:

            search_text = search_text.lower()

            filtered_df = filtered_df[
                filtered_df.astype(str)
                .apply(
                    lambda row:
                    row.str.lower()
                    .str.contains(
                        search_text,
                        na=False
                    ).any(),
                    axis=1
                )
            ]

        # -------------------------------------------------
        # APPLY STATUS FILTER
        # -------------------------------------------------

        if status_filter != "All":

            filtered_df = filtered_df[
                filtered_df["Status"] == status_filter
            ]

        # -------------------------------------------------
        # APPLY PRIORITY FILTER
        # -------------------------------------------------

        if priority_filter != "All":

            filtered_df = filtered_df[
                filtered_df["Priority"] == priority_filter
            ]

        # -------------------------------------------------
        # APPLY CATEGORY FILTER
        # -------------------------------------------------

        if category_filter != "All":

            filtered_df = filtered_df[
                filtered_df["Category"] == category_filter
            ]

        # -------------------------------------------------
        # APPLY BUILDING FILTER
        # -------------------------------------------------

        if building_filter != "All":

            filtered_df = filtered_df[
                filtered_df["Building"] == building_filter
            ]

        # -------------------------------------------------
        # RESULTS
        # -------------------------------------------------

        st.divider()

        st.write(
            f"Showing **{len(filtered_df)}** of "
            f"**{len(df)}** complaints"
        )

        if not filtered_df.empty:

            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No complaints match the selected filters."
            )

    else:

        st.info("No complaints found.")

# =========================================================
# ADD COMPLAINT
# =========================================================

elif page == "Add Complaint":

    st.header("Add New Complaint")

    with st.form("complaint_form"):

        student_name = st.text_input("Student Name")

        department = st.text_input("Department")

        building = st.text_input("Building")

        room_no = st.text_input("Room Number")

        category = st.selectbox(
            "Category",
            [
                "Electrical",
                "Plumbing",
                "Furniture",
                "Cleaning",
                "Internet",
                "Other"
            ]
        )

        priority = st.selectbox(
            "Priority",
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ]
        )

        description = st.text_area(
            "Complaint Description"
        )

        submitted = st.form_submit_button(
            "Submit Complaint"
        )

        if submitted:

            if not student_name or not department or not building or not room_no or not description:

                st.warning(
                    "Please fill in all required fields."
                )

            else:

                ticket_id = Database.add_complaint(
                    student_name,
                    department,
                    building,
                    room_no,
                    category,
                    priority,
                    description
                )

                st.success(
                    f"Complaint submitted successfully. "
                    f"Complaint ID: {ticket_id}"
                )


# =========================================================
# UPDATE COMPLAINT
# =========================================================

elif page == "Update Complaint":

    st.header("Update Complaint")

    ticket_id = st.number_input(
        "Complaint ID",
        min_value=1,
        step=1
    )

    if st.button("Fetch Complaint"):

        complaint = Database.fetch_complaint(
            ticket_id
        )

        if complaint:

            st.session_state["complaint"] = complaint

        else:

            st.error(
                f"No complaint found with ID {ticket_id}."
            )


    if "complaint" in st.session_state:

        complaint = st.session_state["complaint"]

        st.write(
            f"**Student:** {complaint[1]}"
        )

        st.write(
            f"**Department:** {complaint[2]}"
        )

        st.write(
            f"**Category:** {complaint[5]}"
        )

        st.write(
            f"**Current Status:** {complaint[8]}"
        )

        st.divider()

        technician = st.text_input(
            "Technician Name",
            value=complaint[9] or ""
        )

        new_status = st.selectbox(
            "New Status",
            [
                "Pending",
                "In Progress",
                "Resolved"
            ],
            index=[
                "Pending",
                "In Progress",
                "Resolved"
            ].index(complaint[8])
            if complaint[8] in [
                "Pending",
                "In Progress",
                "Resolved"
            ]
            else 0
        )

        maintenance_details = st.text_area(
            "Maintenance / Resolution Details",
            value=complaint[10] or ""
        )

        if st.button("Update Complaint"):

            Database.update_status(
                ticket_id,
                new_status
            )

            Database.update_complaint(
                ticket_id,
                technician,
                maintenance_details,
                complaint[11] or 0
            )

            st.success(
                f"Complaint #{ticket_id} updated successfully."
            )

            st.session_state.pop(
                "complaint",
                None
            )


# =========================================================
# MAINTENANCE DETAILS
# =========================================================

elif page == "Maintenance Details":

    st.header("Maintenance Details")

    ticket_id = st.number_input(
        "Complaint ID",
        min_value=1,
        step=1
    )

    if st.button("Fetch Details"):

        complaint = Database.fetch_complaint(ticket_id)

        if complaint:

            st.session_state["maintenance_complaint"] = complaint

        else:

            st.error(
                f"No complaint found with ID {ticket_id}."
            )


    # -----------------------------------------------------
    # DISPLAY / EDIT MAINTENANCE INFORMATION
    # -----------------------------------------------------

    if "maintenance_complaint" in st.session_state:

        complaint = st.session_state["maintenance_complaint"]

        st.divider()

        st.subheader("Complaint Information")

        st.write(
            f"**Student:** {complaint[1]}"
        )

        st.write(
            f"**Department:** {complaint[2]}"
        )

        st.write(
            f"**Category:** {complaint[5]}"
        )

        st.write(
            f"**Status:** {complaint[8]}"
        )

        st.divider()

        st.subheader("Update Maintenance Information")

        technician = st.text_input(
            "Technician Name",
            value=complaint[9] or ""
        )

        maintenance_details = st.text_area(
            "Maintenance Details",
            value=complaint[10] or ""
        )

        repair_cost = st.number_input(
            "Repair Cost (₹)",
            min_value=0.0,
            value=float(complaint[11] or 0),
            step=100.0
        )

        if st.button("Update Maintenance Details"):

            result = Database.update_complaint(
                ticket_id,
                technician,
                maintenance_details,
                repair_cost
            )

            if result > 0:

                # Fetch updated data
                updated_complaint = Database.fetch_complaint(
                    ticket_id
                )

                st.session_state["maintenance_complaint"] = updated_complaint

                st.success(
                    f"Maintenance details for Complaint #{ticket_id} "
                    f"updated successfully."
                )

            else:

                st.error(
                    "Unable to update the complaint."
                )