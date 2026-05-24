from flask import Flask, render_template, request
import datetime
import os

app = Flask(__name__)

LOG_FILE = "logs/honeypot_logs.txt"

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)


# ---------------- LOG FUNCTION ----------------
def log_activity(event, ip, details):
    with open(LOG_FILE, "a") as file:
        file.write("\n--------------------------")
        file.write(f"\nTime: {datetime.datetime.now()}")
        file.write(f"\nIP: {ip}")
        file.write(f"\nEvent: {event}")
        file.write(f"\nDetails: {details}")
        file.write("\nStatus: SUSPICIOUS\n")


# ---------------- HOME PAGE ----------------
@app.route('/')
def home():
    return render_template('login.html')


# ---------------- AUTHORIZED USER LOGIN ----------------
@app.route('/user-login', methods=['POST'])
def user_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == "employee" and password == "company123":
        return "✅ Welcome employee (Authorized Access)"
    else:
        return "❌ Invalid user credentials"


# ---------------- HONEYPOT LOGIN ----------------
@app.route('/secure-login', methods=['POST'])
def secure_login():
    username = request.form.get('username')
    password = request.form.get('password')
    ip = request.remote_addr

    log_activity("HONEYPOT_LOGIN", ip, f"{username}:{password}")
    print(f"[ALERT] Suspicious secure login attempt from {ip}")

    return "⚠ Invalid credentials"


# ---------------- ADMIN HONEYPOT ----------------
@app.route('/admin')
def admin_panel():
    ip = request.remote_addr

    log_activity("ADMIN_ACCESS", ip, "Tried accessing hidden admin panel")
    print(f"[ALERT] Unauthorized admin access attempt from {ip}")

    return "⚠ Access Denied"


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)