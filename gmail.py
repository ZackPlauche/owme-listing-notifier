import os
import smtplib
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(override=True)

EMAIL = os.getenv('GMAIL_EMAIL')
PASSWORD = os.getenv('GMAIL_APP_PASSWORD')


@dataclass
class Email:
    to: str
    subject: str
    body: str

    def __str__(self):
        return f'To: {self.to}\nSubject: {self.subject}\n\n{self.body}'


def send_email(to: str, subject: str, body: str):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        connection.login(
            user=EMAIL,
            password=PASSWORD,
        )
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=to,
            msg=str(Email(to=to, subject=subject, body=body)).encode('utf-8'),
        )
