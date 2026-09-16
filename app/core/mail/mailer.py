import smtplib
from email.message import EmailMessage
from decouple import config


def send_magic_link(to_email:str,link:str):
    msg = EmailMessage()
    msg['Subject'] = 'Confirm login'
    msg['From'] = config('SMTP_FROM')
    msg['To'] = to_email

    msg.set_content(f"Follow the link {link}\nIt's valid for 15 minutes")

    with smtplib.SMTP(host=config("SMTP_HOST"),port=config("SMTP_PORT",cast=int)) as server:
        server.starttls()

        server.login(user=config("SMTP_USER"),password=config("SMTP_PASSWORD"))
        server.send_message(msg=msg)