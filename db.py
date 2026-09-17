import sqlite3
import hashlib


DB_NAME = "complaints.db"


def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_NAME)


def hash_password(password):
    """Convert a password into a secure hash."""
    return hashlib.sha256(password.encode()).hexdigest()


def init_database():
    """Create all required database tables."""

    conn = get_connection()
    cursor = conn.cursor()

    # Complaints table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT UNIQUE NOT NULL,
            student_name TEXT NOT NULL,
            email TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT,
            priority TEXT,
            department TEXT,
            status TEXT DEFAULT 'Pending',
            image_path TEXT,
            created_at TEXT
        )
    """)

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'student',
            created_at TEXT
        )
    """)

    # Create default admin account
    admin_password = hash_password("admin123")

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (name, email, password, role, created_at)
        VALUES (?, ?, ?, ?, datetime('now'))
    """, (
        "Campus Administrator",
        "admin@campus.com",
        admin_password,
        "admin"
    ))

    conn.commit()
    conn.close()


# -------------------------------------------------
# USER FUNCTIONS
# -------------------------------------------------

def register_user(name, email, password):
    """Register a new student."""

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users
            (name, email, password, role, created_at)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (
            name,
            email.lower().strip(),
            hash_password(password),
            "student"
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def authenticate_user(email, password):
    """Check login credentials."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, email, password, role
        FROM users
        WHERE email = ?
    """, (email.lower().strip(),))

    user = cursor.fetchone()

    conn.close()

    if user is None:
        return None

    name, stored_email, stored_password, role = user

    if hash_password(password) == stored_password:

        return {
            "name": name,
            "email": stored_email,
            "role": role
        }

    return None


# -------------------------------------------------
# COMPLAINT FUNCTIONS
# -------------------------------------------------

def add_complaint(
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
):
    """Add a complaint to the database."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints (
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
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        complaint_id,
        student_name,
        email,
        title,
        description,
        category,
        priority,
        department,
        "Pending",
        image_path,
        created_at
    ))

    conn.commit()
    conn.close()


def get_all_complaints():
    """Return all complaints."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM complaints
        ORDER BY id DESC
    """)

    complaints = cursor.fetchall()

    conn.close()

    return complaints


def get_complaint(complaint_id):
    """Find a complaint using its ID."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM complaints
        WHERE complaint_id = ?
    """, (complaint_id,))

    complaint = cursor.fetchone()

    conn.close()

    return complaint


def update_complaint_status(complaint_id, status):
    """Update complaint status."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE complaints
        SET status = ?
        WHERE complaint_id = ?
    """, (status, complaint_id))

    conn.commit()
    conn.close()