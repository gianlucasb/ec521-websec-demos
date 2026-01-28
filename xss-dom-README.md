# DOM-based XSS Demo - TerrierGreet

A hands-on demonstration of DOM-based Cross-Site Scripting (XSS) vulnerabilities for EC521 Introduction to Cybersecurity.

## Overview

This demo teaches students how **DOM-based XSS** attacks work. Unlike reflected or stored XSS, the vulnerability exists entirely in client-side JavaScript. The malicious payload never reaches the server - it stays in the browser, making it invisible to server-side security measures.

**See also:**
- **Reflected XSS** (port 5004): `xss-reflected-app.py` - Server reflects payload
- **Stored XSS** (port 5007): `xss-stored-app.py` - Payload stored in database
- **Encoded** (port 5005): `xss-encoded-app.py` - Output encoding defense
- **CSP + HttpOnly** (port 5006): `xss-csp-app.py` - Full protection

## Learning Objectives

- Understand how DOM-based XSS differs from reflected and stored XSS
- Learn about JavaScript sources and sinks
- Recognize why server-side protections don't help against DOM XSS
- Understand the importance of secure client-side coding

## Setup

### Requirements

- Python 3.7+
- Flask

### Installation

```bash
pip install -r xss-dom-requirements.txt
```

### Running the App

```bash
python xss-dom-app.py
```

Visit `http://localhost:5008` in your browser.

## The Challenge

The greeting page reads your name from the URL fragment (`#`). Your goal: **Inject JavaScript that executes entirely in the browser, bypassing all server-side security!**

### Key Insight

Visit these two URLs and compare:
```
http://localhost:5008/#Alice
http://localhost:5008/#<img src=x onerror=alert(document.cookie)>
```

Now check the server logs - **the payload is invisible to the server!**

## Solution (For Instructors)

<details>
<summary>Click to reveal solution</summary>

### The Vulnerability

JavaScript reads from `location.hash` (SOURCE) and writes to `innerHTML` (SINK):

```javascript
// VULNERABLE CODE
var name = decodeURIComponent(location.hash.substring(1));
document.getElementById('greeting-name').innerHTML = name;
```

### Exploitation

Simply append a payload to the URL fragment:

```
http://localhost:5008/#<img src=x onerror=alert('XSS')>
```

### Why Server Can't See It

URL fragments (everything after `#`) are **never sent to the server** per HTTP specification. The server receives:

```
GET / HTTP/1.1
Host: localhost:5008
```

Not:
```
GET /#<script>alert('XSS')</script> HTTP/1.1  # THIS NEVER HAPPENS
```

### Attack Scenario

1. Attacker crafts malicious URL: `http://example.com/#<script>...</script>`
2. Attacker sends link to victim (email, social media, etc.)
3. Victim clicks link
4. Browser loads page, JavaScript reads fragment
5. Malicious script executes in victim's browser
6. Server logs show nothing suspicious

</details>

## DOM XSS Concepts

### Sources (Attacker-Controlled Input)

| Source | Description |
|--------|-------------|
| `location.hash` | URL fragment (#...) - **this demo** |
| `location.search` | Query string (?...) |
| `location.href` | Full URL |
| `document.referrer` | Referring page URL |
| `document.cookie` | If attacker can set cookies |
| `postMessage` | Cross-window messaging |
| `localStorage` | Browser local storage |
| `window.name` | Window name property |

### Sinks (Dangerous Functions)

| Sink | Danger Level | Why |
|------|--------------|-----|
| `innerHTML` | High | Parses and renders HTML |
| `outerHTML` | High | Same as innerHTML |
| `document.write()` | High | Writes directly to document |
| `eval()` | Critical | Executes string as JavaScript |
| `setTimeout(string)` | Critical | Executes string as code |
| `setInterval(string)` | Critical | Executes string as code |
| `Function()` | Critical | Creates function from string |
| `element.src` | Medium | Can execute javascript: URLs |
| `element.href` | Medium | Can execute javascript: URLs |

### Safe Alternatives

| Dangerous | Safe Alternative |
|-----------|------------------|
| `innerHTML` | `textContent` or `innerText` |
| `document.write()` | DOM manipulation methods |
| `eval()` | `JSON.parse()` for JSON |
| `setTimeout(string)` | `setTimeout(function)` |

## DOM XSS vs Other XSS Types

| Aspect | Reflected | Stored | DOM-based |
|--------|-----------|--------|-----------|
| **Payload travels to server** | Yes | Yes | No |
| **Visible in server logs** | Yes | Yes | No |
| **WAF can block** | Yes | Yes | No |
| **Vulnerability location** | Server code | Server code | Client JS |
| **Fix location** | Server | Server | Client |
| **CSP helps?** | Yes | Yes | Yes |

## Why DOM XSS is Dangerous

1. **Invisible to servers** - No logs, no WAF detection, no server-side filtering
2. **Hard to find** - Requires JavaScript code review, not just server code
3. **Common in SPAs** - Single-page applications heavily use client-side routing
4. **Often overlooked** - Security testing focuses on server-side vulnerabilities

## Real-World Examples

- **Google** (2018): DOM XSS in Google Maps via URL parameters
- **Twitter** (2010): DOM XSS in TweetDeck
- **Various SPAs**: React, Angular, Vue apps with unsafe data binding

## Security Vulnerabilities Demonstrated

| Vulnerability | Description |
|--------------|-------------|
| **DOM XSS** | Client-side code uses untrusted input unsafely |
| **Unsafe Sink** | `innerHTML` used with user-controlled data |
| **No Input Validation** | Fragment not validated before use |
| **No CSP** | No Content Security Policy |
| **No HttpOnly Cookie** | Cookie accessible via JavaScript |

## How to Fix (Discussion Points)

### 1. Use Safe Sinks

```javascript
// DANGEROUS - parses HTML
element.innerHTML = userInput;

// SAFE - treats as text only
element.textContent = userInput;
```

### 2. Validate Input

```javascript
// Validate before use
var name = location.hash.substring(1);
if (/^[a-zA-Z0-9 ]+$/.test(name)) {
    element.textContent = name;
}
```

### 3. Use Encoding Libraries

```javascript
// Use a library like DOMPurify
var clean = DOMPurify.sanitize(userInput);
element.innerHTML = clean;
```

### 4. Content Security Policy

CSP can still help by blocking inline event handlers:

```
Content-Security-Policy: script-src 'self'
```

This blocks `onerror=alert()` even if injected via DOM.

### 5. Frameworks with Auto-Escaping

Modern frameworks like React escape by default:

```jsx
// React automatically escapes this
<div>{userInput}</div>
```

## Files

| File | Description |
|------|-------------|
| `xss-dom-app.py` | Flask app serving the vulnerable page |
| `xss-dom-requirements.txt` | Python dependencies |
| `xss-dom-README.md` | This documentation |

## Try These Payloads

| Payload | Effect |
|---------|--------|
| `#<img src=x onerror=alert('XSS')>` | Image error handler |
| `#<img src=x onerror=alert(document.cookie)>` | **Steal the cookie!** |
| `#<input onfocus=alert('XSS') autofocus>` | Autofocus triggers focus event |
| `#<marquee onstart=alert('XSS')>` | Marquee start event |
| `#<video><source onerror=alert('XSS')>` | Video source error |
| `#<details open ontoggle=alert('XSS')>` | Details toggle event |

**Note:** `<script>` tags and `<svg onload>` do NOT work when inserted via `innerHTML` - they only execute during initial page parsing. Use error/focus/toggle event handlers instead.

## Why `<script>` Tags Don't Work with innerHTML

This is a deliberate browser security behavior defined in the HTML5 specification:

| Insertion Method | `<script>` executes? |
|------------------|---------------------|
| Original HTML (page load) | Yes |
| `innerHTML` | **No** |
| `document.write()` | Yes (during parsing) |
| `createElement('script')` + `appendChild` | Yes |

Event handlers (`onerror`, `onfocus`, etc.) still work because they're HTML attributes attached to elements - when the event fires (image fails to load, element gets focus), the browser executes the handler.

```html
<!-- Does NOT execute via innerHTML -->
<script>alert('XSS')</script>

<!-- DOES execute via innerHTML (when image fails to load) -->
<img src=x onerror="alert('XSS')">
```

This is an important lesson: XSS payloads depend on context. What works for reflected/stored XSS (server-rendered) may not work for DOM XSS via innerHTML.

## Observing the Attack

1. Open the browser's Developer Tools (F12)
2. Go to the Network tab
3. Visit `http://localhost:5008/#<script>alert('XSS')</script>`
4. Notice the request shows only `GET /` - no fragment!
5. Check the server terminal - no payload logged
6. Yet the XSS still executes

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
| Stored XSS | 5007 | Stored XSS in note-taking app |
| **DOM XSS** | 5008 | DOM-based XSS via URL fragment (this demo) |

## License

Educational use only - EC521 Boston University
