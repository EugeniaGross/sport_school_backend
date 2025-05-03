from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from settings import settings


async def send_email(name, phone, message, email):
    msg = MIMEMultipart()
    message = f"{message}\n\n{name}. Электронная почта: {email}. "
    if phone:
        message += f"Телефон: {phone}. "
    password = settings.EMAIL_HOST_PASSWORD
    msg["From"] = settings.EMAIL_HOST_USER
    msg["To"] = settings.ADMIN_EMAIL
    msg["Subject"] = "Обратная связь"
    msg.attach(MIMEText(message, "plain"))
    server = smtplib.SMTP(f"{settings.EMAIL_HOST}: {settings.EMAIL_PORT}")
    server.starttls()
    server.login(msg["From"], password)
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()
