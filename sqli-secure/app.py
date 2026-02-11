import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, g

app = Flask(__name__)
app.secret_key = "insecure-secret-key-for-demo"

DATABASE = "sqli-secure-database.db"


def get_db():
    """Get database connection."""
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Close database connection."""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize database with users table and admin user."""
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Create admin user
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", "EC521isCool"),
    )

    conn.commit()
    conn.close()
    print("[*] Database initialized with admin user")


@app.route("/")
def index():
    """Redirect to login page."""
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page using SECURE parameterized queries."""
    error = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        db = get_db()
        cursor = db.cursor()

        # SECURE: Using parameterized query with placeholders
        # The ? placeholders are replaced safely by the database driver
        # User input is NEVER concatenated into the query string
        query = "SELECT * FROM users WHERE username = ? AND password = ?"

        print(f"[DEBUG] Executing parameterized query: {query}")
        print(f"[DEBUG] Parameters: username={username!r}, password={password!r}")

        try:
            # Pass parameters as a tuple - they are escaped automatically
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                session["logged_in"] = True
                session["username"] = user["username"]
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid username or password"
        except sqlite3.Error as e:
            error = f"Database error: {e}"

    return render_template("sqli-secure-login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registration page."""
    error = None
    success = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if not username or not password:
            error = "Username and password are required"
        else:
            db = get_db()
            cursor = db.cursor()

            try:
                # SECURE: Parameterized query
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password),
                )
                db.commit()
                success = "Account created! You can now login."
            except sqlite3.IntegrityError:
                error = "Username already exists"

    return render_template("sqli-secure-register.html", error=error, success=success)


@app.route("/dashboard")
def dashboard():
    """Dashboard page - shows different content for admin."""
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    username = session.get("username")
    is_admin = username == "admin"

    return render_template("sqli-secure-dashboard.html", username=username, is_admin=is_admin)


@app.route("/logout")
def logout():
    """Logout and clear session."""
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5003)
