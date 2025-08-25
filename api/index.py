# api/send_email.py
import json, os, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

def handler(request):
    # Vercel Python serverless signature
    if request.method != "POST":
        body = json.dumps({"error": "Use POST /api/send_email"})
        return (body, 405, {"Content-Type": "application/json"})

    try:
        data = request.json() if callable(getattr(request, "json", None)) else json.loads(request.body or "{}")
        subject = data.get("subject", "No Subject")
        message = data.get("message", "Hello!")
        if not SENDER_PASSWORD:
            return (json.dumps({"error": "Missing SENDER_PASSWORD env (Gmail App Password)"}), 500, {"Content-Type": "application/json"})

        _send_gmail(subject, message)
        return (json.dumps({"status": "ok", "message": "Email sent"}), 200, {"Content-Type": "application/json"})
    except Exception as e:
        return (json.dumps({"status": "error", "message": str(e)}), 500, {"Content-Type": "application/json"})

