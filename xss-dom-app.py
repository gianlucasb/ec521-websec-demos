from flask import Flask, request, render_template_string, make_response
from datetime import datetime

app = Flask(__name__)

# Track server requests to demonstrate that fragments aren't sent
request_log = []

# HTML template - vulnerability is entirely in client-side JavaScript
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TerrierGreet - DOM XSS Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            background: #0d1117;
            color: #c9d1d9;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding-top: 40px;
        }

        .logo {
            text-align: center;
            margin-bottom: 10px;
        }

        .logo img {
            width: 100px;
            height: auto;
        }

        h1 {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 5px;
            color: #58a6ff;
        }

        .subtitle {
            text-align: center;
            color: #8b949e;
            margin-bottom: 20px;
        }

        .badge {
            text-align: center;
            margin-bottom: 30px;
        }

        .badge span {
            background: #161b22;
            border: 2px solid #58a6ff;
            color: #58a6ff;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .greeting-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 15px;
            padding: 40px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }

        .greeting-card h2 {
            font-size: 2rem;
            color: #c9d1d9;
            margin-bottom: 10px;
        }

        #greeting-name {
            color: #58a6ff;
            font-weight: bold;
        }

        .greeting-card p {
            color: #8b949e;
            margin-top: 15px;
        }

        .try-it-box {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .try-it-box h3 {
            color: #58a6ff;
            margin-bottom: 15px;
            font-size: 1rem;
        }

        .name-input {
            display: flex;
            gap: 10px;
        }

        input[type="text"] {
            flex: 1;
            padding: 12px 15px;
            border: 1px solid #30363d;
            border-radius: 8px;
            background: #0d1117;
            color: #c9d1d9;
            font-size: 1rem;
            font-family: 'Courier New', monospace;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: #58a6ff;
        }

        button {
            padding: 12px 20px;
            background: #238636;
            border: none;
            border-radius: 8px;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }

        button:hover {
            background: #2ea043;
        }

        .server-log {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .server-log h3 {
            color: #f85149;
            margin-bottom: 15px;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .server-log h3::before {
            content: "";
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #f85149;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .log-entries {
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            max-height: 150px;
            overflow-y: auto;
        }

        .log-entry {
            padding: 5px 0;
            border-bottom: 1px solid #21262d;
            color: #7ee787;
        }

        .log-entry:last-child {
            border-bottom: none;
        }

        .no-logs {
            color: #8b949e;
            font-style: italic;
        }

        .info-box {
            margin-top: 20px;
            padding: 20px;
            background: #161b22;
            border-radius: 10px;
            border-left: 4px solid #58a6ff;
        }

        .info-box.warning {
            border-left-color: #d29922;
        }

        .info-box h3 {
            color: #58a6ff;
            margin-bottom: 10px;
            font-size: 0.95rem;
        }

        .info-box.warning h3 {
            color: #d29922;
        }

        .info-box p, .info-box li {
            color: #8b949e;
            font-size: 0.85rem;
            line-height: 1.7;
        }

        .info-box ul {
            margin-top: 10px;
            margin-left: 20px;
        }

        code {
            background: #0d1117;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #79c0ff;
        }

        .code-block {
            background: #0d1117;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            overflow-x: auto;
            border: 1px solid #30363d;
        }

        .code-block code {
            background: none;
            padding: 0;
            color: #79c0ff;
            font-size: 0.85rem;
            white-space: pre;
        }

        .payload-list {
            margin-top: 15px;
        }

        .payload-item {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 10px 15px;
            margin-bottom: 10px;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            color: #ffa657;
            cursor: pointer;
            transition: border-color 0.3s;
        }

        .payload-item:hover {
            border-color: #58a6ff;
        }

        .comparison-table {
            width: 100%;
            margin-top: 15px;
            border-collapse: collapse;
            font-size: 0.85rem;
        }

        .comparison-table th, .comparison-table td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #30363d;
        }

        .comparison-table th {
            background: #0d1117;
            color: #58a6ff;
        }

        .comparison-table td {
            color: #8b949e;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo"><img src="/static/terrier.png" alt="Boston Terrier"></div>
        <h1>TerrierGreet</h1>
        <p class="subtitle">DOM-based XSS Demo - Client-Side Vulnerability</p>

        <div class="badge">
            <span>&#9888; VULNERABLE - DOM XSS</span>
        </div>

        <div class="greeting-card">
            <h2>Welcome, <span id="greeting-name">Guest</span>!</h2>
            <p>Personalize your greeting by adding your name to the URL</p>
        </div>

        <div class="try-it-box">
            <h3>Try It - Enter Your Name</h3>
            <div class="name-input">
                <input type="text" id="name-input" placeholder="Enter your name...">
                <button onclick="updateGreeting()">Greet Me!</button>
            </div>
            <p style="margin-top: 10px; color: #8b949e; font-size: 0.85rem;">
                Or visit: <code>http://localhost:5008/#YourName</code>
            </p>
        </div>

        <div class="server-log">
            <h3>Live Server Log</h3>
            <div class="log-entries">
                {% if logs %}
                    {% for log in logs %}
                    <div class="log-entry">{{ log }}</div>
                    {% endfor %}
                {% else %}
                    <p class="no-logs">No requests logged yet...</p>
                {% endif %}
            </div>
            <p style="margin-top: 15px; color: #f85149; font-size: 0.85rem;">
                <strong>Notice:</strong> The URL fragment (#...) is NEVER sent to the server!
                <br>The server cannot see or block the XSS payload.
            </p>
        </div>

        <div class="info-box warning">
            <h3>&#9888; The Vulnerability</h3>
            <p>This page reads the URL fragment and inserts it using <code>innerHTML</code>:</p>
            <div class="code-block">
<code>// VULNERABLE CODE
var name = decodeURIComponent(location.hash.substring(1));
document.getElementById('greeting-name').innerHTML = name;</code>
            </div>
            <p style="margin-top: 15px;">
                The payload never reaches the server - it stays in the browser.
                WAFs, server logs, and backend filters are completely bypassed!
            </p>
        </div>

        <div class="info-box" style="margin-top: 20px;">
            <h3>Try These Payloads</h3>
            <p>Click a payload to test it (or paste into URL after #):</p>
            <div class="payload-list">
                <div class="payload-item" onclick="testPayload(this.textContent)">&lt;img src=x onerror=alert('DOM-XSS')&gt;</div>
                <div class="payload-item" onclick="testPayload(this.textContent)">&lt;img src=x onerror=alert(document.cookie)&gt;</div>
                <div class="payload-item" onclick="testPayload(this.textContent)">&lt;input onfocus=alert('XSS') autofocus&gt;</div>
                <div class="payload-item" onclick="testPayload(this.textContent)">&lt;marquee onstart=alert('XSS')&gt;</div>
            </div>
            <p style="margin-top: 15px; color: #8b949e; font-size: 0.8rem;">
                <strong>Note:</strong> <code>&lt;svg onload&gt;</code> and <code>&lt;script&gt;</code> tags
                don't work via <code>innerHTML</code> - they only execute during initial page parsing.
                Use event handlers like <code>onerror</code>, <code>onfocus</code>, or <code>onstart</code> instead.
            </p>
        </div>

        <div class="info-box" style="margin-top: 20px;">
            <h3>DOM XSS vs Other XSS Types</h3>
            <table class="comparison-table">
                <tr>
                    <th>Aspect</th>
                    <th>Reflected</th>
                    <th>Stored</th>
                    <th>DOM-based</th>
                </tr>
                <tr>
                    <td><strong>Payload location</strong></td>
                    <td>Request (URL/body)</td>
                    <td>Database</td>
                    <td>Client-side only</td>
                </tr>
                <tr>
                    <td><strong>Server sees payload</strong></td>
                    <td>Yes</td>
                    <td>Yes</td>
                    <td>No</td>
                </tr>
                <tr>
                    <td><strong>Server logs</strong></td>
                    <td>Contains payload</td>
                    <td>Contains payload</td>
                    <td>Clean</td>
                </tr>
                <tr>
                    <td><strong>WAF detection</strong></td>
                    <td>Possible</td>
                    <td>Possible</td>
                    <td>Impossible</td>
                </tr>
                <tr>
                    <td><strong>Vulnerability in</strong></td>
                    <td>Server code</td>
                    <td>Server code</td>
                    <td>Client JS</td>
                </tr>
            </table>
        </div>

        <div class="info-box" style="margin-top: 20px;">
            <h3>Common DOM XSS Sources and Sinks</h3>
            <p><strong>Sources</strong> (where attacker-controlled data comes from):</p>
            <ul>
                <li><code>location.hash</code> - URL fragment (this demo)</li>
                <li><code>location.search</code> - Query parameters</li>
                <li><code>location.href</code> - Full URL</li>
                <li><code>document.referrer</code> - Referring page</li>
                <li><code>postMessage</code> - Cross-window messaging</li>
                <li><code>localStorage / sessionStorage</code> - Browser storage</li>
            </ul>
            <p style="margin-top: 15px;"><strong>Sinks</strong> (dangerous functions that execute/render data):</p>
            <ul>
                <li><code>innerHTML</code> - Parses and renders HTML</li>
                <li><code>document.write()</code> - Writes to document</li>
                <li><code>eval()</code> - Executes JavaScript</li>
                <li><code>setTimeout(string)</code> - Executes string as code</li>
                <li><code>element.src</code> - Can load javascript: URLs</li>
            </ul>
        </div>
    </div>

    <script>
        // VULNERABLE CODE - DOM-based XSS
        // Reads from location.hash (SOURCE) and writes to innerHTML (SINK)
        function loadNameFromHash() {
            if (location.hash) {
                var name = decodeURIComponent(location.hash.substring(1));
                // VULNERABLE: Using innerHTML with untrusted data
                document.getElementById('greeting-name').innerHTML = name;
            }
        }

        // Load on page load
        loadNameFromHash();

        // Also update when hash changes (for single-page app behavior)
        window.addEventListener('hashchange', loadNameFromHash);

        // Update greeting from input field
        function updateGreeting() {
            var name = document.getElementById('name-input').value;
            if (name) {
                // Update the URL hash (this triggers hashchange event)
                location.hash = encodeURIComponent(name);
            }
        }

        // Test payload by setting it as the hash
        function testPayload(payload) {
            location.hash = encodeURIComponent(payload);
        }

        // Allow Enter key to submit
        document.getElementById('name-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                updateGreeting();
            }
        });
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    # Log this request (to show that fragment is NOT included)
    log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] GET / - Fragment: (not sent to server)"
    request_log.append(log_entry)

    # Keep only last 10 entries
    while len(request_log) > 10:
        request_log.pop(0)

    print(f"[SERVER] Request received - URL: {request.url}")
    print(f"[SERVER] Notice: URL fragment (#...) is NOT visible to server!")

    response = make_response(render_template_string(HOME_TEMPLATE, logs=request_log))

    # Cookie WITHOUT HttpOnly - vulnerable to theft via XSS
    response.set_cookie("secret", "s3cr3t")

    # NO CSP header - no protection against inline scripts

    return response


@app.route("/logs")
def get_logs():
    """API endpoint to fetch server logs (for demo purposes)"""
    return {"logs": request_log}


if __name__ == "__main__":
    print("\n" + "="*60)
    print("TerrierGreet - DOM-based XSS Demo")
    print("="*60)
    print("\nServer starting on http://localhost:5008")
    print("\nTry these URLs:")
    print("  http://localhost:5008/#YourName")
    print("  http://localhost:5008/#<img src=x onerror=alert('XSS')>")
    print("\nNote: The fragment (#...) is NEVER sent to the server!")
    print("="*60 + "\n")

    app.run(debug=True, port=5008)
