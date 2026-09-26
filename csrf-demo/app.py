"""
CSRF Demo - Terrier Bank

A single local Flask site for teaching Cross-Site Request Forgery, meant to
be paired with your own fake phishing email containing a malicious link
(instead of a hosted "attacker" site or a live demo bank like the classic
victorzhou.com/blog/csrf/ post, which is no longer available).

The /transfer endpoint moves money out of the logged-in user's account and
- crucially - accepts plain GET requests. That means a single <a href="...">
link (the kind you'd drop into a phishing email) is enough to trigger it:
no form, no JavaScript, no separate attacker page required.

The app deliberately shows no hints about the vulnerability anywhere in its
own pages - see README.md for the full attack write-up and exploitation
steps to use with your class.

For EC521 Introduction to Cybersecurity.
"""

from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "insecure-secret-key-for-demo"

# In-memory "database" - username -> balance
accounts = {}
# List of dicts: {from, to, amount, description, timestamp}
transfer_log = []

STARTING_BALANCE = 20000.00


@app.route("/")
def index():
    if not session.get("username"):
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page. Accepts ANY username/password - this demo bank doesn't
    actually check credentials, it just needs you to have a session cookie."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()

        if not username:
            flash("Please enter a username and password.")
            return redirect(url_for("login"))

        session["username"] = username
        accounts.setdefault(username, STARTING_BALANCE)
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    balance = accounts.get(username, STARTING_BALANCE)
    my_transfers = [t for t in transfer_log if t["from"] == username]
    return render_template(
        "dashboard.html",
        username=username,
        balance=balance,
        transfers=list(reversed(my_transfers)),
    )


@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    """VULNERABLE endpoint: only checks the session cookie. No CSRF token,
    no Origin/Referer check - and it accepts GET, so a plain hyperlink
    (e.g. one pasted into a phishing email) is enough to trigger a transfer.
    Any site, email, or chat message that gets a logged-in user's browser
    to hit this URL can move their money. See README.md for the full
    write-up and how to build the attack link for class."""
    username = session.get("username")
    if not username:
        return "Not logged in", 401

    to = request.values.get("to", "")
    description = request.values.get("description", "")
    try:
        amount = float(request.values.get("amount", "0"))
    except ValueError:
        amount = 0.0

    print(
        f"[DEBUG] {request.method} /transfer  session_user={username!r}  "
        f"origin={request.headers.get('Origin')!r}  referer={request.headers.get('Referer')!r}  "
        f"to={to!r} amount={amount!r} description={description!r}"
    )

    accounts[username] = accounts.get(username, STARTING_BALANCE) - amount
    transfer_log.append(
        {
            "from": username,
            "to": to,
            "amount": amount,
            "description": description,
            "timestamp": datetime.now().strftime("%b %d, %Y %I:%M %p"),
        }
    )

    flash(f"Transferred ${amount:,.2f} to {to}.")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    print("=" * 60)
    print("CSRF Demo - Terrier Bank")
    print("=" * 60)
    print()
    print("  Bank: http://localhost:5012")
    print()
    print("See README.md for the attack write-up and phishing link to use in class.")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    app.run(host="127.0.0.1", port=5012, debug=True, use_reloader=False)
