# Cookie Security Demo - Treasure Hunt

A hands-on demonstration of cookie-based authentication vulnerabilities for EC521 Introduction to Cybersecurity.

## Overview

This demo teaches students why cookies should never be trusted for authorization decisions without proper security measures. Students will exploit an insecure cookie to gain "admin" access to a treasure chest.

## Learning Objectives

- Understand how cookies work in web applications
- Learn why client-side data cannot be trusted
- Practice using browser Developer Tools to inspect and modify cookies
- Recognize the importance of server-side validation and signed cookies

## Setup

### Requirements

- Python 3.7+
- Flask

### Installation

```bash
pip install -r cookie-requirements.txt
```

### Running the App

```bash
python cookie-app.py
```

Visit `http://localhost:5000` in your browser.

## The Challenge

When you visit the app, you'll see an empty treasure chest with $0. Your goal: **find the treasure!**

### Hints for Students

1. Open your browser's Developer Tools (F12 or right-click → Inspect)
2. Navigate to the **Application** tab (Chrome) or **Storage** tab (Firefox)
3. Look at **Cookies** → `localhost`
4. Notice anything interesting about the `Admin` cookie?
5. What happens if you change its value and refresh?

## Solution (For Instructors)

<details>
<summary>Click to reveal solution</summary>

The application sets a cookie `Admin=False` when a user visits. To "hack" the app:

1. Open Developer Tools (F12)
2. Go to Application → Cookies → localhost
3. Change the `Admin` cookie value from `False` to `True`
4. Refresh the page
5. Congratulations! You now have $1,000,000!

</details>

## Security Vulnerabilities Demonstrated

This app intentionally contains the following security issues:

| Vulnerability | Description |
|--------------|-------------|
| **No HttpOnly flag** | Cookie can be accessed via JavaScript |
| **No Secure flag** | Cookie is sent over unencrypted connections |
| **No signing/encryption** | Cookie value can be trivially modified |
| **Client-side trust** | Server blindly trusts cookie value for authorization |

## How to Fix (Discussion Points)

1. **Server-side sessions**: Store session data on the server, only send a session ID to the client
2. **Signed cookies**: Use cryptographic signing (e.g., Flask's `session` with `SECRET_KEY`)
3. **JWT tokens**: Use signed/encrypted tokens for authentication claims
4. **HttpOnly & Secure flags**: Prevent JavaScript access and ensure HTTPS-only transmission
5. **Never trust client data**: Always validate and verify on the server

## Files

| File | Description |
|------|-------------|
| `cookie-app.py` | Flask application with insecure cookie handling |
| `templates/cookie-index.html` | Frontend with treasure hunt UI |
| `cookie-requirements.txt` | Python dependencies |
| `cookie-README.md` | This documentation |

## All Demos in This Repository

| Demo | Port | Description |
|------|------|-------------|
| **Cookie Security** | 5000 | Cookie manipulation attack (this demo) |
| SQL Injection | 5001 | Classic SQL injection in login form |
| Blind SQL Injection | 5002 | Boolean-based blind SQL injection |
| Secure SQL | 5003 | SQL injection prevention with prepared statements |
| Reflected XSS | 5004 | Cross-site scripting via search |
| XSS Encoded | 5005 | Output encoding only |
| XSS + CSP | 5006 | Full protection with CSP |

## License

Educational use only - EC521 Boston University
