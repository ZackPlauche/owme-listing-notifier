import smtplib
import os
from dotenv import load_dotenv

load_dotenv(override=True)

EMAIL = os.getenv('GMAIL_EMAIL')
PASSWORD = os.getenv('GMAIL_APP_PASSWORD')


def send_email(to: str, subject: str, body: str):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        connection.login(
            user=EMAIL,
            password=PASSWORD,
        )
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=to,
            msg=f'Subject:{subject}\n\n{body}'.encode(),
        )
