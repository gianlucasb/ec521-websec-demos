from flask import Flask, request, render_template_string, make_response, redirect, url_for
import uuid

app = Flask(__name__)

# In-memory storage for notes (in production this would be a database)
notes = {}

# HTML template - VULNERABLE: uses | safe, allowing stored XSS
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TerrierNotes - Stored XSS Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            background: #1a1a2e;
            color: #eee;
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
            color: #e94560;
        }

        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 20px;
        }

        .badge {
            text-align: center;
            margin-bottom: 30px;
        }

        .badge span {
            background: #16213e;
            border: 2px solid #e94560;
            color: #e94560;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .create-form {
            background: #16213e;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }

        .create-form h2 {
            color: #e94560;
            margin-bottom: 15px;
            font-size: 1.2rem;
        }

        .form-group {
            margin-bottom: 15px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #aaa;
            font-size: 0.9rem;
        }

        input[type="text"], textarea {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #0f3460;
            border-radius: 8px;
            background: #0f3460;
            color: #eee;
            font-size: 1rem;
            font-family: 'Courier New', monospace;
        }

        textarea {
            min-height: 100px;
            resize: vertical;
        }

        input[type="text"]:focus, textarea:focus {
            outline: none;
            border-color: #e94560;
        }

        button {
            padding: 12px 25px;
            background: #e94560;
            border: none;
            border-radius: 8px;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }

        button:hover {
            background: #c73e54;
        }

        .notes-list {
            margin-top: 30px;
        }

        .notes-list h2 {
            color: #e94560;
            margin-bottom: 15px;
            font-size: 1.2rem;
        }

        .note-item {
            background: #16213e;
            border-radius: 10px;
            padding: 15px 20px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: transform 0.2s;
        }

        .note-item:hover {
            transform: translateX(5px);
        }

        .note-item a {
            color: #eee;
            text-decoration: none;
            font-size: 1.1rem;
        }

        .note-item a:hover {
            color: #e94560;
        }

        .note-date {
            color: #666;
            font-size: 0.8rem;
        }

        .no-notes {
            color: #666;
            text-align: center;
            padding: 30px;
            font-style: italic;
        }

        .info-box {
            margin-top: 30px;
            padding: 20px;
            background: #16213e;
            border-radius: 10px;
            border-left: 4px solid #e94560;
        }

        .info-box h3 {
            color: #e94560;
            margin-bottom: 10px;
            font-size: 0.95rem;
        }

        .info-box p {
            color: #aaa;
            font-size: 0.85rem;
            line-height: 1.7;
        }

        code {
            background: #0f3460;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #e94560;
        }

        .code-block {
            background: #0a0a15;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            overflow-x: auto;
        }

        .code-block code {
            background: none;
            padding: 0;
            color: #e94560;
            font-size: 0.85rem;
            white-space: pre;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo"><img src="/static/terrier.png" alt="Boston Terrier"></div>
        <h1>TerrierNotes</h1>
        <p class="subtitle">Stored XSS Demo - No Sanitization</p>

        <div class="badge">
            <span>&#9888; VULNERABLE - NO PROTECTION</span>
        </div>

        <div class="create-form">
            <h2>Create New Note</h2>
            <form method="POST" action="/create">
                <div class="form-group">
                    <label for="title">Title</label>
                    <input type="text" id="title" name="title" placeholder="Enter note title..." required>
                </div>
                <div class="form-group">
                    <label for="content">Content</label>
                    <textarea id="content" name="content" placeholder="Enter note content..." required></textarea>
                </div>
                <button type="submit">Save Note</button>
            </form>
        </div>

        <div class="notes-list">
            <h2>Your Notes</h2>
            {% if notes %}
                {% for note_id, note in notes.items() %}
                <div class="note-item">
                    <a href="/note/{{ note_id }}">{{ note.title | safe }}</a>
                    <span class="note-date">Click to view</span>
                </div>
                {% endfor %}
            {% else %}
                <p class="no-notes">No notes yet. Create your first note above!</p>
            {% endif %}
        </div>

        <div class="info-box">
            <h3>&#9888; Stored XSS Vulnerability</h3>
            <p>
                This app stores notes <strong>without sanitization</strong>. Any HTML or JavaScript
                in note titles or content is rendered directly in the page.
            </p>
            <p style="margin-top: 15px;">
                <strong>Unlike Reflected XSS:</strong>
                <br>- The malicious script is <strong>stored</strong> on the server
                <br>- <strong>Every user</strong> who views the note is affected
                <br>- No need to trick users into clicking a special link
            </p>
        </div>

        <div class="info-box" style="margin-top: 20px;">
            <h3>Try These Payloads</h3>
            <p>Create a note with these titles or content:</p>
            <div class="code-block">
<code>&lt;script&gt;alert('Stored XSS!')&lt;/script&gt;

&lt;img src=x onerror="alert(document.cookie)"&gt;

&lt;script&gt;alert('Cookie: ' + document.cookie)&lt;/script&gt;</code>
            </div>
            <p style="margin-top: 15px;">
                The script will execute for <strong>anyone</strong> who visits this page or views the note!
            </p>
        </div>
    </div>
</body>
</html>
"""

NOTE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ note.title | safe }} - TerrierNotes</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            background: #1a1a2e;
            color: #eee;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding-top: 40px;
        }

        .back-link {
            margin-bottom: 20px;
        }

        .back-link a {
            color: #e94560;
            text-decoration: none;
            font-size: 0.9rem;
        }

        .back-link a:hover {
            text-decoration: underline;
        }

        .note-card {
            background: #16213e;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }

        .note-title {
            color: #e94560;
            font-size: 1.8rem;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #0f3460;
        }

        .note-content {
            color: #ccc;
            font-size: 1.1rem;
            line-height: 1.8;
            white-space: pre-wrap;
        }

        .info-box {
            margin-top: 30px;
            padding: 20px;
            background: #16213e;
            border-radius: 10px;
            border-left: 4px solid #e94560;
        }

        .info-box h3 {
            color: #e94560;
            margin-bottom: 10px;
            font-size: 0.95rem;
        }

        .info-box p {
            color: #aaa;
            font-size: 0.85rem;
            line-height: 1.7;
        }

        code {
            background: #0f3460;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #e94560;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="back-link">
            <a href="/">&larr; Back to all notes</a>
        </div>

        <div class="note-card">
            <!-- VULNERABLE: Title rendered without escaping -->
            <h1 class="note-title">{{ note.title | safe }}</h1>
            <!-- VULNERABLE: Content rendered without escaping -->
            <div class="note-content">{{ note.content | safe }}</div>
        </div>

        <div class="info-box">
            <h3>&#9888; Why Stored XSS is Dangerous</h3>
            <p>
                This note's content is rendered with <code>| safe</code>,
                which disables HTML escaping. Any script in the content executes
                for <strong>every visitor</strong> to this page.
            </p>
            <p style="margin-top: 10px;">
                Real-world examples: Comment sections, forum posts, user profiles,
                product reviews - anywhere user content is stored and displayed.
            </p>
        </div>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    response = make_response(render_template_string(HOME_TEMPLATE, notes=notes))

    # Cookie WITHOUT HttpOnly - vulnerable to theft via XSS
    response.set_cookie("secret", "s3cr3t")

    # NO CSP header - no protection against inline scripts

    return response


@app.route("/create", methods=["POST"])
def create_note():
    title = request.form.get("title", "")
    content = request.form.get("content", "")

    if title and content:
        note_id = str(uuid.uuid4())[:8]
        notes[note_id] = {
            "title": title,
            "content": content
        }
        print(f"[DEBUG] Created note {note_id}: {title}")

    return redirect(url_for("home"))


@app.route("/note/<note_id>")
def view_note(note_id):
    note = notes.get(note_id)

    if not note:
        return "Note not found", 404

    response = make_response(render_template_string(NOTE_TEMPLATE, note=note))

    # Cookie WITHOUT HttpOnly
    response.set_cookie("secret", "s3cr3t")

    return response


if __name__ == "__main__":
    app.run(debug=True, port=5007)
