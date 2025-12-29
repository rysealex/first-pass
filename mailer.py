import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_job_link(job_link, company_name, role_title):
    sender_email = os.getenv("GMAIL_USER")
    receiver_email = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_APP_PASSWORD")

    if not sender_email or not password:
        print("Error: Gmail credentials not found in .env file.")
        return

    message = MIMEMultipart("alternative")
    message["Subject"] = f"🚀 Apply: {company_name} - {role_title}"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"New Job Found!\nCompany: {company_name}\nRole: {role_title}\nLink: {job_link}"
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #2d3748;">New Job Opportunity Found</h2>
        <p><strong>Company:</strong> {company_name}</p>
        <p><strong>Role:</strong> {role_title}</p>
        <div style="margin-top: 20px;">
            <a href="{job_link}" 
               style="background-color: #48bb78; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">
               Open Application
            </a>
        </div>
        <p style="margin-top: 30px; font-size: 0.8em; color: #718096;">Sent from your Raspberry Pi 5.</p>
      </body>
    </html>
    """

    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"✅ Email sent successfully for {company_name}!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")