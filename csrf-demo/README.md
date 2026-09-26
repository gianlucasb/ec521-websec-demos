# CSRF Demo - Terrier Bank

A hands-on demonstration of Cross-Site Request Forgery (CSRF) for EC521 Introduction to Cybersecurity.

This is a local rebuild of the classic bank-transfer CSRF walkthrough
popularized by Victor Zhou's ["Definitely Secure Bank" blog post](https://victorzhou.com/blog/csrf/)
(no longer available), so the class exercise keeps working without depending
on an external hosted demo.

**The app itself looks and behaves like a real online bank and contains no
hints about the vulnerability.** Everything about the attack - the write-up,
the exploit URL, and the fix - lives in this README, for you to use however
fits your class (e.g. embedded in a fake phishing email you build yourself).

## Overview

Students log into "Terrier Bank," a fake bank that accepts any
username/password. The `/transfer` endpoint moves money out of the
logged-in user's account, but:

- it only checks the session cookie (no CSRF token, no Origin/Referer check), and
- it accepts plain **GET** requests, not just POST.

That second point is what makes this demo well-suited to an email-based
attack: a single `<a href="...">` link is enough to trigger a transfer - no
form, no JavaScript, no separate "attacker" web page required. Craft your
own fake phishing email containing the malicious link (see below) and send
it to a volunteer, or open it yourself, to demonstrate the attack live.

## Learning Objectives

- Understand how CSRF attacks work and why the browser's automatic cookie
  handling makes them possible
- See why using GET for state-changing actions makes CSRF trivial to deliver
  (a plain link is a full attack payload)
- Practice constructing a CSRF attack URL
- Discuss mitigations: CSRF tokens, SameSite cookies, and never using GET for
  state-changing requests

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

Visit `http://localhost:5012` in your browser.

## The Challenge

1. Log in with any username and password (try your own name).
2. Note your balance ($20,000) on the dashboard.
3. Build a phishing email (a text file, an actual email draft, whatever fits
   your class demo) containing a link like:

   ```
   http://localhost:5012/transfer?to=Evil-Scammers&amount=10000&description=Gotcha!
   ```

4. While still logged in, click the link (or have a volunteer click it).
5. Refresh the dashboard - the balance has silently dropped by $10,000, with
   a new entry in "Recent Activity" showing `Evil-Scammers` as the recipient.

Nothing on the bank's own pages gives this away - the attack link and the
"why" live only in this README, so you control exactly what students see
and when.

## Solution (For Instructors)

<details>
<summary>Click to reveal solution</summary>

### The Vulnerability

```python
@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    username = session.get("username")
    if not username:
        return "Not logged in", 401

    to = request.values.get("to", "")
    amount = float(request.values.get("amount", "0"))
    # ... moves money, no CSRF token check, no Origin/Referer check
```

Because the endpoint accepts `GET` and `request.values` reads from both the
query string and form data, the attack payload is just a URL:

```
http://localhost:5012/transfer?to=Evil-Scammers&amount=10000&description=Gotcha!
```

Anywhere that URL can end up - a phishing email, a chat message, an
`<img src="...">` tag on a malicious page, a link preview bot that
pre-fetches URLs - can trigger the transfer for anyone who's currently
logged into the bank in that browser.

### Why It Works

1. The bank identifies the user solely via a session cookie.
2. Browsers automatically attach cookies to every request to a given site,
   regardless of which page or email initiated the request.
3. The server never checks *where* the request came from (no CSRF token,
   no Origin/Referer validation) or *how* it arrived (GET vs. POST).

</details>

## Security Vulnerabilities Demonstrated

| Vulnerability | Description |
|--------------|-------------|
| **CSRF** | State-changing action has no CSRF token or Origin/Referer check |
| **State-changing GET** | `/transfer` accepts GET, so a single link is a full attack payload |

## How to Fix (Discussion Points)

### 1. Never Use GET for State-Changing Actions

```python
# VULNERABLE
@app.route("/transfer", methods=["GET", "POST"])

# BETTER (removes the "just click this link" attack, though POST alone
# still doesn't stop an auto-submitting form on a malicious page)
@app.route("/transfer", methods=["POST"])
```

### 2. CSRF Tokens (Primary Fix)

1. When the transfer form is rendered, generate a random token and store it
   server-side, tied to the user's session.
2. Embed the token as a hidden field in the form.
3. On submit, verify the token matches before processing the transfer.

```python
import secrets

@app.route("/dashboard")
def dashboard():
    session["csrf_token"] = secrets.token_hex(16)
    ...

@app.route("/transfer", methods=["POST"])
def transfer():
    if not secrets.compare_digest(
        request.form.get("csrf_token", ""), session.get("csrf_token", "")
    ):
        return "CSRF validation failed", 403
    ...
```

As long as the token is never sent as a cookie (it must live in a form field
or header), an attacker forging a request has no way to include it - they
can get your browser to *send* a request, but they can't read anything back
from your session to put in it.

Many web frameworks (Flask-WTF, Django, Rails) have CSRF protection
built in - check for an existing solution before implementing it yourself.

### 3. SameSite Cookies (Defense in Depth)

Setting `SESSION_COOKIE_SAMESITE = "Lax"` or `"Strict"` tells the browser
not to send the session cookie on cross-site requests, which blocks most
CSRF delivered from a different website. It does **not** help against this
demo's exact GET-based attack when the "attacker" page and the bank share a
registrable domain (e.g. two ports on `localhost` count as the same site),
so it's a good complement to CSRF tokens, not a replacement.

### Further Reading

- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)

## Watching the Attack

The app prints each `/transfer` request to the console, including the HTTP
method and any `Origin`/`Referer` headers:

```
[DEBUG] GET /transfer  session_user='alice'  origin=None  referer='file:///.../phishing-email.html'  to='Evil-Scammers' amount=10000.0 description='Gotcha!'
```

## Files

| File | Description |
|------|-------------|
| `app.py` | Flask application with the vulnerable transfer endpoint |
| `templates/login.html` | Terrier Bank login page (accepts any credentials) |
| `templates/dashboard.html` | Account balance, transfer form, and recent activity |
| `requirements.txt` | Python dependencies |
| `README.md` | This documentation, including the full attack write-up |

## All Demos in This Series

| Folder | Port | Description |
|--------|------|-------------|
| cookie-demo | 5000 | Cookie manipulation attack |
| sqli-classic | 5001 | Classic SQL injection in login form |
| sqli-blind | 5002 | Boolean-based blind SQL injection |
| sqli-secure | 5003 | SQL injection prevention with prepared statements |
| xss-reflected | 5004 | Cross-site scripting via search |
| xss-encoded | 5005 | Output encoding only |
| xss-csp | 5006 | Full protection with CSP |
| xss-stored | 5007 | Stored XSS in notes app |
| xss-dom | 5008 | DOM-based XSS |
| sop-demo | 5009, 5010 | Same-Origin Policy boundaries |
| **csrf-demo** | 5012 | Cross-Site Request Forgery via a phishing link (this demo) |

## License

Educational use only - EC521 Boston University
