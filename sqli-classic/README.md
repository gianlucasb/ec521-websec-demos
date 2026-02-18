# SQL Injection Demo - Classic Attack

A hands-on demonstration of SQL injection vulnerabilities for EC521 Introduction to Cybersecurity.

## Overview

This demo teaches students how SQL injection attacks work by providing a deliberately vulnerable login form. Students will learn to exploit the vulnerability and understand why parameterized queries are essential.

**See also:** Compare with `sqli-secure` (port 5003) to understand how to prevent this attack.

## Learning Objectives

- Understand how SQL injection attacks work
- Learn to identify vulnerable code patterns (string concatenation in queries)
- Practice exploiting a SQL injection vulnerability
- Understand the importance of parameterized queries / prepared statements

## Setup

### Requirements

- Python 3.7+
- Flask

### Installation

```bash
pip install -r requirements.txt
```

### Running the App

```bash
python app.py
```

Visit `http://localhost:5001` in your browser.

**Note:** The database is automatically initialized with an `admin` user each time the app starts.

## The Challenge

There is an admin account with a secret password. Your goal: **Login as admin without knowing the password!**

### Hints for Students

1. Try creating a regular account and logging in - observe how it works
2. Think about how the login query might be constructed
3. What happens if you include special SQL characters in your input?
4. Research "SQL injection authentication bypass"

## Solution (For Instructors)

<details>
<summary>Click to reveal solution</summary>

### The Vulnerability

The login query uses string concatenation:

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

### Exploitation Methods

**Method 1: Classic OR injection (in password field)**
- Username: `admin`
- Password: `' OR '1'='1`

This transforms the query into:
```sql
SELECT * FROM users WHERE username = 'admin' AND password = '' OR '1'='1'
```

**Method 2: OR injection in both fields**
- Username: `' OR '1'='1`
- Password: `' OR '1'='1`

This transforms the query into:
```sql
SELECT * FROM users WHERE username = '' OR '1'='1' AND password = '' OR '1'='1'
```

</details>

## Security Vulnerabilities Demonstrated

| Vulnerability | Description |
|--------------|-------------|
| **SQL Injection** | User input directly concatenated into SQL query |
| **No Input Validation** | Special characters not escaped or filtered |
| **Plain Text Passwords** | Passwords stored without hashing (additional issue) |

## How to Fix (Discussion Points)

### 1. Parameterized Queries (Primary Fix)

```python
# VULNERABLE (don't do this!)
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

# SECURE (do this!)
cursor.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (username, password)
)
```

### 2. Use an ORM

ORMs like SQLAlchemy handle parameterization automatically:

```python
user = User.query.filter_by(username=username, password=password).first()
```

### 3. Additional Security Measures

- **Hash passwords**: Use bcrypt, argon2, or similar
- **Input validation**: Whitelist allowed characters
- **Least privilege**: Database user should have minimal permissions
- **WAF**: Web Application Firewall can detect injection patterns

## Watching the Attack

The app prints the executed SQL query to the console. Watch the terminal output to see exactly how your input modifies the query:

```
[DEBUG] Executing query: SELECT * FROM users WHERE username = 'admin' AND password = '' OR '1'='1'
```

## Files

| File | Description |
|------|-------------|
| `app.py` | Flask application with vulnerable login |
| `templates/sqli-login.html` | Login page with hints |
| `templates/sqli-register.html` | User registration page |
| `templates/sqli-dashboard.html` | Dashboard (green for users, red for admin) |
| `requirements.txt` | Python dependencies |
| `README.md` | This documentation |
| `sqli-database.db` | SQLite database (auto-created) |

## Admin Credentials

For testing legitimate login:
- Username: `admin`
- Password: `EC521isCool`

## All Demos in This Series

| Folder | Port | Description |
|--------|------|-------------|
| cookie-demo | 5000 | Cookie manipulation attack |
| **sqli-classic** | 5001 | Classic SQL injection in login form (this demo) |
| sqli-blind | 5002 | Boolean-based blind SQL injection |
| sqli-secure | 5003 | SQL injection prevention with prepared statements |
| xss-reflected | 5004 | Cross-site scripting via search |
| xss-encoded | 5005 | Output encoding only |
| xss-csp | 5006 | Full protection with CSP |
| xss-stored | 5007 | Stored XSS in notes app |
| xss-dom | 5008 | DOM-based XSS |

## License

Educational use only - EC521 Boston University
