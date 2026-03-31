def analyze_logs():
    with open("logs.txt", "r") as f:
        lines = f.readlines()

    failed_logins = {}
    
    print("\n--- Suspicious Activity Report ---\n")

    for line in lines:
        parts = line.strip().split("|")
        if len(parts) < 4:
            continue

        timestamp, username, action, ip = [p.strip() for p in parts]

        # Count failed logins
        if action == "login_failed":
            failed_logins[username] = failed_logins.get(username, 0) + 1

        # Detect SQL injection attempts
        if "injection" in action:
            print(f"[ALERT] SQL Injection attempt by {username} from {ip} at {timestamp}")

    # Flag too many failed logins
    for user, count in failed_logins.items():
        if count >= 3:
            print(f"[ALERT] Multiple failed logins for {user}: {count} times")

    print("\n--- End of Report ---\n")


if __name__ == "__main__":
    analyze_logs()