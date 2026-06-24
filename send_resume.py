import os
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template_string, request, flash, redirect

app = Flask(__name__)
app.secret_key = "super_secret_key_for_flash_messages"

# Professional HTML Page Design
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automated Application Dispatch</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f8f9fa;
            color: #212529;
            margin: 0;
            padding: 60px 20px;
            display: flex;
            justify-content: center;
        }
        .card {
            background: #ffffff;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            max-width: 550px;
            width: 100%;
            border: 1px solid #e9ecef;
        }
        .header {
            margin-bottom: 30px;
        }
        h2 {
            font-size: 24px;
            font-weight: 600;
            color: #1a1f36;
            margin: 0 0 10px 0;
        }
        p {
            font-size: 14px;
            color: #697386;
            line-height: 1.5;
            margin: 0;
        }
        .btn {
            background-color: #5469d4;
            color: white;
            border: none;
            padding: 14px 24px;
            font-size: 15px;
            font-weight: 500;
            border-radius: 6px;
            cursor: pointer;
            width: 100%;
            transition: background-color 0.15s ease;
            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.08);
        }
        .btn:hover {
            background-color: #4353bc;
        }
        .alert {
            padding: 14px 16px;
            border-radius: 6px;
            margin-bottom: 24px;
            font-size: 14px;
            font-weight: 500;
            line-height: 1.4;
        }
        .alert-success {
            background-color: #e3fcef;
            color: #0e6245;
            border: 1px solid #a3e9c9;
        }
        .alert-danger {
            background-color: #fde8e8;
            color: #9b1c1c;
            border: 1px solid #f8b4b4;
        }
    </style>
</head>
<body>

<div class="card">
    <div class="header">
        <h2>Application Dispatcher</h2>
        <p>Trigger the automated mailing pipeline. The system will look for target contacts in <code>emails.txt</code> and attach the specified PDF resume document.</p>
    </div>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    <form action="/send-emails" method="POST">
        <button type="submit" class="btn">Dispatch Applications</button>
    </form>
</div>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/send-emails', methods=['POST'])
def send_emails():
    # --- FILE VALIDATION CHECKS ---
    
    # 1. Check if emails.txt exists and has content
    if not os.path.exists("emails.txt"):
        flash("no email found", "danger")
        return redirect('/')
        
    with open("emails.txt", "r") as f:
        hr_emails = [line.strip() for line in f if line.strip()]
        
    if not hr_emails:
        flash("no email found", "danger")
        return redirect('/')

    # 2. Check if the resume file exists
    if not os.path.exists("MY_RESUME_FILE_NAME.pdf"):
        flash("no resume found", "danger")
        return redirect('/')


    # --- YOUR EXACT CODE START ---
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
    # --- YOUR EXACT CODE END ---

    flash("All emails have been sent successfully!", "success")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)