import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, g

app = Flask(__name__)
app.secret_key = "insecure-secret-key-for-demo"

DATABASE = "sqli-blind-database.db"


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

    # Create admin user with secret username
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("EC521admin", "231asdkl1231"),
    )

    conn.commit()
    conn.close()
    print("[*] Database initialized with secret admin user")


@app.route("/")
def index():
    """Redirect to login page."""
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page with blind SQL injection vulnerability."""
    error = None
    error_type = None  # 'user' or 'password' - for styling

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        db = get_db()
        cursor = db.cursor()

        # VULNERABLE SQL QUERY - Blind SQL Injection
        # Step 1: Try full login with username AND password
        login_query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        print(f"[DEBUG] Executing login query: {login_query}")

        try:
            cursor.execute(login_query)
            user = cursor.fetchone()

            if user:
                # Login successful
                session["logged_in"] = True
                session["username"] = user["username"]
                return redirect(url_for("dashboard"))
            else:
                # Login failed - now check WHY to provide different error messages
                # This second query creates the information leak!
                user_check_query = f"SELECT * FROM users WHERE username = '{username}'"
                print(f"[DEBUG] Checking if user exists: {user_check_query}")

                cursor.execute(user_check_query)
                user_exists = cursor.fetchone()

                if user_exists:
                    # Username exists but password was wrong
                    error = "Password is incorrect"
                    error_type = "password"
                else:
                    # Username doesn't exist
                    error = "User does not exist"
                    error_type = "user"

        except sqlite3.Error as e:
            error = f"Database error: {e}"
            error_type = "user"

    return render_template("sqli-blind-login.html", error=error, error_type=error_type)


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
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password),
                )
                db.commit()
                success = "Account created! You can now login."
            except sqlite3.IntegrityError:
                error = "Username already exists"

    return render_template("sqli-blind-register.html", error=error, success=success)


@app.route("/dashboard")
def dashboard():
    """Dashboard page - shows different content for admin."""
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    username = session.get("username")
    is_admin = username == "EC521admin"

    return render_template("sqli-blind-dashboard.html", username=username, is_admin=is_admin)


@app.route("/logout")
def logout():
    """Logout and clear session."""
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5002)
