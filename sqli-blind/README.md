# Blind SQL Injection Demo

A hands-on demonstration of blind SQL injection vulnerabilities for EC521 Introduction to Cybersecurity.

## Overview

This demo teaches students how blind SQL injection works by exploiting information leakage in error messages. Unlike classic SQL injection where you directly see data, blind SQL injection requires asking yes/no questions to extract information one bit at a time.

**See also:** Compare with `sqli-classic` (port 5001) for classic SQL injection.

## Learning Objectives

- Understand the difference between classic and blind SQL injection
- Learn how information leakage enables attacks
- Practice Boolean-based blind SQL injection techniques
- Understand why consistent error messages are important for security

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

Visit `http://localhost:5002` in your browser.

## The Challenge

There is a secret admin account. You don't know the username OR the password. Your goal: **Discover the admin username and log in!**

### The Information Leak

The login form returns different error messages:
- **"User does not exist"** (red) - The username was not found
- **"Password is incorrect"** (yellow) - The username EXISTS but password is wrong

This difference allows you to ask yes/no questions about usernames in the database!

## Solution (For Instructors)

<details>
<summary>Click to reveal solution</summary>

### Step 1: Discover the Username

The admin username is `EC521admin`. Students must discover it character by character using blind SQL injection techniques.

### Step 2: Bruteforce the Username

Use the LIKE operator to test each character by injecting SQL conditions:

If you get "Password is incorrect" → A username matching your condition exists
If you get "User does not exist" → No username matches

### Bruteforce Process:

Students should discover the admin username one character at a time by observing the different error responses.

### Step 3: Login as Admin

Once you know the username is `EC521admin`, use SQL injection techniques to authenticate.

</details>

## Types of Blind SQL Injection

### 1. Boolean-based (This Demo)

- Application returns different responses for true/false conditions
- Attacker asks yes/no questions
- Example: Different error messages, different page content

### 2. Time-based

- Application behavior is identical for true/false
- Attacker uses time delays to infer results
- Example: Using conditional sleep functions in SQL

## Security Vulnerabilities Demonstrated

| Vulnerability | Description |
|--------------|-------------|
| **SQL Injection** | User input concatenated into SQL query |
| **Information Leakage** | Different error messages reveal database state |
| **Username Enumeration** | Can determine if usernames exist |

## How to Fix (Discussion Points)

### 1. Use Generic Error Messages

```python
# VULNERABLE - leaks information
if not user:
    error = "User does not exist"
else:
    error = "Password is incorrect"

# SECURE - no information leakage
error = "Invalid username or password"
```

### 2. Parameterized Queries

```python
# SECURE
cursor.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (username, password)
)
```

### 3. Rate Limiting

Slow down brute-force attempts with rate limiting and account lockout.

### 4. Additional Measures

- Use CAPTCHAs after failed attempts
- Implement account lockout policies
- Log and monitor for suspicious patterns
- Use WAF to detect injection patterns

## Watching the Attack

The app prints executed SQL queries to the console:

```
[DEBUG] Executing login query: SELECT * FROM users WHERE username = '<injected SQL>' AND password = 'x'
[DEBUG] Checking if user exists: SELECT * FROM users WHERE username = '<injected SQL>'
```

## Files

| File | Description |
|------|-------------|
| `app.py` | Flask app with blind SQL injection |
| `templates/sqli-blind-login.html` | Login with information leakage |
| `templates/sqli-blind-register.html` | User registration |
| `templates/sqli-blind-dashboard.html` | Dashboard (green=user, red=admin) |
| `requirements.txt` | Python dependencies |
| `README.md` | This documentation |
| `sqli-blind-database.db` | SQLite database (auto-created) |

## Secret Admin Credentials

For instructor testing only:
- Username: `EC521admin`
- Password: `231asdkl1231`

## Comparison: Classic vs Blind SQL Injection

| Aspect | Classic SQLi | Blind SQLi |
|--------|-------------|------------|
| Data visibility | Direct output | Inferred from behavior |
| Speed | Fast | Slow (character by character) |
| Complexity | Simple | More complex |
| Detectability | Easier to detect | Harder to detect |
| This series | `sqli-classic` (port 5001) | `sqli-blind` (port 5002) |

## All Demos in This Series

| Folder | Port | Description |
|--------|------|-------------|
| cookie-demo | 5000 | Cookie manipulation attack |
| sqli-classic | 5001 | Classic SQL injection in login form |
| **sqli-blind** | 5002 | Boolean-based blind SQL injection (this demo) |
| sqli-secure | 5003 | SQL injection prevention with prepared statements |
| xss-reflected | 5004 | Cross-site scripting via search |
| xss-encoded | 5005 | Output encoding only |
| xss-csp | 5006 | Full protection with CSP |
| xss-stored | 5007 | Stored XSS in notes app |
| xss-dom | 5008 | DOM-based XSS |

## License

Educational use only - EC521 Boston University
