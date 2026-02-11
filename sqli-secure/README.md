# Secure SQL Demo - Prepared Statements

A demonstration of how to **prevent** SQL injection using parameterized queries for EC521 Introduction to Cybersecurity.

## Overview

This is the secure version of the SQL injection demo. It uses parameterized queries (prepared statements) to safely handle user input, making SQL injection attacks impossible.

**Compare with:** Run `sqli-classic` (port 5001) side-by-side to see the difference between vulnerable and secure implementations.

## Learning Objectives

- Understand how parameterized queries prevent SQL injection
- See the code difference between vulnerable and secure implementations
- Verify that SQL injection attacks fail on properly secured applications

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

Visit `http://localhost:5003` in your browser.

## Try the Attacks

Attempt the same SQL injection attacks that worked on the vulnerable version:

| Attack | Username | Password | Result |
|--------|----------|----------|--------|
| OR injection | `admin` | `' OR '1'='1` | ❌ Fails |
| OR injection (both) | `' OR '1'='1` | `' OR '1'='1` | ❌ Fails |
| Comment injection | `admin'--` | `anything` | ❌ Fails |
| Union injection | `' UNION SELECT * FROM users--` | `x` | ❌ Fails |

**None of these attacks will work!** The input is treated as data, not SQL code.

## The Fix: Parameterized Queries

### Vulnerable Code (DON'T DO THIS)

```python
# User input is concatenated directly into the query string
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```

If `password = "' OR '1'='1"`, the query becomes:
```sql
SELECT * FROM users WHERE username = 'admin' AND password = '' OR '1'='1'
```

### Secure Code (DO THIS)

```python
# User input is passed as parameters, separate from the query
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
```

If `password = "' OR '1'='1"`, the database searches for a password literally equal to `' OR '1'='1` - which doesn't match!

## How Parameterized Queries Work

1. **Query and data are separate**: The SQL query structure is sent to the database first
2. **Parameters are escaped**: The database driver safely escapes all special characters
3. **Data stays data**: User input can never be interpreted as SQL code

```
┌─────────────────────────────────────────────────────────────────────┐
│  Vulnerable: Query + Data mixed together                            │
│  "SELECT * FROM users WHERE ... password = '' OR '1'='1'"           │
│                                                ^^^^^^^^^^^^         │
│                                                Interpreted as SQL!  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  Secure: Query and Data separate                                    │
│  Query:  "SELECT * FROM users WHERE username = ? AND password = ?"  │
│  Data:   ("admin", "' OR '1'='1")  ← Treated as literal strings     │
└─────────────────────────────────────────────────────────────────────┘
```

## Other Prevention Methods

### 1. ORM (Object-Relational Mapping)

ORMs like SQLAlchemy handle parameterization automatically:

```python
# SQLAlchemy example
user = User.query.filter_by(username=username, password=password).first()
```

### 2. Stored Procedures

Pre-compiled database procedures that accept parameters safely.

### 3. Input Validation (Defense in Depth)

While not sufficient alone, validating input adds an extra layer:

```python
import re
if not re.match(r'^[a-zA-Z0-9_]+$', username):
    raise ValueError("Invalid username format")
```

### 4. Least Privilege

Database user should only have necessary permissions (no DROP, no schema changes).

## Files

| File | Description |
|------|-------------|
| `app.py` | Flask app with parameterized queries |
| `templates/sqli-secure-login.html` | Login page explaining the protection |
| `templates/sqli-secure-register.html` | Registration page |
| `templates/sqli-secure-dashboard.html` | Dashboard |
| `requirements.txt` | Python dependencies |
| `README.md` | This documentation |
| `sqli-secure-database.db` | SQLite database (auto-created) |

## Comparison: Vulnerable vs Secure

| Aspect | Vulnerable (`sqli-classic`) | Secure (`sqli-secure`) |
|--------|---------------------------|------------------------------|
| Port | 5001 | 5003 |
| Query method | String concatenation | Parameterized queries |
| `' OR '1'='1` | ✅ Works (bypasses auth) | ❌ Fails |
| `admin'--` | ✅ Works (bypasses auth) | ❌ Fails |
| Theme | Red (danger) | Green (secure) |

## Admin Credentials

For legitimate login testing:
- Username: `admin`
- Password: `EC521isCool`

## All Demos in This Series

| Folder | Port | Description |
|--------|------|-------------|
| cookie-demo | 5000 | Cookie manipulation attack |
| sqli-classic | 5001 | Classic SQL injection in login form |
| sqli-blind | 5002 | Boolean-based blind SQL injection |
| **sqli-secure** | 5003 | SQL injection prevention with prepared statements (this demo) |
| xss-reflected | 5004 | Cross-site scripting via search |
| xss-encoded | 5005 | Output encoding only |
| xss-csp | 5006 | Full protection with CSP |
| xss-stored | 5007 | Stored XSS in notes app |
| xss-dom | 5008 | DOM-based XSS |

## License

Educational use only - EC521 Boston University
