from flask import Flask, request, render_template_string, make_response

app = Flask(__name__)

# HTML template with BOTH output encoding AND CSP protection
# Now with toggles to demonstrate each protection layer
SEARCH_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TerrierSearch - Full CSP Protection</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            background: #e8f5e9;
            color: #333;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding-top: 60px;
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
            color: #2e7d32;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 20px;
        }

        .badge {
            text-align: center;
            margin-bottom: 30px;
        }

        .badge span {
            background: #c8e6c9;
            border: 1px solid #2e7d32;
            color: #2e7d32;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }

        input[type="text"] {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #ddd;
            border-radius: 10px;
            background: white;
            color: #333;
            font-size: 1.1rem;
            font-family: 'Courier New', monospace;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: #2e7d32;
        }

        button {
            padding: 15px 30px;
            background: #2e7d32;
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }

        button:hover {
            background: #1b5e20;
        }

        .results-box {
            background: white;
            border: 1px solid #c8e6c9;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .results-header {
            color: #666;
            margin-bottom: 15px;
            font-size: 0.95rem;
        }

        .query-display {
            font-size: 1.3rem;
            color: #2e7d32;
            word-break: break-all;
        }

        .no-results {
            color: #999;
            margin-top: 15px;
            font-style: italic;
        }

        .info-box {
            margin-top: 30px;
            padding: 20px;
            background: white;
            border-radius: 10px;
            border-left: 4px solid #2e7d32;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .info-box h3 {
            color: #2e7d32;
            margin-bottom: 10px;
            font-size: 0.95rem;
        }

        .info-box p {
            color: #555;
            font-size: 0.85rem;
            line-height: 1.7;
        }

        code {
            background: #e8f5e9;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #2e7d32;
        }

        .code-block {
            background: #263238;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            overflow-x: auto;
        }

        .code-block code {
            background: none;
            padding: 0;
            color: #a5d6a7;
            font-size: 0.85rem;
            white-space: pre;
        }

        .protection-table {
            width: 100%;
            margin-top: 15px;
            border-collapse: collapse;
            font-size: 0.85rem;
        }

        .protection-table th, .protection-table td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        .protection-table th {
            background: #e8f5e9;
            color: #2e7d32;
        }

        .check {
            color: #2e7d32;
            font-weight: bold;
        }

        .cross {
            color: #c62828;
            font-weight: bold;
        }

        .share-link {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #c8e6c9;
        }

        .share-link a {
            color: #2e7d32;
            text-decoration: none;
        }

        .share-link a:hover {
            text-decoration: underline;
        }

        .toggles {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }

        .toggle-group {
            display: flex;
            align-items: center;
            gap: 10px;
            background: white;
            padding: 10px 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .toggle-group label {
            font-weight: 600;
            color: #333;
            cursor: pointer;
        }

        .toggle-switch {
            position: relative;
            width: 50px;
            height: 26px;
        }

        .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .toggle-slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: 0.3s;
            border-radius: 26px;
        }

        .toggle-slider:before {
            position: absolute;
            content: "";
            height: 20px;
            width: 20px;
            left: 3px;
            bottom: 3px;
            background-color: white;
            transition: 0.3s;
            border-radius: 50%;
        }

        input:checked + .toggle-slider {
            background-color: #2e7d32;
        }

        input:checked + .toggle-slider:before {
            transform: translateX(24px);
        }

        .status-on {
            color: #2e7d32;
            font-weight: bold;
        }

        .status-off {
            color: #c62828;
            font-weight: bold;
        }

        .current-status {
            text-align: center;
            margin-bottom: 20px;
            padding: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .current-status h4 {
            margin-bottom: 10px;
            color: #333;
        }

        .status-indicators {
            display: flex;
            justify-content: center;
            gap: 30px;
        }

        .warning-box {
            margin-top: 20px;
            padding: 15px;
            background: #fff3e0;
            border-radius: 10px;
            border-left: 4px solid #ff9800;
        }

        .warning-box h4 {
            color: #e65100;
            margin-bottom: 5px;
        }

        .warning-box p {
            color: #555;
            font-size: 0.85rem;
        }

        .try-this {
            background: #e3f2fd;
            border-left-color: #1976d2;
        }

        .try-this h4 {
            color: #1565c0;
        }

    </style>
</head>
<body>
    <div class="container">
        <div class="logo"><img src="/static/terrier.png" alt="Boston Terrier"></div>
        <h1>TerrierSearch</h1>
        <p class="subtitle">Full Protection - CSP + Encoding + HttpOnly</p>

        <div class="badge">
            {% if csp_enabled and httponly_enabled %}
            <span>🛡️ FULL PROTECTION - DEFENSE IN DEPTH</span>
            {% elif csp_enabled or httponly_enabled %}
            <span style="background: #fff3e0; border-color: #ff9800; color: #e65100;">⚠️ PARTIAL PROTECTION</span>
            {% else %}
            <span style="background: #ffebee; border-color: #c62828; color: #c62828;">🚨 ENCODING ONLY - NO EXTRA PROTECTION</span>
            {% endif %}
        </div>

        <form method="GET" action="/" id="searchForm">
            <div class="toggles">
                <div class="toggle-group">
                    <label for="csp">CSP Header</label>
                    <div class="toggle-switch">
                        <input type="checkbox" id="csp" name="csp" value="1" {{ 'checked' if csp_enabled else '' }} onchange="document.getElementById('searchForm').submit()">
                        <span class="toggle-slider"></span>
                    </div>
                    <span class="{{ 'status-on' if csp_enabled else 'status-off' }}">{{ 'ON' if csp_enabled else 'OFF' }}</span>
                </div>
                <div class="toggle-group">
                    <label for="httponly">HttpOnly Cookie</label>
                    <div class="toggle-switch">
                        <input type="checkbox" id="httponly" name="httponly" value="1" {{ 'checked' if httponly_enabled else '' }} onchange="document.getElementById('searchForm').submit()">
                        <span class="toggle-slider"></span>
                    </div>
                    <span class="{{ 'status-on' if httponly_enabled else 'status-off' }}">{{ 'ON' if httponly_enabled else 'OFF' }}</span>
                </div>
            </div>

            <div class="search-box">
                <input type="text" name="q" placeholder="Enter your search query..." value="{{ query if query else '' }}">
                <button type="submit">Search</button>
            </div>
        </form>

        <div class="current-status">
            <h4>Current Protection Status</h4>
            <div class="status-indicators">
                <span>Output Encoding: <span class="status-on">✓ ON</span></span>
                <span>CSP: <span class="{{ 'status-on' if csp_enabled else 'status-off' }}">{{ '✓ ON' if csp_enabled else '✗ OFF' }}</span></span>
                <span>HttpOnly: <span class="{{ 'status-on' if httponly_enabled else 'status-off' }}">{{ '✓ ON' if httponly_enabled else '✗ OFF' }}</span></span>
            </div>
        </div>

        {% if query %}
        <div class="results-box">
            <p class="results-header">Showing results for:</p>
            <!-- FULLY SECURE: Encoding + CSP + HttpOnly cookie -->
            <p class="query-display">{{ query }}</p>
            <p class="no-results">No results found. Try a different search term.</p>
            <!-- CSP blocks javascript: URLs even in href attributes -->
            <p class="share-link">📤 <a href="{{ query }}">Share this search</a></p>
        </div>
        {% endif %}

        <div class="info-box">
            <h3>🛡️ Defense in Depth</h3>
            <p>
                This version uses <strong>three layers of protection</strong>:
            </p>
            <table class="protection-table">
                <tr>
                    <th>Protection</th>
                    <th>What it does</th>
                    <th>Current</th>
                </tr>
                <tr>
                    <td><strong>Output Encoding</strong></td>
                    <td>Escapes HTML entities</td>
                    <td class="check">✓ Always ON</td>
                </tr>
                <tr>
                    <td><strong>CSP Header</strong></td>
                    <td>Blocks inline scripts</td>
                    <td class="{{ 'check' if csp_enabled else 'cross' }}">{{ '✓ ON' if csp_enabled else '✗ OFF' }}</td>
                </tr>
                <tr>
                    <td><strong>HttpOnly Cookie</strong></td>
                    <td>Hides cookie from JS</td>
                    <td class="{{ 'check' if httponly_enabled else 'cross' }}">{{ '✓ ON' if httponly_enabled else '✗ OFF' }}</td>
                </tr>
            </table>
        </div>

        <div class="info-box" style="margin-top: 20px;">
            <h3>📋 CSP Header</h3>
            {% if csp_enabled %}
            <p>The server sends this Content-Security-Policy header:</p>
            <div class="code-block">
<code>Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'</code>
            </div>
            <p style="margin-top: 15px;">
                <strong>Try these attacks:</strong>
                <br>• <code>&lt;img src=x onerror="alert('XSS')"&gt;</code>
                <br>• <code>javascript:alert(document.cookie)</code> (then click "Share this search")
                <br><br>
                Both are blocked! CSP prevents inline scripts AND javascript: URLs.
                Open the browser console (F12) to see:
            </p>
            <div class="code-block">
<code>Refused to execute inline event handler because it violates
Content Security Policy directive: "script-src 'self'"</code>
            </div>
            {% else %}
            <p><span class="status-off">CSP is currently disabled.</span></p>
            <p style="margin-top: 10px;">
                Without CSP, inline event handlers can execute. Try:
                <br>• <code>javascript:alert(document.cookie)</code> (then click "Share this search")
                <br><br>
                The <code>javascript:</code> URL will execute because there's no CSP to block it!
            </p>
            {% endif %}
        </div>

        <div class="info-box" style="margin-top: 20px;">
            <h3>🍪 HttpOnly Cookie</h3>
            {% if httponly_enabled %}
            <p>The <code>secret</code> cookie has the <code>HttpOnly</code> flag set.</p>
            <p style="margin-top: 10px;">
                Open the browser console (F12) and type:
            </p>
            <div class="code-block">
<code>document.cookie</code>
            </div>
            <p style="margin-top: 10px;">
                The <code>secret</code> cookie is <strong>not visible</strong> to JavaScript!
                Even if XSS somehow executed, it couldn't steal the session cookie.
            </p>
            {% else %}
            <p><span class="status-off">HttpOnly is currently disabled.</span></p>
            <p style="margin-top: 10px;">
                Open the browser console (F12) and type:
            </p>
            <div class="code-block">
<code>document.cookie</code>
            </div>
            <p style="margin-top: 10px;">
                You can see <code>secret=s3cr3t</code>! An XSS attack could steal this cookie.
            </p>
            {% endif %}
        </div>

        {% if not csp_enabled %}
        <div class="warning-box try-this">
            <h4>💡 Try This (CSP is OFF)</h4>
            <p>
                Search for <code>javascript:alert(document.cookie)</code> then click the "Share this search" link.
                {% if httponly_enabled %}
                The alert will show an empty string because HttpOnly protects the cookie.
                {% else %}
                The alert will show <code>secret=s3cr3t</code> - the cookie is exposed!
                {% endif %}
            </p>
        </div>
        {% endif %}

        <div class="info-box" style="margin-top: 20px;">
            <h3>🔒 Why This Matters</h3>
            <p>
                CSP provides <strong>defense in depth</strong>. Even if:
            </p>
            <ul style="margin-top: 10px; margin-left: 20px; color: #555; font-size: 0.85rem; line-height: 1.8;">
                <li>A developer accidentally uses <code>| safe</code> somewhere</li>
                <li>A new injection vector is discovered</li>
                <li>A third-party library has a vulnerability</li>
            </ul>
            <p style="margin-top: 10px;">
                ...the CSP header still blocks script execution!
            </p>
        </div>
    </div>
</body>
</html>
"""


@app.route("/")
def search():
    query = request.args.get("q", "")

    # Toggle states - default to ON for full protection
    csp_enabled = request.args.get("csp", "1") == "1"
    httponly_enabled = request.args.get("httponly", "1") == "1"

    if query:
        print(f"[DEBUG] Search query: {query}")
        print(f"[DEBUG] CSP: {'ON' if csp_enabled else 'OFF'}, HttpOnly: {'ON' if httponly_enabled else 'OFF'}")

    # Render template with toggle states
    response = make_response(render_template_string(
        SEARCH_TEMPLATE,
        query=query,
        csp_enabled=csp_enabled,
        httponly_enabled=httponly_enabled
    ))

    # Cookie - HttpOnly flag controlled by toggle
    response.set_cookie("secret", "s3cr3t", httponly=httponly_enabled)

    # Content Security Policy - controlled by toggle
    if csp_enabled:
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
        )

    return response


if __name__ == "__main__":
    app.run(debug=True, port=5006)
