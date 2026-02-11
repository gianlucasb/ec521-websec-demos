from flask import Flask, request, render_template_string, make_response

app = Flask(__name__)

# HTML template with OUTPUT ENCODING (no | safe) but NO CSP
SEARCH_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TerrierSearch - Output Encoding Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            background: #fff3e0;
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
            color: #e65100;
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
            background: #ffe0b2;
            border: 1px solid #e65100;
            color: #e65100;
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
            border-color: #e65100;
        }

        button {
            padding: 15px 30px;
            background: #e65100;
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }

        button:hover {
            background: #bf360c;
        }

        .results-box {
            background: white;
            border: 1px solid #ffe0b2;
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
            color: #e65100;
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
            border-left: 4px solid #e65100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .info-box h3 {
            color: #e65100;
            margin-bottom: 10px;
            font-size: 0.95rem;
        }

        .info-box p {
            color: #555;
            font-size: 0.85rem;
            line-height: 1.7;
        }

        code {
            background: #fff3e0;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #e65100;
        }

        .warning-box {
            margin-top: 20px;
            padding: 20px;
            background: #ffebee;
            border-radius: 10px;
            border-left: 4px solid #c62828;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .warning-box h3 {
            color: #c62828;
            margin-bottom: 10px;
            font-size: 0.95rem;
        }

        .warning-box p {
            color: #555;
            font-size: 0.85rem;
            line-height: 1.7;
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
            color: #ffcc80;
            font-size: 0.85rem;
            white-space: pre;
        }

        .share-link {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
        }

        .share-link a {
            color: #e65100;
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
        <p class="subtitle">Output Encoding Demo</p>

        <div class="badge">
            <span>🔶 PARTIAL PROTECTION - ENCODING ONLY</span>
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
            <!-- PARTIALLY SECURE: HTML is escaped, but no CSP backup -->
            <p class="query-display">{{ query }}</p>
            <p class="no-results">No results found. Try a different search term.</p>
            <!-- VULNERABLE: Query used in href - javascript: URLs bypass encoding! -->
            <p class="share-link">📤 <a href="{{ query }}">Share this search</a></p>
        </div>
        {% endif %}

        <div class="info-box">
            <h3>🔶 How Output Encoding Works</h3>
            <p>
                This version uses <strong>output encoding</strong> to escape HTML entities:
            </p>
            <div class="code-block">
<code>&lt;script&gt;  →  &amp;lt;script&amp;gt;
&lt;img&gt;     →  &amp;lt;img&amp;gt;
"          →  &amp;quot;</code>
            </div>
            <p style="margin-top: 15px;">
                Try these attacks - they'll display as text instead of executing:
                <br>• <code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code>
                <br>• <code>&lt;img src=x onerror="alert('XSS')"&gt;</code>
            </p>
        </div>

        <div class="warning-box">
            <h3>⚠️ Encoding Bypass: javascript: URLs</h3>
            <p>
                The "Share this search" link uses your query in an <code>href</code> attribute.
                HTML encoding doesn't protect URL contexts!
            </p>
            <p style="margin-top: 15px;">
                <strong>Try this attack:</strong>
            </p>
            <div class="code-block">
<code>javascript:alert(document.cookie)</code>
            </div>
            <p style="margin-top: 15px;">
                Then click "Share this search" - the JavaScript executes and shows your cookie!
                <br><br>
                This works because <code>javascript:</code> contains no characters that HTML encoding escapes
                (<code>&lt; &gt; " ' &amp;</code>), so it passes through unchanged.
            </p>
        </div>

        <div class="info-box" style="margin-top: 20px;">
            <h3>📚 Why This Matters</h3>
            <ul style="margin-top: 10px; margin-left: 20px; color: #555; font-size: 0.85rem; line-height: 1.8;">
                <li><strong>Context matters:</strong> HTML encoding protects HTML context, not URL context</li>
                <li><strong>Defense in depth:</strong> CSP would block this attack (see port 5006)</li>
                <li><strong>Proper fix:</strong> Validate URLs - only allow <code>http:</code> and <code>https:</code> schemes</li>
            </ul>
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

    # PARTIAL SECURITY: Uses auto-escaping (no | safe) but no CSP
    response = make_response(render_template_string(SEARCH_TEMPLATE, query=query))

    # Cookie WITHOUT HttpOnly - still vulnerable if encoding ever fails
    response.set_cookie("secret", "s3cr3t")

    # NO CSP header - relying only on output encoding

    return response


if __name__ == "__main__":
    app.run(debug=True, port=5005)
