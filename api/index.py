
# api/send-email.py
import os, smtplib, json
from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

SENDER_EMAIL = os.getenv("SENDER_EMAIL", "aarshikbro21@gmail.com")

SENDER_EMAIL = "aarshikbro21@gmail.com"
SENDER_PASSWORD = "Lumeth12#"  # 🔑 Replace with Gmail App Password
RECEIVER_EMAIL = "asvinpradeep12@gmail.com"

def _send_gmail(subject: str, message: str):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()

@app.post("/")  # <-- IMPORTANT: route is "/" for serverless function
def send_email():
    try:
        data = request.get_json(force=True, silent=True) or {}
        subject = data.get("subject", "No Subject")
        message = data.get("message", "Hello!")
        if not SENDER_PASSWORD:
            return jsonify({"error": "Missing SENDER_PASSWORD env"}), 500
        _send_gmail(subject, message)
        return jsonify({"status": "ok", "message": "Email sent"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


