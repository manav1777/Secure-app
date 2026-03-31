from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"
bcrypt = Bcrypt(app)

# In-memory users dictionary with hashed passwords
users = {
    "jack": bcrypt.generate_password_hash("jack").decode("utf-8"),
    # add more users here
}

# Temporary storage for comments
comments = []

# Logging function
def log_activity(username, action, ip):
    timestamp = datetime.datetime.now()
    line = f"{timestamp} | {username} | {action} | {ip}"
    print("Logging:", line)  # debug print
    with open("logs.txt", "a") as f:
        f.write(line + "\n")


#Home
@app.route("/")
def index():
    if "username" not in session:
        return "Access Denied – please <a href='/login'>login</a>"

    # Read logs to count alerts
    failed_logins = {}
    injection_attempts = 0
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
            injection_attempts += 1

    # Count alerts
    alert_count = sum(1 for c in failed_logins.values() if c >= 3) + injection_attempts

    return render_template("index.html", username=session["username"], alert_count=alert_count)

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(f"Attempting login: {username} / {password}")  # debug print

        # temporary bypass for testing
        if username == "jack" and password == "jack":
            session["username"] = username
            print("Login successful")  # debug print
            return redirect("/")

        return "Login Failed"

    return render_template("login.html")


# Comment route
@app.route("/comment", methods=["GET", "POST"])
def comment():
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        content = request.form["content"]
        username = session["username"]
        ip = request.remote_addr

        # Save comment
        comments.append({"user": username, "content": content})
        
        # Log the action
        log_activity(username, "comment_posted", ip)

        return redirect("/comment")

    return render_template("comment.html", comments=comments)

# Logout route
@app.route("/logout")
def logout():
    if "username" in session:
        username = session["username"]
        ip = request.remote_addr
        log_activity(username, "logout", ip)
    session.pop("username", None)
    return redirect("/login")

# Suspicious activity dashboard
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

    # Build alerts
    alerts_list = []

    for user, count in failed_logins.items():
        if count >= 3:
            alerts_list.append(f"Multiple failed logins for {user}: {count} times")

    for inj in injection_attempts:
        alerts_list.append(f"SQL Injection attempt detected: {inj}")

    return render_template("alerts.html", alerts=alerts_list)

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


if __name__ == "__main__":
    app.run(debug=True)