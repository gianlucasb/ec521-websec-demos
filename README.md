# EC521 Web Security Demos

Hands-on demonstrations of common web security vulnerabilities for EC521 Introduction to Cybersecurity at Boston University.

## Quick Start

Each demo is self-contained in its own directory. To run a demo:

```bash
cd <demo-folder>
pip install -r requirements.txt
python app.py
```

## All Demos

| Folder | Port | Topic | Description |
|--------|------|-------|-------------|
| `cookie-demo` | 5000 | Cookie Security | Exploit insecure cookies to gain admin access |
| `sqli-classic` | 5001 | SQL Injection | Classic SQL injection authentication bypass |
| `sqli-blind` | 5002 | Blind SQL Injection | Boolean-based blind SQL injection via error messages |
| `sqli-secure` | 5003 | Secure SQL | How parameterized queries prevent SQL injection |
| `xss-reflected` | 5004 | Reflected XSS | Cross-site scripting via URL parameters |
| `xss-encoded` | 5005 | Output Encoding | XSS prevention with encoding (and its limits) |
| `xss-csp` | 5006 | CSP Protection | Defense in depth with Content Security Policy |
| `xss-stored` | 5007 | Stored XSS | Persistent XSS in a note-taking app |
| `xss-dom` | 5008 | DOM XSS | Client-side XSS invisible to servers |
| `sop-demo` | 5009, 5010 | Same-Origin Policy | Browser security boundaries between origins |

## Suggested Learning Path

### SQL Injection Series
1. Start with `sqli-classic` - understand basic SQL injection
2. Try `sqli-blind` - learn advanced techniques
3. Compare with `sqli-secure` - understand the fix

### XSS Series
1. Start with `xss-reflected` - understand basic XSS
2. Try `xss-encoded` - see how encoding helps (and its limits)
3. Compare with `xss-csp` - understand defense in depth
4. Explore `xss-stored` - more dangerous persistent XSS
5. Try `xss-dom` - client-side XSS that evades server detection

### Browser Security
- Try `sop-demo` - understand why the Same-Origin Policy exists

## Requirements

- Python 3.7+
- Flask (installed via each demo's `requirements.txt`)

## License

Educational use only - EC521 Boston University
