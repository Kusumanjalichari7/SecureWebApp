# SecureWebApp 🔐

A cybersecurity learning project demonstrating secure authentication and common web application security controls using Python, Flask, and SQLite.

## Project Overview

SecureWebApp is a locally tested web application with registration, login, and a protected dashboard. It demonstrates secure coding practices and basic security testing against an application running on the developer's own machine.

## Technologies Used

* Python
* Flask
* SQLite
* Flask-WTF
* Flask-Limiter
* Werkzeug
* python-dotenv
* HTML and CSS
* Kali Linux

## Security Features

* **SQL injection prevention:** Parameterized SQL queries.
* **Password security:** Passwords are hashed before storage.
* **CSRF protection:** Authentication forms require valid CSRF tokens.
* **Login rate limiting:** Login attempts are limited to 5 per minute.
* **Input validation:** Username length is limited to 3–30 characters; password length to 8–128 characters.
* **Session authentication:** Dashboard access requires an authenticated session.
* **Session cookie settings:** HttpOnly and SameSite=Lax.
* **Security logging:** Records registration, successful and failed login, and logout events without logging passwords.
* **Secret management:** Flask secret key is loaded from `.env`.
* **Debug mode:** Disabled.

## Project Structure

```text
SecureWebApp/
├── app.py
├── database.py
├── README.md
├── .gitignore
├── .env                 # Local secret; do not upload
├── secureweb.db         # Local database; do not upload
├── security.log         # Local log; do not upload
├── static/
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
└── venv/                # Local virtual environment; do not upload
```

## Run Locally

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install flask python-dotenv flask-wtf flask-limiter werkzeug
   ```

3. Create a `.env` file containing a secret key:

   ```text
   FLASK_SECRET_KEY=replace-with-a-random-secret
   ```

   Generate a random key with:

   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

4. Initialize the database:

   ```bash
   python database.py
   ```

5. Start the application:

   ```bash
   python app.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.

## Security Testing

The following tests were performed against the local application:

| Test                             | Result |
| -------------------------------- | ------ |
| Unauthorized dashboard access    | PASS   |
| SQL injection login attempt      | PASS   |
| POST request without CSRF token  | PASS   |
| Login rate limiting              | PASS   |
| Password hashing                 | PASS   |
| Username and password validation | PASS   |
| Logout and session protection    | PASS   |

The SQL injection test used a crafted username and returned an invalid-credentials response. A POST request without a valid CSRF token was rejected, and repeated login attempts triggered the configured rate limit.

## Architecture

The browser sends requests to the Flask application. Flask handles registration, login, dashboard access, and logout. Authentication data is stored in SQLite, while security events are recorded in `security.log`. Security controls are applied within the application and its authentication flow.

## Scope and Limitations

This project is intended for educational use and local testing. It is not production-deployed. Production use would require additional review and hardening, including HTTPS, production-grade rate-limit storage, and deployment using a production WSGI server.

Security testing should only be performed on systems you own or are authorized to test.

## Author

**Kusumanjali M.**
B.E. Electronics and Communication Engineering
MVJ College of Engineering, Bengaluru

Project focus: Cybersecurity, web application security, and secure coding.
