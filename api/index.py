

from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

# ⚠️ Hard-coded credentials (unsafe, use only for local quick test)
SENDER_EMAIL = "aarshikbro21@gmail.com"
SENDER_APP_PASSWORD = "Lumeth12#"
DEFAULT_TO_EMAIL = "rithvikprasannakumr@gmail.com"

def send_via_gmail_smtp(subject, body):
    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = DEFAULT_TO_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        smtp.send_message(msg)

@app.route("/send", methods=["POST"])
def send_email():
    try:
        data = request.get_json()
        subject = data.get("subject", "No Subject")
        body = data.get("body", "Empty Body")
        send_via_gmail_smtp(subject, body)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
