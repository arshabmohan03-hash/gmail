from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Gmail credentials
SENDER_EMAIL = "aarshikbro21@gmail.com"
SENDER_PASSWORD = "Lumeth12#"  # 🔑 Replace with Gmail App Password
RECEIVER_EMAIL = "asvinpradeep12@gmail.com"

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        subject = data.get("subject", "No Subject")
        message = data.get("message", "Hello!")

        # Setup email
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Connect to Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()

        return jsonify({"status": "success", "message": "Email sent successfully!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
