from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import logging
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

logging.basicConfig(
    filename="security.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

csrf = CSRFProtect(app)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[]
)

DATABASE = "secureweb.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        if len(username) < 3 or len(username) > 30:
            return "Username must be between 3 and 30 characters."

        if len(password) < 8 or len(password) > 128:
            return "Password must be between 8 and 128 characters."

        password_hash = generate_password_hash(password)

        connection = get_db_connection()

        try:
            connection.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )

            connection.commit()

            logger.info("New user registered: %s", username)

        except sqlite3.IntegrityError:
            connection.close()
            logger.warning("Registration failed - username already exists: %s", username)
            return "Username already exists."

        connection.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_db_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(user["password_hash"], password):

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            logger.info("Successful login for username: %s", username)

            return redirect(url_for("dashboard"))

        logger.warning("Failed login attempt for username: %s", username)

        return "Invalid username or password."

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


@app.route("/logout")
def logout():

    username = session.get("username")

    session.clear()

    logger.info("User logged out: %s", username)

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=False)
