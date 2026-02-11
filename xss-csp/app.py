from flask import Flask, request, render_template_string, make_response

app = Flask(__name__)

# HTML template with BOTH output encoding AND CSP protection
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

    </style>
</head>
<body>
    <div class="container">
        <div class="logo"><img src="/static/terrier.png" alt="Boston Terrier"></div>
        <h1>TerrierSearch</h1>
        <p class="subtitle">Full Protection - CSP + Encoding + HttpOnly</p>

        <div class="badge">
            <span>🛡️ FULL PROTECTION - DEFENSE IN DEPTH</span>
        </div>

        <form method="GET" action="/">
            <div class="search-box">
                <input type="text" name="q" placeholder="Enter your search query..." value="{{ query if query else '' }}">
                <button type="submit">Search</button>
            </div>
        </form>

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
                    <th>Unsanitized</th>
                    <th>Encoded</th>
                    <th>CSP+HttpOnly</th>
                </tr>
                <tr>
                    <td><strong>Output Encoding</strong></td>
                    <td>Escapes HTML entities</td>
                    <td class="cross">✗</td>
                    <td class="check">✓</td>
                    <td class="check">✓</td>
                </tr>
                <tr>
                    <td><strong>CSP Header</strong></td>
                    <td>Blocks inline scripts</td>
                    <td class="cross">✗</td>
                    <td class="cross">✗</td>
                    <td class="check">✓</td>
                </tr>
                <tr>
                    <td><strong>HttpOnly Cookie</strong></td>
                    <td>Hides cookie from JS</td>
                    <td class="cross">✗</td>
                    <td class="cross">✗</td>
                    <td class="check">✓</td>
                </tr>
            </table>
        </div>

        <div class="info-box" style="margin-top: 20px;">
            <h3>📋 CSP Header</h3>
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
        </div>

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

    if query:
        print(f"[DEBUG] Search query: {query}")

    # FULLY SECURE: Encoding + CSP + HttpOnly
    response = make_response(render_template_string(SEARCH_TEMPLATE, query=query))

    # HttpOnly cookie - JavaScript cannot access it
    response.set_cookie("secret", "s3cr3t", httponly=True)

    # Content Security Policy - blocks ALL inline scripts
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
    )

    return response


if __name__ == "__main__":
    app.run(debug=True, port=5006)
