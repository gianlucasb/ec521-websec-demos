"""
Same-Origin Policy Demo - Shopping Website

This demo runs TWO servers to simulate different origins:
- Port 5009: shopmart.com (shopping site with payment info)
- Port 5010: evil-ads.com (third-party ad network)

The shopping site embeds two iframes:
1. /deals.html (same origin - localhost:5009)
2. localhost:5010/banner.html (cross-origin - different port = different origin)

Toggle the "SOP Simulation" to see:
- SOP OFF: Simulates a world without SOP (ad can steal credit card!)
- SOP ON: Real browser behavior (cross-origin access blocked)
"""

from flask import Flask, render_template_string
from threading import Thread
import time

# ============================================================
# SHOPMART.COM (Main Shopping Site) - Port 5009
# ============================================================
main_app = Flask(__name__)

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShopMart - Your Trusted Online Store</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            color: #333;
            min-height: 100vh;
        }

        /* Header / Navigation */
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }

        .top-bar {
            background: #1a252f;
            padding: 8px 20px;
            font-size: 0.85rem;
            display: flex;
            justify-content: space-between;
        }

        .top-bar a {
            color: #aaa;
            text-decoration: none;
            margin-left: 20px;
        }

        .top-bar a:hover {
            color: white;
        }

        .nav-main {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px 20px;
            max-width: 1400px;
            margin: 0 auto;
        }

        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .logo-icon {
            background: #e74c3c;
            padding: 8px 12px;
            border-radius: 8px;
        }

        .search-bar {
            flex: 1;
            max-width: 500px;
            margin: 0 30px;
            display: flex;
        }

        .search-bar input {
            flex: 1;
            padding: 12px 20px;
            border: none;
            border-radius: 5px 0 0 5px;
            font-size: 1rem;
        }

        .search-bar button {
            padding: 12px 25px;
            background: #e74c3c;
            border: none;
            color: white;
            border-radius: 0 5px 5px 0;
            cursor: pointer;
            font-weight: bold;
        }

        .nav-icons {
            display: flex;
            gap: 25px;
            align-items: center;
        }

        .nav-icons a {
            color: white;
            text-decoration: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 0.8rem;
        }

        .nav-icons span.icon {
            font-size: 1.5rem;
            margin-bottom: 3px;
        }

        .cart-badge {
            background: #e74c3c;
            color: white;
            border-radius: 50%;
            padding: 2px 8px;
            font-size: 0.75rem;
            margin-left: 5px;
        }

        /* Main Content */
        .main-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 20px;
        }

        /* Checkout Section */
        .checkout-section {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .section-header {
            background: #2c3e50;
            color: white;
            padding: 15px 20px;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .checkout-content {
            padding: 25px;
        }

        /* Order Summary */
        .order-summary {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 25px;
        }

        .order-summary h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }

        .order-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }

        .order-item:last-child {
            border-bottom: none;
        }

        .item-name {
            color: #555;
        }

        .item-price {
            font-weight: bold;
            color: #2c3e50;
        }

        .order-total {
            display: flex;
            justify-content: space-between;
            padding-top: 15px;
            margin-top: 10px;
            border-top: 2px solid #2c3e50;
            font-size: 1.2rem;
            font-weight: bold;
        }

        .order-total .price {
            color: #e74c3c;
        }

        /* Payment Form */
        .payment-section h3 {
            color: #2c3e50;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .card-icons {
            display: flex;
            gap: 10px;
            margin-left: auto;
        }

        .card-icons span {
            background: #f0f0f0;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.8rem;
            color: #666;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }

        .form-group input {
            width: 100%;
            padding: 14px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
            font-family: 'Courier New', monospace;
            transition: border-color 0.3s;
        }

        .form-group input:focus {
            outline: none;
            border-color: #3498db;
        }

        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }

        .sensitive-field {
            position: relative;
        }

        .sensitive-field::after {
            content: "SENSITIVE";
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: #e74c3c;
            color: white;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.65rem;
            font-weight: bold;
        }

        .btn-checkout {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            border: none;
            color: white;
            font-size: 1.2rem;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 10px;
            transition: transform 0.2s;
        }

        .btn-checkout:hover {
            transform: translateY(-2px);
        }

        .security-note {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 15px;
            padding: 12px;
            background: #e8f5e9;
            border-radius: 8px;
            color: #2e7d32;
            font-size: 0.85rem;
        }

        /* Sidebar */
        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .iframe-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .iframe-header {
            padding: 12px 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85rem;
        }

        .same-origin .iframe-header {
            background: #27ae60;
            color: white;
        }

        .cross-origin .iframe-header {
            background: #e74c3c;
            color: white;
        }

        .origin-tag {
            font-family: monospace;
            font-size: 0.75rem;
            background: rgba(255,255,255,0.2);
            padding: 3px 8px;
            border-radius: 10px;
        }

        iframe {
            width: 100%;
            height: 200px;
            border: none;
            display: block;
        }

        /* Demo Controls */
        .demo-controls {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            border-radius: 10px;
            padding: 20px;
            color: white;
        }

        .demo-controls h3 {
            margin-bottom: 15px;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .toggle-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 12px;
        }

        .toggle-label {
            font-size: 0.85rem;
            font-weight: 600;
        }

        .toggle-label.off {
            color: #e74c3c;
        }

        .toggle-label.on {
            color: #2ecc71;
        }

        .toggle-switch {
            position: relative;
            width: 60px;
            height: 30px;
        }

        .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #e74c3c;
            transition: 0.4s;
            border-radius: 30px;
        }

        .slider:before {
            position: absolute;
            content: "";
            height: 24px;
            width: 24px;
            left: 3px;
            bottom: 3px;
            background-color: white;
            transition: 0.4s;
            border-radius: 50%;
        }

        input:checked + .slider {
            background-color: #2ecc71;
        }

        input:checked + .slider:before {
            transform: translateX(30px);
        }

        .demo-description {
            font-size: 0.8rem;
            color: #bbb;
            text-align: center;
            line-height: 1.5;
        }

        .demo-description strong {
            color: white;
        }

        /* Info Box */
        .info-box {
            grid-column: 1 / -1;
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #3498db;
        }

        .info-box h3 {
            color: #2c3e50;
            margin-bottom: 10px;
        }

        .info-box p {
            color: #666;
            line-height: 1.7;
            font-size: 0.9rem;
        }

        code {
            background: #f0f0f0;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: monospace;
            color: #e74c3c;
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="top-bar">
            <div>Free shipping on orders over $50!</div>
            <div>
                <a href="#">Help</a>
                <a href="#">Track Order</a>
                <a href="#">Returns</a>
            </div>
        </div>
        <nav class="nav-main">
            <div class="logo">
                <span class="logo-icon">SM</span>
                ShopMart
            </div>
            <div class="search-bar">
                <input type="text" placeholder="Search for products...">
                <button>Search</button>
            </div>
            <div class="nav-icons">
                <a href="#"><span class="icon">&#128100;</span> Account</a>
                <a href="#"><span class="icon">&#9825;</span> Wishlist</a>
                <a href="#"><span class="icon">&#128722;</span> Cart <span class="cart-badge">3</span></a>
            </div>
        </nav>
    </header>

    <main class="main-content">
        <section class="checkout-section">
            <div class="section-header">
                &#128179; Secure Checkout
            </div>
            <div class="checkout-content">
                <div class="order-summary">
                    <h3>Order Summary</h3>
                    <div class="order-item">
                        <span class="item-name">Wireless Bluetooth Headphones</span>
                        <span class="item-price">$79.99</span>
                    </div>
                    <div class="order-item">
                        <span class="item-name">USB-C Charging Cable (2-pack)</span>
                        <span class="item-price">$14.99</span>
                    </div>
                    <div class="order-item">
                        <span class="item-name">Laptop Stand - Aluminum</span>
                        <span class="item-price">$45.00</span>
                    </div>
                    <div class="order-item">
                        <span class="item-name">Shipping</span>
                        <span class="item-price">FREE</span>
                    </div>
                    <div class="order-total">
                        <span>Total</span>
                        <span class="price">$139.98</span>
                    </div>
                </div>

                <div class="payment-section">
                    <h3>
                        &#128179; Payment Information
                        <div class="card-icons">
                            <span>VISA</span>
                            <span>MC</span>
                            <span>AMEX</span>
                        </div>
                    </h3>

                    <div class="form-group">
                        <label>Cardholder Name</label>
                        <input type="text" id="card-name" value="John D. Smith" readonly>
                    </div>

                    <div class="form-group sensitive-field">
                        <label>Card Number</label>
                        <input type="text" id="card-number" value="4532 8901 2345 6789" readonly>
                    </div>

                    <div class="form-row">
                        <div class="form-group sensitive-field">
                            <label>Expiry Date</label>
                            <input type="text" id="card-expiry" value="09/27" readonly>
                        </div>
                        <div class="form-group sensitive-field">
                            <label>CVV</label>
                            <input type="text" id="card-cvv" value="847" readonly>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Billing Address</label>
                        <input type="text" id="billing-address" value="123 Main Street, Boston, MA 02215" readonly>
                    </div>

                    <button class="btn-checkout">Complete Purchase - $139.98</button>

                    <div class="security-note">
                        &#128274; Your payment information is encrypted and secure
                    </div>
                </div>
            </div>
        </section>

        <aside class="sidebar">
            <div class="demo-controls">
                <h3>&#9881; SOP Demo Controls</h3>
                <div class="toggle-container">
                    <span class="toggle-label off">OFF</span>
                    <label class="toggle-switch">
                        <input type="checkbox" id="sop-toggle">
                        <span class="slider"></span>
                    </label>
                    <span class="toggle-label on">ON</span>
                </div>
                <p class="demo-description" id="toggle-desc">
                    <strong style="color: #e74c3c;">Same-Origin Policy: OFF</strong><br>
                    Any iframe can steal your credit card!
                </p>
            </div>

            <div class="iframe-container same-origin">
                <div class="iframe-header">
                    <span>Today's Deals</span>
                    <span class="origin-tag">localhost:5009</span>
                </div>
                <iframe src="/deals.html" id="deals-iframe"></iframe>
            </div>

            <div class="iframe-container cross-origin">
                <div class="iframe-header">
                    <span>Sponsored Ad</span>
                    <span class="origin-tag">localhost:5010</span>
                </div>
                <iframe src="http://localhost:5010/banner.html" id="ad-iframe"></iframe>
            </div>
        </aside>

        <div class="info-box">
            <h3>&#128218; How This Demo Works</h3>
            <p>
                This page simulates a shopping checkout with your credit card information.
                Two iframes are embedded: a "Deals" widget from the same origin (<code>localhost:5009/deals.html</code>)
                and a third-party ad from a different origin (<code>localhost:5010/banner.html</code>).
                <br><br>
                <strong>SOP OFF:</strong> We simulate a world without the Same-Origin Policy by sending payment data to all iframes.
                Watch the ad steal your credit card!
                <br>
                <strong>SOP ON:</strong> Real browser behavior. The ad tries to access <code>parent.document</code> but gets blocked.
                The deals widget (same origin) can still access the data.
            </p>
        </div>
    </main>

    <script>
        const toggle = document.getElementById('sop-toggle');
        const toggleDesc = document.getElementById('toggle-desc');
        const dealsIframe = document.getElementById('deals-iframe');
        const adIframe = document.getElementById('ad-iframe');

        // Sensitive payment data
        const paymentData = {
            cardName: document.getElementById('card-name').value,
            cardNumber: document.getElementById('card-number').value,
            cardExpiry: document.getElementById('card-expiry').value,
            cardCvv: document.getElementById('card-cvv').value,
            billingAddress: document.getElementById('billing-address').value
        };

        function updateMode() {
            const sopEnabled = toggle.checked;

            if (sopEnabled) {
                toggleDesc.innerHTML = '<strong>Same-Origin Policy: ON</strong><br>Cross-origin iframes cannot access payment data.';

                // Tell iframes to try direct access (real SOP behavior)
                dealsIframe.contentWindow.postMessage({ mode: 'sop-on' }, '*');
                adIframe.contentWindow.postMessage({ mode: 'sop-on' }, '*');
            } else {
                toggleDesc.innerHTML = '<strong style="color: #e74c3c;">Same-Origin Policy: OFF</strong><br>Any iframe can steal your credit card!';

                // Simulate no SOP by sending data to ALL iframes
                dealsIframe.contentWindow.postMessage({
                    mode: 'sop-off',
                    stolenData: paymentData
                }, '*');
                adIframe.contentWindow.postMessage({
                    mode: 'sop-off',
                    stolenData: paymentData
                }, '*');
            }
        }

        toggle.addEventListener('change', updateMode);

        // Wait for iframes to load, then set initial mode
        window.addEventListener('load', () => {
            setTimeout(updateMode, 500);
        });

        // Re-send mode when iframes request it
        window.addEventListener('message', (event) => {
            if (event.data === 'ready') {
                setTimeout(updateMode, 100);
            }
        });
    </script>
</body>
</html>
"""

DEALS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Today's Deals</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0fff0;
            padding: 12px;
            font-size: 13px;
        }

        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
        }

        h3 {
            color: #27ae60;
            font-size: 0.95rem;
        }

        .badge {
            background: #27ae60;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.7rem;
        }

        .deal-item {
            background: white;
            border-radius: 6px;
            padding: 8px 10px;
            margin-bottom: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .deal-name {
            color: #333;
            font-size: 0.8rem;
        }

        .deal-discount {
            color: #e74c3c;
            font-weight: bold;
            font-size: 0.8rem;
        }

        .status-box {
            margin-top: 10px;
            padding: 10px;
            border-radius: 6px;
            font-size: 0.75rem;
        }

        .status-box.success {
            background: #d4edda;
            border: 1px solid #27ae60;
            color: #155724;
        }

        .status-box.info {
            background: #e7f3ff;
            border: 1px solid #3498db;
            color: #004085;
        }

        .stolen-card {
            font-family: monospace;
            background: #f8f9fa;
            padding: 5px;
            margin-top: 5px;
            border-radius: 4px;
            font-size: 0.7rem;
            color: #e74c3c;
        }

        .method {
            font-size: 0.65rem;
            color: #888;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h3>Flash Deals!</h3>
        <span class="badge">SAME ORIGIN</span>
    </div>

    <div class="deal-item">
        <span class="deal-name">Smart Watch</span>
        <span class="deal-discount">-40%</span>
    </div>
    <div class="deal-item">
        <span class="deal-name">Wireless Mouse</span>
        <span class="deal-discount">-25%</span>
    </div>

    <div id="status-box" class="status-box info">
        Waiting for demo mode...
    </div>

    <script>
        const statusBox = document.getElementById('status-box');

        parent.postMessage('ready', '*');

        window.addEventListener('message', (event) => {
            if (event.data.mode === 'sop-off') {
                const data = event.data.stolenData;
                statusBox.className = 'status-box success';
                statusBox.innerHTML = `
                    <strong>Data accessed (SOP OFF):</strong>
                    <div class="stolen-card">${data.cardNumber}</div>
                    <div class="method">Via postMessage simulation</div>
                `;
            } else if (event.data.mode === 'sop-on') {
                try {
                    const cardNum = parent.document.getElementById('card-number').value;
                    statusBox.className = 'status-box success';
                    statusBox.innerHTML = `
                        <strong>Same-origin access allowed:</strong>
                        <div class="stolen-card">${cardNum}</div>
                        <div class="method">Via parent.document (same origin)</div>
                    `;
                } catch (e) {
                    statusBox.className = 'status-box info';
                    statusBox.textContent = 'Access error: ' + e.message;
                }
            }
        });
    </script>
</body>
</html>
"""

@main_app.route('/')
def home():
    return render_template_string(MAIN_TEMPLATE)

@main_app.route('/deals.html')
def deals():
    return render_template_string(DEALS_TEMPLATE)


# ============================================================
# EVIL-ADS.COM (Malicious Ad Network) - Port 5010
# ============================================================
ad_app = Flask(__name__)

AD_BANNER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ad Banner</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 12px;
            font-size: 13px;
            color: #eee;
            min-height: 100%;
        }

        .ad-content {
            text-align: center;
            padding: 10px;
        }

        .ad-content h3 {
            color: #f39c12;
            font-size: 1rem;
            margin-bottom: 5px;
        }

        .ad-content p {
            color: #aaa;
            font-size: 0.75rem;
            margin-bottom: 8px;
        }

        .fake-btn {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 0.8rem;
            cursor: pointer;
        }

        .status-box {
            margin-top: 12px;
            padding: 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            text-align: left;
        }

        .status-box.stolen {
            background: rgba(231, 76, 60, 0.3);
            border: 1px solid #e74c3c;
        }

        .status-box.blocked {
            background: rgba(46, 204, 113, 0.2);
            border: 1px solid #2ecc71;
            color: #2ecc71;
        }

        .status-box.waiting {
            background: rgba(52, 152, 219, 0.2);
            border: 1px solid #3498db;
            color: #3498db;
        }

        .stolen-data {
            font-family: monospace;
            background: rgba(0,0,0,0.3);
            padding: 8px;
            margin-top: 8px;
            border-radius: 4px;
            font-size: 0.7rem;
        }

        .stolen-data div {
            margin-bottom: 3px;
        }

        .label {
            color: #888;
        }

        .value {
            color: #e74c3c;
        }

        .blocked-msg {
            font-family: monospace;
            font-size: 0.65rem;
            background: rgba(0,0,0,0.3);
            padding: 8px;
            margin-top: 8px;
            border-radius: 4px;
            color: #888;
            word-break: break-all;
        }

        .skull {
            font-size: 1.5rem;
        }
    </style>
</head>
<body>
    <div class="ad-content">
        <h3>Win a FREE iPhone!</h3>
        <p>Click here to claim your prize!</p>
        <button class="fake-btn">CLAIM NOW!</button>
    </div>

    <div id="status-box" class="status-box waiting">
        <span class="skull">&#9760;</span> Malicious script waiting...
    </div>

    <script>
        const statusBox = document.getElementById('status-box');

        parent.postMessage('ready', '*');

        window.addEventListener('message', (event) => {
            if (event.data.mode === 'sop-off') {
                const data = event.data.stolenData;
                statusBox.className = 'status-box stolen';
                statusBox.innerHTML = `
                    <strong>&#9760; CREDIT CARD STOLEN!</strong>
                    <div class="stolen-data">
                        <div><span class="label">Card:</span> <span class="value">${data.cardNumber}</span></div>
                        <div><span class="label">Exp:</span> <span class="value">${data.cardExpiry}</span></div>
                        <div><span class="label">CVV:</span> <span class="value">${data.cardCvv}</span></div>
                        <div><span class="label">Name:</span> <span class="value">${data.cardName}</span></div>
                    </div>
                `;
            } else if (event.data.mode === 'sop-on') {
                try {
                    // This will throw a SecurityError!
                    const cardNum = parent.document.getElementById('card-number').value;
                    statusBox.innerHTML = 'Unexpectedly got: ' + cardNum;
                } catch (e) {
                    statusBox.className = 'status-box blocked';
                    statusBox.innerHTML = `
                        <strong>&#128274; ACCESS BLOCKED</strong>
                        <div class="blocked-msg">SecurityError: Blocked cross-origin frame access</div>
                    `;
                }
            }
        });
    </script>
</body>
</html>
"""

@ad_app.route('/banner.html')
def banner():
    return render_template_string(AD_BANNER_TEMPLATE)

@ad_app.route('/')
def ad_home():
    return render_template_string(AD_BANNER_TEMPLATE)


# ============================================================
# RUN BOTH SERVERS
# ============================================================
def run_main_server():
    """Run the main shopping site on port 5009"""
    main_app.run(host='127.0.0.1', port=5009, debug=False, use_reloader=False)

def run_ad_server():
    """Run the evil ad server on port 5010"""
    ad_app.run(host='127.0.0.1', port=5010, debug=False, use_reloader=False)


if __name__ == '__main__':
    print("=" * 60)
    print("Same-Origin Policy Demo - Shopping Website")
    print("=" * 60)
    print()
    print("Starting two servers to simulate different origins:")
    print("  - shopmart.com:   http://localhost:5009")
    print("  - evil-ads.com:   http://localhost:5010")
    print()
    print("Open http://localhost:5009 in your browser")
    print("Press Ctrl+C to stop both servers")
    print("=" * 60)
    print()

    # Start the ad server in a background thread
    ad_thread = Thread(target=run_ad_server, daemon=True)
    ad_thread.start()

    # Give the ad server time to start
    time.sleep(0.5)

    # Run the main server in the foreground
    run_main_server()
