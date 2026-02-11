# CSP Protection Demo - TerrierSearch

A demonstration of **defense in depth** against XSS using Content Security Policy for EC521 Introduction to Cybersecurity.

## Overview

This demo shows how **Content Security Policy (CSP)** provides an additional layer of protection on top of output encoding. Even if encoding fails, CSP blocks malicious scripts.

**This is Step 3 of 3** in the XSS demo progression:
1. **Unsanitized** (port 5004): No protection - vulnerable
2. **Encoded** (port 5005): Output encoding only
3. **CSP + HttpOnly** (port 5006): Full protection (this demo)

## Learning Objectives

- Understand how CSP provides defense in depth
- Learn to read and interpret CSP headers
- See CSP violations in the browser console
- Understand why HttpOnly cookies matter

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

Visit `http://localhost:5006` in your browser.

## Three Layers of Protection

| Layer | Protection | Purpose |
|-------|------------|---------|
| **Output Encoding** | HTML entities escaped | Primary defense |
| **CSP Header** | Inline scripts blocked | Backup if encoding fails |
| **HttpOnly Cookie** | JS can't read cookie | Limits damage if XSS occurs |

## The CSP Header

The server sends this header with every response:

```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'
```

### What This Means

| Directive | Value | Effect |
|-----------|-------|--------|
| `default-src` | `'self'` | Only load resources from same origin |
| `script-src` | `'self'` | Only execute scripts from same origin |
| `style-src` | `'self' 'unsafe-inline'` | Allow inline styles (for demo) |

### What Gets Blocked

- `<script>alert('XSS')</script>` - Inline script
- `<img onerror="alert('XSS')">` - Inline event handler
- `<body onload="alert('XSS')">` - Inline event handler
- `javascript:alert('XSS')` - JavaScript URLs

## Try These Attacks

All attacks are blocked by CSP, even event handlers:

| Payload | Encoding | CSP |
|---------|----------|-----|
| `<script>alert(1)</script>` | Escaped | Blocked |
| `<img src=x onerror=alert(1)>` | Escaped | **Blocked by CSP** |
| `<svg onload=alert(1)>` | Escaped | **Blocked by CSP** |

## Viewing CSP Violations

1. Open Developer Tools (F12)
2. Go to the **Console** tab
3. Submit a payload like `<img src=x onerror=alert(1)>`
4. See the CSP violation:

```
Refused to execute inline event handler because it violates the following
Content Security Policy directive: "script-src 'self'"
```

## Why Defense in Depth Matters

### Scenario: Developer Makes a Mistake

```python
# Somewhere in a large codebase, someone writes:
{{ user_comment | safe }}  # Oops! Forgot this is user input
```

**Without CSP:** XSS executes, cookies stolen, game over.

**With CSP:** Browser blocks the script, attack fails!

### Scenario: New Attack Vector

A new XSS technique bypasses encoding. With CSP, inline scripts are still blocked.

## HttpOnly Cookie

The secret cookie is now protected:

```python
response.set_cookie("secret", "s3cr3t", httponly=True)
```

Even if XSS somehow executed:
- `document.cookie` returns empty string
- Attacker cannot steal the session

## Files

| File | Description |
|------|-------------|
| `app.py` | Flask app with full CSP protection |
| `static/terrier.png` | Logo image |
| `requirements.txt` | Python dependencies |
| `README.md` | This documentation |

## Comparison: All Three Versions

| Feature | Unsanitized | Encoded | CSP+HttpOnly |
|---------|-------------|---------|--------------|
| **Vulnerability** | Vulnerable | Partial | **Secure** |
| Output Encoding | ❌ | ✅ | ✅ |
| CSP Header | ❌ | ❌ | ✅ |
| HttpOnly Cookie | ❌ | ❌ | ✅ |
| `<script>` blocked | ❌ | ✅ | ✅ |
| `javascript:` URLs | ❌ | ❌ | ✅ |
| Cookie protected | ❌ | ❌ | ✅ |
| Defense in depth | ❌ | ❌ | ✅ |

## All Demos in This Series

| Folder | Port | Description |
|--------|------|-------------|
| cookie-demo | 5000 | Cookie manipulation attack |
| sqli-classic | 5001 | Classic SQL injection in login form |
| sqli-blind | 5002 | Boolean-based blind SQL injection |
| sqli-secure | 5003 | SQL injection prevention with prepared statements |
| xss-reflected | 5004 | Cross-site scripting via search (vulnerable) |
| xss-encoded | 5005 | Output encoding only |
| **xss-csp** | 5006 | Full protection with CSP (this demo) |
| xss-stored | 5007 | Stored XSS in notes app |
| xss-dom | 5008 | DOM-based XSS |

## License

Educational use only - EC521 Boston University
