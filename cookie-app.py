from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route("/")
def index():
    # Check the Admin cookie value
    admin_cookie = request.cookies.get("Admin", None)

    # If no cookie exists, we'll set it to False
    is_admin = admin_cookie == "True"

    # Render the template with the admin status
    response = make_response(render_template("cookie-index.html", is_admin=is_admin))

    # Set the cookie if it doesn't exist (insecurely!)
    if admin_cookie is None:
        response.set_cookie("Admin", "False")  # No httponly, no secure, no signing!

    return response


if __name__ == "__main__":
    app.run(debug=True, port=5000)
