import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

import Database
import Analysis

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ---------------------------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------------------------

Database.create_tables()


# ---------------------------------------------------------
# MAIN WINDOW
# ---------------------------------------------------------

root = tk.Tk()

root.title("CampusFix - Maintenance Control System")
root.geometry("1100x700")
root.minsize(900, 600)

root.configure(bg="#0B1F33")


# ---------------------------------------------------------
# COLORS
# ---------------------------------------------------------

BG_COLOR = "#0B1F33"
BUTTON_COLOR = "#4FC3E1"
CARD_COLOR = "#12304A"
PRIMARY_COLOR = "#55C7E8"
ACCENT_COLOR = "#F5A623"
TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT = "#A8C7D9"


# ---------------------------------------------------------
# STYLES
# ---------------------------------------------------------

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "TButton",
    font=("Segoe UI", 11, "bold"),
    padding=10
)

style.configure(
    "Title.TLabel",
    background=BG_COLOR,
    foreground=TEXT_COLOR,
    font=("Segoe UI", 28, "bold")
)

style.configure(
    "Subtitle.TLabel",
    background=BG_COLOR,
    foreground=SECONDARY_TEXT,
    font=("Segoe UI", 12)
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

header = tk.Frame(
    root,
    bg=BG_COLOR,
    height=100
)

header.pack(fill="x", padx=30, pady=(20, 10))

title = ttk.Label(
    header,
    text="CampusFix",
    style="Title.TLabel"
)

title.pack(anchor="w")

subtitle = ttk.Label(
    header,
    text="Maintenance Control System",
    style="Subtitle.TLabel"
)

subtitle.pack(anchor="w")


# ---------------------------------------------------------
# DASHBOARD FRAME
# ---------------------------------------------------------

dashboard_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

dashboard_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=20
)


# ---------------------------------------------------------
# GET STATISTICS
# ---------------------------------------------------------

def coming_soon():
    messagebox.showinfo(
        "Coming Soon",
        "This module will be implemented in the next development phase."
    )
    
def get_statistics():

    complaints = Database.get_all_complaints()

    total = len(complaints)

    pending = 0
    in_progress = 0
    resolved = 0

    for complaint in complaints:

        status = complaint[8]

        if status == "Pending":
            pending += 1

        elif status == "In Progress":
            in_progress += 1

        elif status == "Resolved":
            resolved += 1

    return total, pending, in_progress, resolved


# ---------------------------------------------------------
# CREATE STAT CARD
# ---------------------------------------------------------

def create_stat_card(parent, title, value, column):

    card = tk.Frame(
        parent,
        bg=CARD_COLOR,
        width=230,
        height=130,
        highlightbackground="#23516D",
        highlightthickness=1
    )

    card.grid(
        row=0,
        column=column,
        padx=10,
        pady=10,
        sticky="nsew"
    )

    card.grid_propagate(False)

    value_label = tk.Label(
        card,
        text=str(value),
        bg=CARD_COLOR,
        fg=PRIMARY_COLOR,
        font=("Segoe UI", 28, "bold")
    )

    value_label.pack(
        pady=(20, 5)
    )

    title_label = tk.Label(
        card,
        text=title,
        bg=CARD_COLOR,
        fg=SECONDARY_TEXT,
        font=("Segoe UI", 11)
    )

    title_label.pack()

    return value_label


# ---------------------------------------------------------
# STATISTICS
# ---------------------------------------------------------

total, pending, in_progress, resolved = get_statistics()

stats_frame = tk.Frame(
    dashboard_frame,
    bg=BG_COLOR
)

stats_frame.pack(
    fill="x",
    pady=20
)

for i in range(4):
    stats_frame.columnconfigure(i, weight=1)


total_label = create_stat_card(
    stats_frame,
    "TOTAL COMPLAINTS",
    total,
    0
)

pending_label = create_stat_card(
    stats_frame,
    "PENDING",
    pending,
    1
)

progress_label = create_stat_card(
    stats_frame,
    "IN PROGRESS",
    in_progress,
    2
)

resolved_label = create_stat_card(
    stats_frame,
    "RESOLVED",
    resolved,
    3
)


# ---------------------------------------------------------
# BUTTON FUNCTIONS
# ---------------------------------------------------------

def refresh_dashboard():
    """Refresh dashboard statistics."""

    total, pending, in_progress, resolved = get_statistics()

    total_label.config(text=str(total))
    pending_label.config(text=str(pending))
    progress_label.config(text=str(in_progress))
    resolved_label.config(text=str(resolved))


def register_complaint_window():
    """Open the complaint registration form."""

    window = tk.Toplevel(root)

    window.title("Register Complaint")
    window.geometry("850x650")
    window.configure(bg=BG_COLOR)

    window.transient(root)

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    tk.Label(
        window,
        text="REGISTER A COMPLAINT",
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        font=("Segoe UI", 24, "bold")
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        window,
        text="Enter the complaint details below",
        bg=BG_COLOR,
        fg=SECONDARY_TEXT,
        font=("Segoe UI", 11)
    ).pack(
        pady=(0, 20)
    )

    # -----------------------------------------------------
    # FORM
    # -----------------------------------------------------

    form = tk.Frame(
        window,
        bg="#F4F0E6",
        padx=30,
        pady=25
    )

    form.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 25)
    )

    # -----------------------------------------------------
    # VARIABLES
    # -----------------------------------------------------

    student_name_var = tk.StringVar()
    department_var = tk.StringVar()
    building_var = tk.StringVar()
    room_var = tk.StringVar()
    category_var = tk.StringVar()
    priority_var = tk.StringVar()

    # -----------------------------------------------------
    # LABEL STYLE
    # -----------------------------------------------------

    label_font = (
        "Segoe UI",
        10,
        "bold"
    )

    # -----------------------------------------------------
    # STUDENT NAME
    # -----------------------------------------------------

    tk.Label(
        form,
        text="Student Name",
        bg="#F4F0E6",
        fg="#555555",
        font=label_font
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=10,
        pady=(5, 5)
    )

    student_entry = ttk.Entry(
        form,
        textvariable=student_name_var,
        width=35
    )

    student_entry.grid(
        row=1,
        column=0,
        padx=10,
        pady=(0, 15),
        sticky="ew"
    )

    # -----------------------------------------------------
    # DEPARTMENT
    # -----------------------------------------------------

    tk.Label(
        form,
        text="Department",
        bg="#F4F0E6",
        fg="#555555",
        font=label_font
    ).grid(
        row=0,
        column=1,
        sticky="w",
        padx=10,
        pady=(5, 5)
    )

    department_box = ttk.Combobox(
        form,
        textvariable=department_var,
        values=[
            "Computer Science",
            "Artificial Intelligence",
            "Information Technology",
            "Electronics",
            "Mechanical",
            "Civil",
            "Electrical",
            "Other"
        ],
        state="readonly",
        width=32
    )

    department_box.grid(
        row=1,
        column=1,
        padx=10,
        pady=(0, 15),
        sticky="ew"
    )

    # -----------------------------------------------------
    # BUILDING
    # -----------------------------------------------------

    tk.Label(
        form,
        text="Building",
        bg="#F4F0E6",
        fg="#555555",
        font=label_font
    ).grid(
        row=2,
        column=0,
        sticky="w",
        padx=10,
        pady=(5, 5)
    )

    building_box = ttk.Combobox(
        form,
        textvariable=building_var,
        values=[
            "Block A",
            "Block B",
            "Block C",
            "Computer Lab",
            "Library",
            "Hostel Block"
        ],
        state="readonly",
        width=32
    )

    building_box.grid(
        row=3,
        column=0,
        padx=10,
        pady=(0, 15),
        sticky="ew"
    )

    # -----------------------------------------------------
    # ROOM NUMBER
    # -----------------------------------------------------

    tk.Label(
        form,
        text="Room Number",
        bg="#F4F0E6",
        fg="#555555",
        font=label_font
    ).grid(
        row=2,
        column=1,
        sticky="w",
        padx=10,
        pady=(5, 5)
    )

    room_entry = ttk.Entry(
        form,
        textvariable=room_var,
        width=35
    )

    room_entry.grid(
        row=3,
        column=1,
        padx=10,
        pady=(0, 15),
        sticky="ew"
    )

    # -----------------------------------------------------
    # CATEGORY
    # -----------------------------------------------------

    tk.Label(
        form,
        text="Category",
        bg="#F4F0E6",
        fg="#555555",
        font=label_font
    ).grid(
        row=4,
        column=0,
        sticky="w",
        padx=10,
        pady=(5, 5)
    )

    category_box = ttk.Combobox(
        form,
        textvariable=category_var,
        values=[
            "Electrical",
            "Furniture",
            "Plumbing",
            "IT",
            "Internet",
            "Cleaning",
            "AC/Cooling",
            "Other"
        ],
        state="readonly",
        width=32
    )

    category_box.grid(
        row=5,
        column=0,
        padx=10,
        pady=(0, 15),
        sticky="ew"
    )

    # -----------------------------------------------------
    # PRIORITY
    # -----------------------------------------------------

    tk.Label(
        form,
        text="Priority",
        bg="#F4F0E6",
        fg="#555555",
        font=label_font
    ).grid(
        row=4,
        column=1,
        sticky="w",
        padx=10,
        pady=(5, 5)
    )

    priority_box = ttk.Combobox(
        form,
        textvariable=priority_var,
        values=[
            "Low",
            "Medium",
            "High",
            "Critical"
        ],
        state="readonly",
        width=32
    )

    priority_box.grid(
        row=5,
        column=1,
        padx=10,
        pady=(0, 15),
        sticky="ew"
    )

    # -----------------------------------------------------
    # DESCRIPTION
    # -----------------------------------------------------

    tk.Label(
        form,
        text="Problem Description",
        bg="#F4F0E6",
        fg="#555555",
        font=label_font
    ).grid(
        row=6,
        column=0,
        columnspan=2,
        sticky="w",
        padx=10,
        pady=(5, 5)
    )

    description_text = tk.Text(
        form,
        height=6,
        font=("Segoe UI", 10),
        relief="solid",
        borderwidth=1
    )

    description_text.grid(
        row=7,
        column=0,
        columnspan=2,
        padx=10,
        pady=(0, 20),
        sticky="ew"
    )

    # -----------------------------------------------------
    # FORM COLUMNS
    # -----------------------------------------------------

    form.columnconfigure(0, weight=1)
    form.columnconfigure(1, weight=1)

    # -----------------------------------------------------
    # SUBMIT FUNCTION
    # -----------------------------------------------------

    def submit_complaint():

        student_name = student_name_var.get().strip()
        department = department_var.get()
        building = building_var.get()
        room_no = room_var.get().strip()
        category = category_var.get()
        priority = priority_var.get()
        description = description_text.get(
            "1.0",
            tk.END
        ).strip()

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not student_name:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the student name.",
                parent=window
            )
            return

        if not department:
            messagebox.showwarning(
                "Missing Information",
                "Please select a department.",
                parent=window
            )
            return

        if not building:
            messagebox.showwarning(
                "Missing Information",
                "Please select a building.",
                parent=window
            )
            return

        if not room_no:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the room number.",
                parent=window
            )
            return

        if not category:
            messagebox.showwarning(
                "Missing Information",
                "Please select a category.",
                parent=window
            )
            return

        if not priority:
            messagebox.showwarning(
                "Missing Information",
                "Please select a priority.",
                parent=window
            )
            return

        if not description:
            messagebox.showwarning(
                "Missing Information",
                "Please describe the problem.",
                parent=window
            )
            return

        # -------------------------------------------------
        # SAVE COMPLAINT
        # -------------------------------------------------

        ticket_id = Database.add_complaint(
            student_name,
            department,
            building,
            room_no,
            category,
            priority,
            description
        )

        # -------------------------------------------------
        # SUCCESS MESSAGE
        # -------------------------------------------------

        messagebox.showinfo(
            "Complaint Registered",
            f"Complaint registered successfully!\n\n"
            f"Your Ticket ID is: #{ticket_id}",
            parent=window
        )

        # Refresh dashboard
        refresh_dashboard()

        # Close registration window
        window.destroy()

    # -----------------------------------------------------
    # BUTTON
    # -----------------------------------------------------

    submit_button = tk.Button(
        form,
        text="Register Complaint",
        command=submit_complaint,
        bg="#0B1F33",
        fg="white",
        activebackground="#173C58",
        activeforeground="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        padx=25,
        pady=10,
        cursor="hand2"
    )

    submit_button.grid(
        row=8,
        column=0,
        padx=10,
        pady=10,
        sticky="w"
    )

    student_entry.focus_set()

def view_complaints_window():
    window = tk.Toplevel(root)
    window.title("View Complaints")
    window.geometry("1400x650")
    window.configure(bg=BG_COLOR)

    # -----------------------------
    # Title
    # -----------------------------
    title = tk.Label(
        window,
        text="ALL COMPLAINTS",
        font=("Arial", 26, "bold"),
        fg="white",
        bg=BG_COLOR
    )
    title.pack(pady=(20, 10))

    # -----------------------------
    # Main frame
    # -----------------------------
    table_frame = tk.Frame(
        window,
        bg=BG_COLOR
    )
    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    # -----------------------------
    # Columns
    # -----------------------------
    columns = (
        "ID",
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
        "Created At",
        "Updated At"
    )

    # -----------------------------
    # Scrollbars
    # -----------------------------
    vertical_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical"
    )

    horizontal_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="horizontal"
    )

    # -----------------------------
    # Treeview
    # -----------------------------
    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set
    )

    vertical_scrollbar.config(
        command=tree.yview
    )

    horizontal_scrollbar.config(
        command=tree.xview
    )

    # -----------------------------
    # Column headings
    # -----------------------------
    for column in columns:
        tree.heading(
            column,
            text=column
        )

    # -----------------------------
    # Column widths
    # -----------------------------
    tree.column("ID", width=60, anchor="center")
    tree.column("Student", width=150)
    tree.column("Department", width=150)
    tree.column("Building", width=120)
    tree.column("Room", width=80, anchor="center")
    tree.column("Category", width=120)
    tree.column("Priority", width=100, anchor="center")
    tree.column("Description", width=250)
    tree.column("Status", width=120, anchor="center")
    tree.column("Technician", width=150)
    tree.column("Maintenance Details", width=250)
    tree.column("Repair Cost", width=110, anchor="center")
    tree.column("Created At", width=160)
    tree.column("Updated At", width=160)

    # -----------------------------
    # Get complaints from database
    # -----------------------------
    complaints = Database.get_all_complaints()

    # -----------------------------
    # Insert complaints
    # -----------------------------
    for complaint in complaints:
        tree.insert(
            "",
            "end",
            values=complaint
        )

    # -----------------------------
    # Pack table + scrollbars
    # -----------------------------
    tree.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    vertical_scrollbar.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    horizontal_scrollbar.grid(
        row=1,
        column=0,
        sticky="ew"
    )

    table_frame.grid_rowconfigure(
        0,
        weight=1
    )

    table_frame.grid_columnconfigure(
        0,
        weight=1
    )

def search_complaint_window():
    search_window = tk.Toplevel(root)
    search_window.title("Search Complaint")
    search_window.geometry("1250x700")
    search_window.configure(bg=BG_COLOR)

    # =========================
    # TITLE
    # =========================

    title_label = tk.Label(
        search_window,
        text="SEARCH COMPLAINT",
        font=("Segoe UI", 28, "bold"),
        fg="white",
        bg=BG_COLOR
    )
    title_label.pack(pady=25)

    # =========================
    # SEARCH FRAME
    # =========================

    search_frame = tk.Frame(
        search_window,
        bg=BG_COLOR
    )
    search_frame.pack(pady=10)

    tk.Label(
        search_frame,
        text="Search By:",
        font=("Segoe UI", 13, "bold"),
        fg="white",
        bg=BG_COLOR
    ).grid(row=0, column=0, padx=10, pady=10)

    search_type = ttk.Combobox(
        search_frame,
        values=[
            "Complaint ID",
            "Student Name",
            "Department",
            "Category",
            "Status"
        ],
        state="readonly",
        width=18,
        font=("Segoe UI", 11)
    )

    search_type.current(0)
    search_type.grid(row=0, column=1, padx=10)

    search_entry = tk.Entry(
        search_frame,
        width=35,
        font=("Segoe UI", 12)
    )
    search_entry.grid(row=0, column=2, padx=10)

    # =========================
    # TABLE
    # =========================

    table_frame = tk.Frame(
        search_window,
        bg=BG_COLOR
    )
    table_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=20
    )

    columns = (
        "ID",
        "Student",
        "Department",
        "Building",
        "Room",
        "Category",
        "Priority",
        "Description",
        "Status",
        "Technician",
        "Resolution",
        "Cost",
        "Created",
        "Updated"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=120)

    tree.column("ID", width=60)
    tree.column("Student", width=130)
    tree.column("Department", width=130)
    tree.column("Building", width=100)
    tree.column("Room", width=80)
    tree.column("Category", width=100)
    tree.column("Priority", width=80)
    tree.column("Description", width=250)
    tree.column("Status", width=110)
    tree.column("Technician", width=130)
    tree.column("Resolution", width=200)
    tree.column("Cost", width=80)
    tree.column("Created", width=150)
    tree.column("Updated", width=150)

    scrollbar_y = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    scrollbar_x = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=tree.xview
    )

    tree.configure(
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )

    tree.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    scrollbar_y.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    scrollbar_x.grid(
        row=1,
        column=0,
        sticky="ew"
    )

    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    # =========================
    # SEARCH FUNCTION
    # =========================

    def perform_search():
        search_value = search_entry.get().strip()

        if not search_value:
            messagebox.showwarning(
                "Search",
                "Please enter a value to search."
            )
            return

        selected_type = search_type.get()

        column_map = {
            "Complaint ID": "ticket_id",
            "Student Name": "student_name",
            "Department": "department",
            "Category": "category",
            "Status": "status"
        }

        selected_column = column_map[selected_type]

        try:
            conn = Database.connect_db()
            cursor = conn.cursor()

            # Clear previous results
            for item in tree.get_children():
                tree.delete(item)

            if selected_column == "ticket_id":
                try:
                    search_id = int(search_value)

                    cursor.execute(
                        """
                        SELECT
                            ticket_id,
                            student_name,
                            department,
                            building,
                            room_no,
                            category,
                            priority,
                            description,
                            status,
                            technician_name,
                            maintenance_details,
                            repair_cost,
                            complaint_date,
                            updated_date
                        FROM complaints
                        WHERE ticket_id = ?
                        """,
                        (search_id,)
                    )

                except ValueError:
                    messagebox.showerror(
                        "Search",
                        "Complaint ID must be a number."
                    )
                    conn.close()
                    return

            else:
                cursor.execute(
                    f"""
                    SELECT
                        ticket_id,
                        student_name,
                        department,
                        building,
                        room_no,
                        category,
                        priority,
                        description,
                        status,
                        technician_name,
                        maintenance_details,
                        repair_cost,
                        complaint_date,
                        updated_date
                    FROM complaints
                    WHERE {selected_column} LIKE ?
                    ORDER BY ticket_id DESC
                    """,
                    (f"%{search_value}%",)
                )

            results = cursor.fetchall()
            conn.close()

            if not results:
                messagebox.showinfo(
                    "Search",
                    "No complaints were found."
                )
                return

            for row in results:
                tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"An error occurred while searching:\n{e}"
            )
        


    # =========================
    # BUTTONS
    # =========================

    button_frame = tk.Frame(
        search_window,
        bg=BG_COLOR
    )
    button_frame.pack(pady=15)

    search_button = tk.Button(
        button_frame,
        text="SEARCH",
        command=perform_search,
        font=("Segoe UI", 12, "bold"),
        bg=BUTTON_COLOR,
        fg="black",
        width=15,
        height=2,
        relief="flat",
        cursor="hand2"
    )

    search_button.grid(
        row=0,
        column=0,
        padx=10
    )

    clear_button = tk.Button(
        button_frame,
        text="CLEAR",
        command=lambda: [
            search_entry.delete(0, tk.END),
            [tree.delete(item) for item in tree.get_children()]
        ],
        font=("Segoe UI", 12, "bold"),
        bg="white",
        fg="black",
        width=15,
        height=2,
        relief="flat",
        cursor="hand2"
    )

    clear_button.grid(
        row=0,
        column=1,
        padx=10
    )

def update_status_window():

    window = tk.Toplevel()
    window.title("Update Complaint Status")
    window.geometry("650x650")
    window.configure(bg=BG_COLOR)

    # -----------------------------
    # TITLE
    # -----------------------------

    tk.Label(
        window,
        text="Update Complaint Status",
        font=("Segoe UI", 20, "bold"),
        fg="white",
        bg=BG_COLOR
    ).pack(pady=(25, 10))

    tk.Label(
        window,
        text="Enter a Complaint ID to fetch the complaint",
        font=("Segoe UI", 11),
        fg="#B8C7D9",
        bg=BG_COLOR
    ).pack(pady=(0, 20))

    # -----------------------------
    # COMPLAINT ID
    # -----------------------------

    id_frame = tk.Frame(
        window,
        bg=BG_COLOR
    )
    id_frame.pack(pady=10)

    tk.Label(
        id_frame,
        text="Complaint ID:",
        font=("Segoe UI", 11, "bold"),
        fg="white",
        bg=BG_COLOR
    ).grid(row=0, column=0, padx=10)

    complaint_id_entry = tk.Entry(
        id_frame,
        font=("Segoe UI", 11),
        width=20
    )
    complaint_id_entry.grid(row=0, column=1, padx=10)

    # -----------------------------
    # DETAILS FRAME
    # -----------------------------

    details_frame = tk.Frame(
        window,
        bg=BG_COLOR
    )
    details_frame.pack(pady=20, padx=30, fill="x")

    # Variables

    student_var = tk.StringVar()
    department_var = tk.StringVar()
    category_var = tk.StringVar()
    current_status_var = tk.StringVar()

    # Student

    tk.Label(
        details_frame,
        text="Student:",
        font=("Segoe UI", 10, "bold"),
        fg="white",
        bg=BG_COLOR
    ).grid(row=0, column=0, sticky="w", pady=6)

    tk.Label(
        details_frame,
        textvariable=student_var,
        font=("Segoe UI", 10),
        fg="#B8C7D9",
        bg=BG_COLOR
    ).grid(row=0, column=1, sticky="w", pady=6)

    # Department

    tk.Label(
        details_frame,
        text="Department:",
        font=("Segoe UI", 10, "bold"),
        fg="white",
        bg=BG_COLOR
    ).grid(row=1, column=0, sticky="w", pady=6)

    tk.Label(
        details_frame,
        textvariable=department_var,
        font=("Segoe UI", 10),
        fg="#B8C7D9",
        bg=BG_COLOR
    ).grid(row=1, column=1, sticky="w", pady=6)

    # Category

    tk.Label(
        details_frame,
        text="Category:",
        font=("Segoe UI", 10, "bold"),
        fg="white",
        bg=BG_COLOR
    ).grid(row=2, column=0, sticky="w", pady=6)

    tk.Label(
        details_frame,
        textvariable=category_var,
        font=("Segoe UI", 10),
        fg="#B8C7D9",
        bg=BG_COLOR
    ).grid(row=2, column=1, sticky="w", pady=6)

    # Current Status

    tk.Label(
        details_frame,
        text="Current Status:",
        font=("Segoe UI", 10, "bold"),
        fg="white",
        bg=BG_COLOR
    ).grid(row=3, column=0, sticky="w", pady=6)

    tk.Label(
        details_frame,
        textvariable=current_status_var,
        font=("Segoe UI", 10, "bold"),
        fg="#39AFCF",
        bg=BG_COLOR
    ).grid(row=3, column=1, sticky="w", pady=6)

    # -----------------------------
    # TECHNICIAN
    # -----------------------------

    tk.Label(
        window,
        text="Technician Name",
        font=("Segoe UI", 11, "bold"),
        fg="white",
        bg=BG_COLOR
    ).pack(pady=(10, 5))

    technician_entry = tk.Entry(
        window,
        font=("Segoe UI", 11),
        width=40
    )
    technician_entry.pack(pady=5)

    # -----------------------------
    # NEW STATUS
    # -----------------------------

    tk.Label(
        window,
        text="New Status",
        font=("Segoe UI", 11, "bold"),
        fg="white",
        bg=BG_COLOR
    ).pack(pady=(15, 5))

    status_combo = ttk.Combobox(
        window,
        values=[
            "Pending",
            "In Progress",
            "Resolved"
        ],
        state="readonly",
        font=("Segoe UI", 11),
        width=37
    )
    status_combo.pack(pady=5)

    # -----------------------------
    # MAINTENANCE DETAILS
    # -----------------------------

    tk.Label(
        window,
        text="Maintenance / Resolution Details",
        font=("Segoe UI", 11, "bold"),
        fg="white",
        bg=BG_COLOR
    ).pack(pady=(15, 5))

    maintenance_text = tk.Text(
        window,
        height=5,
        width=45,
        font=("Segoe UI", 10)
    )
    maintenance_text.pack(pady=5)

    # -----------------------------
    # FETCH COMPLAINT
    # -----------------------------

    def fetch_complaint():

        complaint_id = complaint_id_entry.get().strip()

        if not complaint_id:
            messagebox.showwarning(
                "Input Required",
                "Please enter a Complaint ID."
            )
            return

        try:

            complaint_id = int(complaint_id)

            import sqlite3

            conn = sqlite3.connect("campus.db")
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    student_name,
                    department,
                    category,
                    status,
                    technician_name,
                    maintenance_details
                FROM complaints
                WHERE ticket_id = ?
                """,
                (complaint_id,)
            )

            complaint = cursor.fetchone()

            conn.close()

            if not complaint:
                messagebox.showerror(
                    "Complaint Not Found",
                    f"No complaint found with ID {complaint_id}."
                )
                return

            student_var.set(complaint[0])
            department_var.set(complaint[1])
            category_var.set(complaint[2])
            current_status_var.set(complaint[3])

            technician_entry.delete(0, tk.END)

            if complaint[4]:
                technician_entry.insert(0, complaint[4])

            status_combo.set(complaint[3])

            maintenance_text.delete("1.0", tk.END)

            if complaint[5]:
                maintenance_text.insert("1.0", complaint[5])

        except ValueError:

            messagebox.showerror(
                "Invalid ID",
                "Complaint ID must be a number."
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"An error occurred while fetching the complaint:\n{e}"
            )

    # -----------------------------
    # UPDATE COMPLAINT
    # -----------------------------

    def update_complaint():

        complaint_id = complaint_id_entry.get().strip()
        new_status = status_combo.get().strip()
        technician = technician_entry.get().strip()
        maintenance_details = maintenance_text.get(
            "1.0",
            tk.END
        ).strip()

        if not complaint_id:
            messagebox.showwarning(
                "Input Required",
                "Please enter a Complaint ID."
            )
            return

        if not new_status:
            messagebox.showwarning(
                "Status Required",
                "Please select a new status."
            )
            return

        try:

            complaint_id = int(complaint_id)

            import sqlite3
            from datetime import datetime

            conn = sqlite3.connect("campus.db")
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE complaints
                SET
                    status = ?,
                    technician_name = ?,
                    maintenance_details = ?,
                    updated_date = ?
                WHERE ticket_id = ?
                """,
                (
                    new_status,
                    technician,
                    maintenance_details,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    complaint_id
                )
            )

            if cursor.rowcount == 0:

                conn.close()

                messagebox.showerror(
                    "Complaint Not Found",
                    f"No complaint found with ID {complaint_id}."
                )

                return

            conn.commit()
            conn.close()

            current_status_var.set(new_status)

            messagebox.showinfo(
                "Success",
                f"Complaint #{complaint_id} has been updated successfully."
            )

        except ValueError:

            messagebox.showerror(
                "Invalid ID",
                "Complaint ID must be a number."
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"An error occurred while updating the complaint:\n{e}"
            )

    # -----------------------------
    # ACTION BUTTONS
    # -----------------------------

    button_frame = tk.Frame(
        window,
        bg=BG_COLOR
    )
    button_frame.pack(pady=25)

    # FETCH BUTTON
    fetch_button = tk.Button(
        button_frame,
        text="FETCH COMPLAINT",
        command=fetch_complaint,
        font=("Segoe UI", 12, "bold"),
        bg=BUTTON_COLOR,
        fg="black",
        width=18,
        height=2,
        relief="flat",
        cursor="hand2"
    )

    fetch_button.grid(
        row=0,
        column=0,
        padx=10
    )

    # UPDATE BUTTON
    update_button = tk.Button(
        button_frame,
        text="UPDATE COMPLAINT",
        command=update_complaint,
        font=("Segoe UI", 12, "bold"),
        bg=PRIMARY_COLOR,
        fg="#062033",
        width=18,
        height=2,
        relief="flat",
        cursor="hand2"
    )

    update_button.grid(
        row=0,
        column=1,
        padx=10
    )

def maintenance_details_window():

    window = tk.Toplevel(root)
    window.title("Maintenance Details")
    window.geometry("850x650")
    window.configure(bg=BG_COLOR)

    # -----------------------------
    # Title
    # -----------------------------

    tk.Label(
        window,
        text="Maintenance Details",
        font=("Segoe UI", 22, "bold"),
        fg="white",
        bg=BG_COLOR
    ).pack(pady=(25, 5))

    tk.Label(
        window,
        text="View and update maintenance information",
        font=("Segoe UI", 11),
        fg="#9FD9F2",
        bg=BG_COLOR
    ).pack(pady=(0, 20))


    # -----------------------------
    # Complaint ID
    # -----------------------------

    input_frame = tk.Frame(
        window,
        bg=BG_COLOR
    )
    input_frame.pack(pady=10)

    tk.Label(
        input_frame,
        text="Complaint ID:",
        font=("Segoe UI", 11, "bold"),
        fg="white",
        bg=BG_COLOR
    ).grid(row=0, column=0, padx=10)

    complaint_id_entry = tk.Entry(
        input_frame,
        font=("Segoe UI", 11),
        width=25
    )
    complaint_id_entry.grid(row=0, column=1, padx=10)


    # -----------------------------
    # Details Frame
    # -----------------------------

    details_frame = tk.Frame(
        window,
        bg=BG_COLOR
    )
    details_frame.pack(pady=20, padx=40, fill="both")


    # Student
    tk.Label(
        details_frame,
        text="Student:",
        font=("Segoe UI", 11, "bold"),
        fg="white",
        bg=BG_COLOR
    ).grid(row=0, column=0, sticky="w", pady=8)

    student_label = tk.Label(
        details_frame,
        text="-",
        font=("Segoe UI", 11),
        fg="#9FD9F2",
        bg=BG_COLOR
    )
    student_label.grid(row=0, column=1, sticky="w", pady=8)


    # Category
    tk.Label(
        details_frame,
        text="Category:",
        font=("Segoe UI", 11, "bold"),
        fg="white",
        bg=BG_COLOR
    ).grid(row=1, column=0, sticky="w", pady=8)

    category_label = tk.Label(
        details_frame,
        text="-",
        font=("Segoe UI", 11),
        fg="#9FD9F2",
        bg=BG_COLOR
    )
    category_label.grid(row=1, column=1, sticky="w", pady=8)


    # Status
    tk.Label(
        details_frame,
        text="Status:",
        font=("Segoe UI", 11, "bold"),
        fg="white",
        bg=BG_COLOR
    ).grid(row=2, column=0, sticky="w", pady=8)

    status_label = tk.Label(
        details_frame,
        text="-",
        font=("Segoe UI", 11, "bold"),
        fg="#9FD9F2",
        bg=BG_COLOR
    )
    status_label.grid(row=2, column=1, sticky="w", pady=8)


    # Technician
    tk.Label(
        details_frame,
        text="Technician:",
        font=("Segoe UI", 11, "bold"),
        fg="white",
        bg=BG_COLOR
    ).grid(row=3, column=0, sticky="w", pady=8)

    technician_entry = tk.Entry(
        details_frame,
        font=("Segoe UI", 11),
        width=40
    )
    technician_entry.grid(row=3, column=1, sticky="w", pady=8)


    # Maintenance Details
    tk.Label(
        details_frame,
        text="Maintenance Details:",
        font=("Segoe UI", 11, "bold"),
        fg="white",
        bg=BG_COLOR
    ).grid(row=4, column=0, sticky="nw", pady=8)

    maintenance_text = tk.Text(
        details_frame,
        font=("Segoe UI", 11),
        width=40,
        height=5
    )
    maintenance_text.grid(row=4, column=1, sticky="w", pady=8)


    # Repair Cost
    tk.Label(
        details_frame,
        text="Repair Cost:",
        font=("Segoe UI", 11, "bold"),
        fg="white",
        bg=BG_COLOR
    ).grid(row=5, column=0, sticky="w", pady=8)

    repair_cost_entry = tk.Entry(
        details_frame,
        font=("Segoe UI", 11),
        width=20
    )
    repair_cost_entry.grid(row=5, column=1, sticky="w", pady=8)


    # -----------------------------
    # Load Complaint
    # -----------------------------

    def load_complaint():

        complaint_id = complaint_id_entry.get().strip()

        if not complaint_id:
            messagebox.showwarning(
                "Input Required",
                "Please enter a Complaint ID."
            )
            return

        try:

            conn = Database.connect_db()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    student_name,
                    category,
                    status,
                    technician_name,
                    maintenance_details,
                    repair_cost
                FROM complaints
                WHERE ticket_id = ?
                """,
                (complaint_id,)
            )

            result = cursor.fetchone()

            conn.close()

            if not result:
                messagebox.showerror(
                    "Not Found",
                    "No complaint found with this ID."
                )
                return

            student, category, status, technician, maintenance, cost = result

            student_label.config(text=student)
            category_label.config(text=category)
            status_label.config(text=status)

            technician_entry.delete(0, tk.END)
            technician_entry.insert(
                0,
                technician or ""
            )

            maintenance_text.delete(
                "1.0",
                tk.END
            )

            maintenance_text.insert(
                "1.0",
                maintenance or ""
            )

            repair_cost_entry.delete(
                0,
                tk.END
            )

            repair_cost_entry.insert(
                0,
                str(cost or 0)
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"An error occurred while loading complaint:\n{e}"
            )

    def save_maintenance_details():

        complaint_id = complaint_id_entry.get().strip()
        technician = technician_entry.get().strip()
        maintenance = maintenance_text.get("1.0", tk.END).strip()
        repair_cost = repair_cost_entry.get().strip()

        if not complaint_id:
            messagebox.showwarning(
                "Input Required",
                "Please enter a Complaint ID."
            )
            return

        if not technician:
            messagebox.showwarning(
                "Input Required",
                "Please enter the Technician Name."
            )
            return

        if not maintenance:
            messagebox.showwarning(
                "Input Required",
                "Please enter Maintenance Details."
            )
            return

        if not repair_cost:
            repair_cost = "0"

        try:
            repair_cost = float(repair_cost)

            if repair_cost < 0:
                messagebox.showwarning(
                    "Invalid Cost",
                    "Repair cost cannot be negative."
                )
                return

        except ValueError:
            messagebox.showerror(
                "Invalid Cost",
                "Please enter a valid repair cost."
            )
            return

        try:
            updated = Database.update_complaint(
                complaint_id,
                technician,
                maintenance,
                repair_cost
            )

            if updated == 0:
                messagebox.showerror(
                    "Not Found",
                    "No complaint found with this Complaint ID."
                )
                return

            messagebox.showinfo(
                "Success",
                "Maintenance details updated successfully."
            )

            # Reload the complaint to show the latest information
            load_complaint()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Unable to update complaint.\n\n{e}"
            )

    # -----------------------------
    # Save Maintenance Details
    # -----------------------------

    def save_details():

        complaint_id = complaint_id_entry.get().strip()

        technician = technician_entry.get().strip()

        maintenance = maintenance_text.get(
            "1.0",
            tk.END
        ).strip()

        repair_cost = repair_cost_entry.get().strip()

        if not complaint_id:
            messagebox.showwarning(
                "Input Required",
                "Please enter a Complaint ID."
            )
            return

        try:

            repair_cost_value = float(
                repair_cost
            ) if repair_cost else 0

        except ValueError:

            messagebox.showwarning(
                "Invalid Cost",
                "Repair cost must be a valid number."
            )
            return

        try:

            conn = Database.connect_db()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE complaints
                SET
                    technician_name = ?,
                    maintenance_details = ?,
                    repair_cost = ?,
                    updated_date = datetime('now')
                WHERE ticket_id = ?
                """,
                (
                    technician,
                    maintenance,
                    repair_cost_value,
                    complaint_id
                )
            )

            if cursor.rowcount == 0:

                conn.close()

                messagebox.showerror(
                    "Not Found",
                    "No complaint found with this ID."
                )

                return

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Maintenance details updated successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"An error occurred while saving details:\n{e}"
            )

        # =========================
    # FETCH MAINTENANCE DETAILS
    # =========================

    def fetch_maintenance_details():

        complaint_id = complaint_id_entry.get().strip()

        if not complaint_id:
            messagebox.showwarning(
                "Input Required",
                "Please enter a Complaint ID."
            )
            return

        try:
            complaint_id = int(complaint_id)

            conn = Database.connect_db()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    student_name,
                    category,
                    status,
                    technician_name,
                    maintenance_details,
                    repair_cost
                FROM complaints
                WHERE ticket_id = ?
                """,
                (complaint_id,)
            )

            complaint = cursor.fetchone()

            conn.close()

            if not complaint:
                messagebox.showerror(
                    "Complaint Not Found",
                    f"No complaint found with ID {complaint_id}."
                )
                return

            # Display fetched information
            student_label.config(text=complaint[0] or "-")
            category_label.config(text=complaint[1] or "-")
            status_label.config(text=complaint[2] or "-")

            technician_entry.delete(0, tk.END)

            if complaint[3]:
                technician_entry.insert(0, complaint[3])

            maintenance_text.delete("1.0", tk.END)

            if complaint[4]:
                maintenance_text.insert("1.0", complaint[4])

            repair_cost_entry.delete(0, tk.END)

            if complaint[5] is not None:
                repair_cost_entry.insert(0, str(complaint[5]))

        except ValueError:

            messagebox.showerror(
                "Invalid ID",
                "Complaint ID must be a number."
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"An error occurred while fetching maintenance details:\n{e}"
            )
            
    # =============================
    # BUTTON FRAME
    # =============================

    button_frame = tk.Frame(
        window,
        bg=BG_COLOR
    )

    button_frame.pack(pady=25)

    # =============================
    # FETCH BUTTON
    # =============================

    fetch_button = tk.Button(
        button_frame,
        text="FETCH DETAILS",
        command=fetch_maintenance_details,
        font=("Segoe UI", 12, "bold"),
        bg=BUTTON_COLOR,
        fg="black",
        width=18,
        height=2,
        relief="flat",
        cursor="hand2"
    )

    fetch_button.grid(
        row=0,
        column=0,
        padx=10
    )

    # =============================
    # UPDATE BUTTON
    # =============================

    update_button = tk.Button(
        button_frame,
        text="UPDATE DETAILS",
        command=save_maintenance_details,
        font=("Segoe UI", 12, "bold"),
        bg=BUTTON_COLOR,
        fg="black",
        width=18,
        height=2,
        relief="flat",
        cursor="hand2"
    )

    update_button.grid(
        row=0,
        column=1,
        padx=10
    )

def export_analysis_csv():

    try:

        path = Analysis.export_complaints_csv()

        messagebox.showinfo(
            "Export Successful",
            f"Complaints report exported successfully.\n\nLocation:\n{path}"
        )

    except Exception as e:

        messagebox.showerror(
            "Export Error",
            f"Could not export the report.\n\n{e}"
        )


def reports_analysis_window():

    window = tk.Toplevel(root)

    window.title("Reports & Analysis")
    window.geometry("1100x750")
    window.configure(bg=BG_COLOR)

    # ==========================================================
    # HEADER
    # ==========================================================

    tk.Label(
        window,
        text="Reports & Analysis",
        font=("Segoe UI", 22, "bold"),
        fg="white",
        bg=BG_COLOR
    ).pack(pady=(20, 5))

    tk.Label(
        window,
        text="Complaint and maintenance performance overview",
        font=("Segoe UI", 11),
        fg="#9CC9E8",
        bg=BG_COLOR
    ).pack(pady=(0, 15))


    # ==========================================================
    # MAIN SCROLLABLE AREA
    # ==========================================================

    main_frame = tk.Frame(
        window,
        bg=BG_COLOR
    )

    main_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=5
    )


    canvas = tk.Canvas(
        main_frame,
        bg=BG_COLOR,
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        main_frame,
        orient="vertical",
        command=canvas.yview
    )

    scrollable_frame = tk.Frame(
        canvas,
        bg=BG_COLOR
    )

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=scrollable_frame,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )


    # ==========================================================
    # METRICS
    # ==========================================================

    try:

        metrics = Analysis.calculate_metrics()

    except Exception as e:

        messagebox.showerror(
            "Analysis Error",
            f"Unable to load analysis data.\n\n{e}"
        )

        return


    metrics_frame = tk.Frame(
        scrollable_frame,
        bg=BG_COLOR
    )

    metrics_frame.pack(
        fill="x",
        padx=10,
        pady=5
    )


    metric_data = [
        ("Total Complaints", metrics["total"]),
        ("Pending", metrics["pending"]),
        ("In Progress", metrics["in_progress"]),
        ("Resolved", metrics["resolved"]),
        (
            "Total Repair Cost",
            f"₹{metrics['total_cost']:,.2f}"
        )
    ]


    for i, (title, value) in enumerate(metric_data):

        card = tk.Frame(
            metrics_frame,
            bg=CARD_COLOR,
            width=190,
            height=100
        )

        card.grid(
            row=0,
            column=i,
            padx=7,
            pady=10
        )

        card.grid_propagate(False)


        tk.Label(
            card,
            text=str(value),
            font=("Segoe UI", 18, "bold"),
            fg=PRIMARY_COLOR,
            bg=CARD_COLOR
        ).pack(
            pady=(18, 2)
        )


        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9),
            fg="white",
            bg=CARD_COLOR
        ).pack()


    # ==========================================================
    # INSIGHTS
    # ==========================================================

    insight_text = (
        f"Most Reported Category: "
        f"{metrics['most_common_category']}    |    "
        f"Most Reported Building: "
        f"{metrics['most_reported_building']}    |    "
        f"Average Repair Cost: "
        f"₹{metrics['average_cost']:,.2f}"
    )


    tk.Label(
        scrollable_frame,
        text=insight_text,
        font=("Segoe UI", 10, "bold"),
        fg="#DCEEFF",
        bg=BG_COLOR
    ).pack(
        pady=(5, 15)
    )


    # ==========================================================
    # CHART FRAME
    # ==========================================================

    charts_frame = tk.Frame(
        scrollable_frame,
        bg=BG_COLOR
    )

    charts_frame.pack(
        fill="both",
        expand=True,
        padx=10
    )


    # ==========================================================
    # CATEGORY CHART
    # ==========================================================

    category_frame = tk.Frame(
        charts_frame,
        bg=CARD_COLOR
    )

    category_frame.grid(
        row=0,
        column=0,
        padx=8,
        pady=8,
        sticky="nsew"
    )


    category_label = tk.Label(
        category_frame,
        text="Complaints by Category",
        font=("Segoe UI", 12, "bold"),
        fg="white",
        bg=CARD_COLOR
    )

    category_label.pack(
        pady=(8, 0)
    )


    try:

        category_fig = Analysis.create_category_chart()

        category_canvas = FigureCanvasTkAgg(
            category_fig,
            master=category_frame
        )

        category_canvas.draw()

        category_canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

    except Exception as e:

        tk.Label(
            category_frame,
            text=f"Unable to load chart\n{e}",
            fg="white",
            bg=CARD_COLOR
        ).pack(
            pady=30
        )


    # ==========================================================
    # STATUS CHART
    # ==========================================================

    status_frame = tk.Frame(
        charts_frame,
        bg=CARD_COLOR
    )

    status_frame.grid(
        row=0,
        column=1,
        padx=8,
        pady=8,
        sticky="nsew"
    )


    tk.Label(
        status_frame,
        text="Status Distribution",
        font=("Segoe UI", 12, "bold"),
        fg="white",
        bg=CARD_COLOR
    ).pack(
        pady=(8, 0)
    )


    try:

        status_fig = Analysis.create_status_chart()

        status_canvas = FigureCanvasTkAgg(
            status_fig,
            master=status_frame
        )

        status_canvas.draw()

        status_canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

    except Exception as e:

        tk.Label(
            status_frame,
            text=f"Unable to load chart\n{e}",
            fg="white",
            bg=CARD_COLOR
        ).pack(
            pady=30
        )


    # ==========================================================
    # BUILDING CHART
    # ==========================================================

    building_frame = tk.Frame(
        charts_frame,
        bg=CARD_COLOR
    )

    building_frame.grid(
        row=1,
        column=0,
        padx=8,
        pady=8,
        sticky="nsew"
    )


    tk.Label(
        building_frame,
        text="Complaints by Building",
        font=("Segoe UI", 12, "bold"),
        fg="white",
        bg=CARD_COLOR
    ).pack(
        pady=(8, 0)
    )


    try:

        building_fig = Analysis.create_building_chart()

        building_canvas = FigureCanvasTkAgg(
            building_fig,
            master=building_frame
        )

        building_canvas.draw()

        building_canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

    except Exception as e:

        tk.Label(
            building_frame,
            text=f"Unable to load chart\n{e}",
            fg="white",
            bg=CARD_COLOR
        ).pack(
            pady=30
        )


    # ==========================================================
    # MONTHLY CHART
    # ==========================================================

    monthly_frame = tk.Frame(
        charts_frame,
        bg=CARD_COLOR
    )

    monthly_frame.grid(
        row=1,
        column=1,
        padx=8,
        pady=8,
        sticky="nsew"
    )


    tk.Label(
        monthly_frame,
        text="Complaints Reported per Month",
        font=("Segoe UI", 12, "bold"),
        fg="white",
        bg=CARD_COLOR
    ).pack(
        pady=(8, 0)
    )


    try:

        monthly_fig = Analysis.create_monthly_chart()

        monthly_canvas = FigureCanvasTkAgg(
            monthly_fig,
            master=monthly_frame
        )

        monthly_canvas.draw()

        monthly_canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

    except Exception as e:

        tk.Label(
            monthly_frame,
            text=f"Unable to load chart\n{e}",
            fg="white",
            bg=CARD_COLOR
        ).pack(
            pady=30
        )


    # ==========================================================
    # COST CHART
    # ==========================================================

    cost_frame = tk.Frame(
        charts_frame,
        bg=CARD_COLOR
    )

    cost_frame.grid(
        row=2,
        column=0,
        columnspan=2,
        padx=8,
        pady=8,
        sticky="nsew"
    )


    tk.Label(
        cost_frame,
        text="Repair Cost by Category",
        font=("Segoe UI", 12, "bold"),
        fg="white",
        bg=CARD_COLOR
    ).pack(
        pady=(8, 0)
    )


    try:

        cost_fig = Analysis.create_cost_chart()

        cost_canvas = FigureCanvasTkAgg(
            cost_fig,
            master=cost_frame
        )

        cost_canvas.draw()

        cost_canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

    except Exception as e:

        tk.Label(
            cost_frame,
            text=f"Unable to load chart\n{e}",
            fg="white",
            bg=CARD_COLOR
        ).pack(
            pady=30
        )


    # Make chart columns expand
    charts_frame.grid_columnconfigure(
        0,
        weight=1
    )

    charts_frame.grid_columnconfigure(
        1,
        weight=1
    )


    # ==========================================================
    # EXPORT BUTTON
    # ==========================================================

    tk.Button(
        scrollable_frame,
        text="Export Complaints CSV",
        command=export_analysis_csv,
        bg=PRIMARY_COLOR,
        fg="#062033",
        font=("Segoe UI", 10, "bold"),
        padx=20,
        pady=8,
        cursor="hand2"
    ).pack(
        pady=20
    )
    

# ---------------------------------------------------------
# BUTTON FRAME
# ---------------------------------------------------------

button_frame = tk.Frame(
    dashboard_frame,
    bg=BG_COLOR
)

button_frame.pack(
    pady=40
)


buttons = [
    ("Register Complaint", register_complaint_window),
    ("View Complaints", view_complaints_window),
    ("Search Complaint", search_complaint_window),
    ("Update Status", update_status_window),
    ("Maintenance Details", maintenance_details_window),
    ("Reports & Analysis", reports_analysis_window)
]


for index, (text, command) in enumerate(buttons):

    button = tk.Button(
        button_frame,
        text=text,
        command=command,
        bg=PRIMARY_COLOR,
        fg="#062033",
        activebackground="#39AFCF",
        activeforeground="#FFFFFF",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        padx=25,
        pady=12,
        cursor="hand2",
        width=20
    )

    row = index // 3
    column = index % 3

    button.grid(
        row=row,
        column=column,
        padx=12,
        pady=12
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

footer = tk.Label(
    root,
    text="CampusFix • College Maintenance Management System",
    bg=BG_COLOR,
    fg=SECONDARY_TEXT,
    font=("Segoe UI", 9)
)

footer.pack(
    pady=(0, 15)
)


# ---------------------------------------------------------
# START APPLICATION
# ---------------------------------------------------------

root.mainloop()