from pathlib import Path
import sqlite3
import Database
import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "campus.db"

REPORTS_DIR = BASE_DIR / "reports"

REPORTS_DIR.mkdir(exist_ok=True)


def load_complaints():

    conn = Database.connect_db()

    df = pd.read_sql_query(
        "SELECT * FROM complaints",
        conn
    )

    conn.close()

    return df


def load_maintenance():

    complaints = load_complaints()

    if complaints.empty:
        return pd.DataFrame(
            columns=[
                "ticket_id",
                "category",
                "technician_name",
                "maintenance_details",
                "repair_cost"
            ]
        )

    return complaints[
        [
            "ticket_id",
            "category",
            "technician_name",
            "maintenance_details",
            "repair_cost"
        ]
    ].copy()

def calculate_metrics():

    complaints = load_complaints()

    maintenance = load_maintenance()

    total = len(complaints)

    if not complaints.empty:

        status_counts = complaints["status"].value_counts()

        pending = int(
            status_counts.get("Pending", 0)
        )

        in_progress = int(
            status_counts.get("In Progress", 0)
        )

        resolved = int(
            status_counts.get("Resolved", 0)
        )

        most_common_category = (
            complaints["category"]
            .value_counts()
            .index[0]
        )

        most_reported_building = (
            complaints["building"]
            .value_counts()
            .index[0]
        )

    else:

        pending = 0
        in_progress = 0
        resolved = 0

        most_common_category = "N/A"
        most_reported_building = "N/A"

    if not maintenance.empty:

        total_cost = float(
            maintenance["repair_cost"].sum()
        )

        average_cost = float(
            maintenance["repair_cost"].mean()
        )

    else:

        total_cost = 0.0
        average_cost = 0.0

    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "resolved": resolved,
        "total_cost": total_cost,
        "average_cost": average_cost,
        "most_common_category": most_common_category,
        "most_reported_building": most_reported_building
    }


def create_category_chart():

    df = load_complaints()

    fig, ax = plt.subplots(figsize=(7, 4))

    if df.empty:

        ax.text(
            0.5,
            0.5,
            "No complaint data available",
            ha="center",
            va="center"
        )

        ax.axis("off")

        return fig

    counts = df["category"].value_counts()

    counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        "Complaints by Category"
    )

    ax.set_xlabel(
        "Category"
    )

    ax.set_ylabel(
        "Number of Complaints"
    )

    ax.tick_params(
        axis="x",
        rotation=35
    )

    fig.tight_layout()

    return fig


def create_status_chart():

    df = load_complaints()

    fig, ax = plt.subplots(
        figsize=(6, 4)
    )

    if df.empty:

        ax.text(
            0.5,
            0.5,
            "No complaint data available",
            ha="center",
            va="center"
        )

        ax.axis("off")

        return fig

    counts = df["status"].value_counts()

    counts.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )

    ax.set_title(
        "Status Distribution"
    )

    ax.set_ylabel("")

    fig.tight_layout()

    return fig


def create_building_chart():

    df = load_complaints()

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    if df.empty:

        ax.text(
            0.5,
            0.5,
            "No complaint data available",
            ha="center",
            va="center"
        )

        ax.axis("off")

        return fig

    counts = df["building"].value_counts()

    counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        "Complaints by Building"
    )

    ax.set_xlabel(
        "Building"
    )

    ax.set_ylabel(
        "Number of Complaints"
    )

    ax.tick_params(
        axis="x",
        rotation=35
    )

    fig.tight_layout()

    return fig


def create_monthly_chart():

    df = load_complaints()

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    if df.empty:

        ax.text(
            0.5,
            0.5,
            "No complaint data available",
            ha="center",
            va="center"
        )

        ax.axis("off")

        return fig

    df["complaint_date"] = pd.to_datetime(
        df["complaint_date"],
        errors="coerce"
    )

    monthly = (
        df.dropna(subset=["complaint_date"])
        .groupby(
            df["complaint_date"].dt.to_period("M")
        )
        .size()
    )

    if monthly.empty:

        ax.text(
            0.5,
            0.5,
            "No valid dates available",
            ha="center",
            va="center"
        )

        ax.axis("off")

        return fig

    monthly.index = monthly.index.astype(str)

    monthly.plot(
        kind="line",
        marker="o",
        ax=ax
    )

    ax.set_title(
        "Complaints Reported per Month"
    )

    ax.set_xlabel(
        "Month"
    )

    ax.set_ylabel(
        "Number of Complaints"
    )

    fig.tight_layout()

    return fig


def create_cost_chart():

    df = load_complaints()

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    if df.empty:

        ax.text(
            0.5,
            0.5,
            "No maintenance data available",
            ha="center",
            va="center"
        )

        ax.axis("off")

        return fig

    df["repair_cost"] = pd.to_numeric(
        df["repair_cost"],
        errors="coerce"
    ).fillna(0)

    costs = (
        df.groupby("category")["repair_cost"]
        .sum()
        .sort_values(ascending=False)
    )

    if costs.empty or costs.sum() == 0:

        ax.text(
            0.5,
            0.5,
            "No maintenance data available",
            ha="center",
            va="center"
        )

        ax.axis("off")

        return fig

    costs.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        "Repair Cost by Category"
    )

    ax.set_xlabel(
        "Category"
    )

    ax.set_ylabel(
        "Repair Cost (₹)"
    )

    ax.tick_params(
        axis="x",
        rotation=35
    )

    fig.tight_layout()

    return fig
def export_complaints_csv():

    df = load_complaints()

    path = (
        REPORTS_DIR /
        "complaints_report.csv"
    )

    df.to_csv(
        path,
        index=False
    )

    return path