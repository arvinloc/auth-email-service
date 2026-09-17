import smtplib
from email.message import EmailMessage
from decouple import config


def send_magic_link(to_email: str, link: str):
    # Настройка SMTP сервера, можно в дальнейшем раскуртить до более совершенной технологии
    msg = EmailMessage()
    msg['Subject'] = 'Подтвердить вход'
    msg['From'] = config('SMTP_FROM')
    msg['To'] = to_email

    msg.set_content(
        f"Перейдите по ссылке. {link}\nОна действительна в течение 15 минут.")

    with smtplib.SMTP(host=config("SMTP_HOST"), port=config("SMTP_PORT", cast=int)) as server:
        server.starttls()

        server.login(user=config("SMTP_USER"),
                     password=config("SMTP_PASSWORD"))
        server.send_message(msg=msg)
