import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_NAME = BASE_DIR  / "campus.db"

def connect_db():
    """Create and return a database connection."""
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    """Create the complaints table if it does not already exist."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            department TEXT NOT NULL,
            building TEXT NOT NULL,
            room_no TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            technician_name TEXT,
            maintenance_details TEXT,
            repair_cost REAL DEFAULT 0,
            complaint_date TEXT NOT NULL,
            updated_date TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_complaint(
    student_name,
    department,
    building,
    room_no,
    category,
    priority,
    description
):
    """Add a new complaint to the database."""

    conn = connect_db()
    cursor = conn.cursor()

    complaint_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO complaints (
            student_name,
            department,
            building,
            room_no,
            category,
            priority,
            description,
            status,
            complaint_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_name,
        department,
        building,
        room_no,
        category,
        priority,
        description,
        "Pending",
        complaint_date
    ))

    ticket_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return ticket_id


def get_all_complaints():
    """Return all complaints from the database."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM complaints
        ORDER BY ticket_id DESC
    """)

    complaints = cursor.fetchall()

    conn.close()

    return complaints


def get_complaint(ticket_id):
    """Return one complaint using its ticket ID."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM complaints
        WHERE ticket_id = ?
    """, (ticket_id,))

    complaint = cursor.fetchone()

    conn.close()

    return complaint


def search_complaints(keyword):
    """Search complaints using ticket ID, student name, building or category."""

    conn = connect_db()
    cursor = conn.cursor()

    search_term = f"%{keyword}%"

    cursor.execute("""
        SELECT *
        FROM complaints
        WHERE
            CAST(ticket_id AS TEXT) LIKE ?
            OR student_name LIKE ?
            OR building LIKE ?
            OR category LIKE ?
            OR status LIKE ?
    """, (
        search_term,
        search_term,
        search_term,
        search_term,
        search_term
    ))

    complaints = cursor.fetchall()

    conn.close()

    return complaints


def update_status(ticket_id, new_status):
    """Update the status of a complaint."""

    conn = connect_db()
    cursor = conn.cursor()

    updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        UPDATE complaints
        SET status = ?,
            updated_date = ?
        WHERE ticket_id = ?
    """, (
        new_status,
        updated_date,
        ticket_id
    ))

    conn.commit()

    rows_updated = cursor.rowcount

    conn.close()

    return rows_updated


def add_maintenance_details(
    ticket_id,
    technician_name,
    maintenance_details,
    repair_cost
):
    """Add maintenance information to a complaint."""

    conn = connect_db()
    cursor = conn.cursor()

    updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        UPDATE complaints
        SET
            technician_name = ?,
            maintenance_details = ?,
            repair_cost = ?,
            updated_date = ?
        WHERE ticket_id = ?
    """, (
        technician_name,
        maintenance_details,
        repair_cost,
        updated_date,
        ticket_id
    ))

    conn.commit()

    rows_updated = cursor.rowcount

    conn.close()

    return rows_updated

def get_all_complaints():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM complaints
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def search_complaints(column, value):
    conn = sqlite3.connect("data/campusfix.db")
    cursor = conn.cursor()

    allowed_columns = {
        "id": "id",
        "student_name": "student_name",
        "department": "department",
        "category": "category",
        "status": "status"
    }

    if column not in allowed_columns:
        conn.close()
        return []

    db_column = allowed_columns[column]

    if column == "id":
        cursor.execute(
            f"""
            SELECT *
            FROM complaints
            WHERE {db_column} = ?
            ORDER BY id DESC
            """,
            (int(value),)
        )
    else:
        cursor.execute(
            f"""
            SELECT *
            FROM complaints
            WHERE {db_column} LIKE ?
            ORDER BY id DESC
            """,
            (f"%{value}%",)
        )

    rows = cursor.fetchall()

    conn.close()

    return rows

def fetch_complaint(ticket_id):
    """Fetch a single complaint using its ticket ID."""

    conn = connect_db()
    cursor = conn.cursor()

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
        (int(ticket_id),)
    )

    row = cursor.fetchone()

    conn.close()

    return row


def update_complaint(
    ticket_id,
    technician_name,
    maintenance_details,
    repair_cost
):
    """Update maintenance details for a complaint."""

    conn = connect_db()
    cursor = conn.cursor()

    updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        UPDATE complaints
        SET
            technician_name = ?,
            maintenance_details = ?,
            repair_cost = ?,
            updated_date = ?
        WHERE ticket_id = ?
        """,
        (
            technician_name,
            maintenance_details,
            float(repair_cost),
            updated_date,
            int(ticket_id)
        )
    )

    conn.commit()

    affected_rows = cursor.rowcount

    conn.close()

    return affected_rows


if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")