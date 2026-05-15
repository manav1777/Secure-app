from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"
bcrypt = Bcrypt(app)

# Users (demo account)
users = {
    "jack": bcrypt.generate_password_hash("jack").decode("utf-8"),
}


# ---------------- LOGGING ----------------
def log_activity(username, action, ip):
    timestamp = datetime.datetime.now()
    line = f"{timestamp} | {username} | {action} | {ip}"
    print("Logging:", line)

    with open("logs.txt", "a") as f:
        f.write(line + "\n")


# ---------------- LANDING PAGE ----------------
@app.route("/")
def home():
    return render_template("landing.html")


# ---------------- DEMO LOGIN ----------------
@app.route("/demo")
def demo():
    session["username"] = "demo"
    log_activity("demo", "demo_login", request.remote_addr)
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    try:
        with open("logs.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    activity_feed = []

    failed_logins = {}
    injection_attempts = 0

    for line in lines:
        parts = line.strip().split("|")
        if len(parts) < 4:
            continue

        timestamp, username, action, ip = [p.strip() for p in parts]

        # Build activity feed
        activity_feed.append({
            "time": timestamp,
            "user": username,
            "action": action,
            "ip": ip
        })

        # Alerts logic
        if action == "login_failed":
            failed_logins[username] = failed_logins.get(username, 0) + 1

        if "injection" in action:
            injection_attempts += 1

    alert_count = sum(1 for c in failed_logins.values() if c >= 3) + injection_attempts

    return render_template(
        "index.html",
        username=session["username"],
        alert_count=alert_count,
        activity_feed=activity_feed
    )


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_password = users.get(username)

        if user_password and bcrypt.check_password_hash(user_password, password):
            session["username"] = username
            log_activity(username, "login_success", request.remote_addr)
            return redirect("/dashboard")
        else:
            log_activity(username, "login_failed", request.remote_addr)
            return "Login Failed"

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    if "username" in session:
        log_activity(session["username"], "logout", request.remote_addr)

    session.pop("username", None)
    return redirect("/")


#----------------- Register -----------------

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users:
            message = "Username already exists"
        else:
            hashed = bcrypt.generate_password_hash(password).decode("utf-8")
            users[username] = hashed
            message = "Account created successfully. You can now login."

    return render_template("register.html", message=message)

# ---------------- ALERTS PAGE ----------------
@app.route("/alerts")
def alerts():
    failed_logins = {}
    injection_attempts = []

    try:
        with open("logs.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    for line in lines:
        parts = line.strip().split("|")
        if len(parts) < 4:
            continue

        timestamp, username, action, ip = [p.strip() for p in parts]

        if action == "login_failed":
            failed_logins[username] = failed_logins.get(username, 0) + 1

        if "injection" in action:
            injection_attempts.append(f"{timestamp} | {username} | {ip}")

    alerts_list = []

    for user, count in failed_logins.items():
        if count >= 3:
            alerts_list.append(f"Multiple failed logins for {user}: {count} times")

    for inj in injection_attempts:
        alerts_list.append(f"SQL Injection attempt detected: {inj}")

    return render_template("alerts.html", alerts=alerts_list)


# ---------------- ALERT COUNT API ----------------
@app.route("/alert_count")
def alert_count():
    count = 0

    try:
        with open("logs.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    failed_logins = {}
    injection_attempts = 0

    for line in lines:
        parts = line.strip().split("|")
        if len(parts) < 4:
            continue

        timestamp, username, action, ip = [p.strip() for p in parts]

        if action == "login_failed":
            failed_logins[username] = failed_logins.get(username, 0) + 1

        if "injection" in action:
            injection_attempts += 1

    for user, c in failed_logins.items():
        if c >= 3:
            count += 1

    count += injection_attempts

    return {"count": count}


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)