# Same-Origin Policy Demo

A hands-on demonstration of the Same-Origin Policy (SOP) for EC521 Introduction to Cybersecurity.

## Overview

This demo illustrates why the Same-Origin Policy is essential for web security using a realistic **shopping website checkout page**. It runs **two servers** to simulate different origins:

- **Port 5009**: `shopmart.com` (shopping site with payment info)
- **Port 5010**: `evil-ads.com` (malicious third-party ad network)

The shopping site embeds two iframes:
1. `/deals.html` - Same origin (localhost:5009) - "Today's Deals" widget
2. `localhost:5010/banner.html` - Cross-origin (different port) - Malicious ad

## Learning Objectives

- Understand what the Same-Origin Policy is and why it exists
- See how origins are defined (protocol + host + port)
- Observe the difference between same-origin and cross-origin access
- Understand what would happen if browsers didn't enforce SOP

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

This starts **both** servers automatically. Visit `http://localhost:5009` in your browser.

## The Demo

> **Note:** The "SOP OFF" mode is a simulation. Browsers always enforce the Same-Origin Policy - it cannot be disabled. This demo illustrates the *concept* of what would happen without SOP by having the parent page voluntarily share its data.

### What You'll See

1. **ShopMart Checkout Page**: A realistic shopping cart with credit card payment form
2. **Deals Widget (Same Origin)**: "Today's Deals" from `localhost:5009/deals.html`
3. **Sponsored Ad (Cross-Origin)**: Malicious ad from `localhost:5010/banner.html`
4. **Toggle Switch**: Simulates enabling/disabling the Same-Origin Policy

### Try It

1. **SOP OFF (Default)**: Toggle starts OFF (red)
   - BOTH iframes can access the credit card information
   - Watch the "malicious ad" steal the card number, CVV, and expiry date!
   - This shows what would happen without the Same-Origin Policy

2. **SOP ON**: Toggle ON (green)
   - The Deals widget (same-origin) CAN still read the credit card
   - The Ad (cross-origin) is BLOCKED - cannot steal payment information
   - This is real browser behavior!

## What is the Same-Origin Policy?

The Same-Origin Policy is a critical browser security mechanism that restricts how documents or scripts from one origin can interact with resources from another origin.

### What is an "Origin"?

An origin is defined by three components:
- **Protocol**: `http` vs `https`
- **Host**: `example.com` vs `other.com`
- **Port**: `:80` vs `:8080`

### Examples

| URL A | URL B | Same Origin? |
|-------|-------|--------------|
| `http://example.com/page1` | `http://example.com/page2` | Yes |
| `http://example.com` | `https://example.com` | No (different protocol) |
| `http://example.com` | `http://other.com` | No (different host) |
| `http://localhost:5009` | `http://localhost:5010` | No (different port) |

## Why SOP Matters

Without the Same-Origin Policy:

1. **Any iframe could read your data**: A malicious ad could read your banking page
2. **Session hijacking**: Ads could steal your session cookies
3. **Data theft**: Third-party widgets could extract form data
4. **No isolation**: Every website could access every other website's content

## How This Demo Works

> **Important:** This demo does NOT actually disable the browser's Same-Origin Policy.
> The SOP is always enforced by the browser and cannot be turned off. The "SOP OFF" mode
> is a **simulation** that illustrates what *would* be possible if the SOP didn't exist.

### SOP ON Mode (Real Browser Behavior)

When the toggle is ON, each iframe attempts to directly access the parent's DOM:

```javascript
// Same-origin iframe (deals.html on port 5009) - SUCCEEDS
const cardNumber = parent.document.getElementById('card-number').value;

// Cross-origin iframe (banner.html on port 5010) - BLOCKED BY BROWSER
const cardNumber = parent.document.getElementById('card-number').value;
// Throws: SecurityError: Blocked a frame with origin "http://localhost:5010"
// from accessing a cross-origin frame.
```

This is the **real** Same-Origin Policy in action. The browser blocks the cross-origin iframe.

### SOP OFF Mode (Simulation Only)

When the toggle is OFF, we **simulate** a world without SOP. Since we can't actually disable the browser's security, we fake it:

```javascript
// The PARENT page voluntarily sends its data to all iframes
adIframe.contentWindow.postMessage({
    mode: 'sop-off',
    stolenData: paymentData  // Card number, CVV, expiry, etc.
}, '*');
```

The ad iframe receives this data via a `message` event listener:

```javascript
// In the ad iframe
window.addEventListener('message', (event) => {
    if (event.data.mode === 'sop-off') {
        // Parent handed us the data - display "STOLEN!"
        const cardNumber = event.data.stolenData.cardNumber;
    }
});
```

**What this simulates:** If SOP didn't exist, the ad could directly read `parent.document` and steal any data. We simulate this by having the parent "give away" its data to everyone, which is functionally equivalent to having no security boundary.

**What actually happens:** The parent uses `postMessage()` (a legitimate cross-origin communication API) to explicitly share data. In real life, a page would never do this with sensitive data. The browser's SOP remains fully enforced throughout.

## Security Concepts Demonstrated

| Concept | Description |
|---------|-------------|
| **Same-Origin Policy** | Browser security restricting cross-origin access |
| **Origin** | Protocol + Host + Port |
| **Cross-Origin** | Different origin = different security boundary |
| **Iframe Isolation** | How SOP protects parent documents from untrusted iframes |

## Related Technologies

### Relaxing SOP (When Needed)

- **CORS**: Cross-Origin Resource Sharing - allows servers to specify who can access their resources
- **postMessage**: Safe cross-origin communication with explicit consent
- **document.domain**: Legacy method to relax SOP for subdomains (deprecated)

### Strengthening SOP

- **CSP**: Content Security Policy - additional restrictions on what can run
- **X-Frame-Options**: Prevent your page from being embedded in iframes
- **SameSite Cookies**: Prevent cookies from being sent cross-origin

## Files

| File | Description |
|------|-------------|
| `app.py` | Flask app running both servers (ports 5009 and 5010) |
| `requirements.txt` | Python dependencies |
| `README.md` | This documentation |

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
| **sop-demo** | 5009, 5010 | Same-Origin Policy demonstration (this demo) |

## License

Educational use only - EC521 Boston University
