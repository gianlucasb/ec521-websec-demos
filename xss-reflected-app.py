from flask import Flask, request, render_template_string, make_response

app = Flask(__name__)

# HTML template with VULNERABLE reflected output
SEARCH_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TerrierSearch - Reflected XSS Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            background: #f5f5f5;
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
            color: #cc0000;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
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
            border-color: #cc0000;
        }

        button {
            padding: 15px 30px;
            background: #cc0000;
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }

        button:hover {
            background: #990000;
        }

        .results-box {
            background: white;
            border: 1px solid #ddd;
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
            color: #cc0000;
            word-break: break-all;
        }

        .no-results {
            color: #999;
            margin-top: 15px;
            font-style: italic;
        }

        .hint-box {
            margin-top: 30px;
            padding: 20px;
            background: white;
            border-radius: 10px;
            border-left: 4px solid #cc0000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .hint-box h3 {
            color: #cc0000;
            margin-bottom: 10px;
            font-size: 0.95rem;
        }

        .hint-box p {
            color: #555;
            font-size: 0.85rem;
            line-height: 1.7;
        }

        code {
            background: #f0f0f0;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #c00;
        }

    </style>
</head>
<body>
    <div class="container">
        <div class="logo"><img src="/static/terrier.png" alt="Boston Terrier"></div>
        <h1>TerrierSearch</h1>
        <p class="subtitle">Reflected XSS Demo</p>

        <form method="GET" action="/">
            <div class="search-box">
                <input type="text" name="q" placeholder="Enter your search query..." value="{{ query if query else '' }}">
                <button type="submit">Search</button>
            </div>
        </form>

        {% if query %}
        <div class="results-box">
            <p class="results-header">Showing results for:</p>
            <!-- VULNERABLE: User input is rendered without escaping! -->
            <p class="query-display">{{ query | safe }}</p>
            <p class="no-results">No results found. Try a different search term.</p>
        </div>
        {% endif %}

        <div class="hint-box">
            <h3>⚠️ Hint for Students</h3>
            <p>
                This search engine reflects your query back on the page.
                What happens if you search for HTML or JavaScript code?
                <br><br>
                Try searching for: <code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code>
                <br><br>
                Or try: <code>&lt;img src=x onerror="alert('XSS')"&gt;</code>
                <br><br>
                Can you steal the secret cookie? Try: <code>&lt;script&gt;alert(document.cookie)&lt;/script&gt;</code>
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

    # VULNERABLE: Passing user input directly to template with | safe
    response = make_response(render_template_string(SEARCH_TEMPLATE, query=query))

    # Set a secret cookie (without HttpOnly flag, so JS can access it!)
    response.set_cookie("secret", "s3cr3t")

    return response


if __name__ == "__main__":
    app.run(debug=True, port=5004)
