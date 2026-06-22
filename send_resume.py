import smtplib
from email.message import EmailMessage

SENDER_EMAIL = "YOUR EMAIL ID HERE"
APP_PASSWORD = "EMAIL APP PASSWORD HERE" #sample :> uin uyinjk tiuytn uh

with open("emails.txt", "r") as f:
    hr_emails = [line.strip() for line in f if line.strip()]

for email in hr_emails:
    msg = EmailMessage()
    msg["Subject"] = "Application for [POSITION HERE]"
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    msg.set_content("""
Dear HR,

# ADD YOUR CONTENT HERE

# Thank you for your time and consideration. 
                    
Yours sincerely,
[NAME]

""")

    with open("MY_RESUME_FILE_NAME.pdf", "rb") as resume:
        msg.add_attachment(
            resume.read(),
            maintype="application",
            subtype="pdf",
            filename="MY_RESUME_FILE_NAME.PDF" #SAME NAME OF PDF IN THE FOLDER
        )

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)

    print(f"Sent to {email}")

print("All emails sent!")