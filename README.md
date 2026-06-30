# Secure App System

## Overview

The **Secure App System** is a Python and Flask web application that simulates a secure authentication platform with user activity monitoring and basic intrusion detection capabilities. The application demonstrates secure login practices, password hashing, session management, and real-time security event tracking through an interactive dashboard.

This project was built to explore authentication security and demonstrate how security monitoring can help detect suspicious user activity.

---

## Features

* Secure user authentication
* Password hashing using bcrypt
* Session-based authentication
* User registration and login
* Activity logging and monitoring
* Failed login detection
* Suspicious activity alerts
* Security dashboard visualization

---

## Tech Stack

* Python
* Flask
* SQLite
* HTML
* CSS
* bcrypt

---

## How It Works

1. Users create an account or log in.
2. Passwords are securely hashed before storage.
3. User sessions are maintained after successful authentication.
4. Login attempts and user activities are recorded.
5. Failed login attempts trigger security monitoring.
6. Security events are displayed through the monitoring dashboard.

---

## Installation

Install the required dependencies:

```bash
pip install flask bcrypt
```

Run the application:

```bash
python app.py
```

Open your browser:

```text
http://127.0.0.1:5000
```

---

## Skills Demonstrated

* Secure authentication
* Password hashing
* Session management
* Activity monitoring
* Security logging
* Flask web development
* Python programming

---

## Security Concepts Covered

* Password hashing with bcrypt
* Secure user authentication
* Session management
* Failed login detection
* Activity logging
* Basic intrusion monitoring

---

## Key Learning Outcomes

* Implementing secure authentication workflows
* Protecting passwords using bcrypt
* Managing authenticated user sessions
* Monitoring user activity for suspicious behavior
* Building secure web applications with Flask

---

## Future Improvements

* Multi-factor authentication (MFA)
* Role-based access control
* Password reset functionality
* Email verification
* Account lockout after repeated failed logins
* Advanced intrusion detection rules
* Audit log export

---

## Author

**Manav Patel**
Cybersecurity Student
Drexel University