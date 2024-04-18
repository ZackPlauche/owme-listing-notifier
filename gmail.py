import os
import smtplib
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(override=True)

EMAIL = os.getenv('GMAIL_EMAIL')
PASSWORD = os.getenv('GMAIL_APP_PASSWORD')


@dataclass
class Email:
    from_: str
    to: str
    subject: str
    body: str

    def __str__(self):
        return f'From: {self.from_}\nTo: {self.to}\nSubject: {self.subject}\n\n{self.body}'


def send_email(to: str | list[str], subject: str, body: str):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        connection.login(
            user=EMAIL,
            password=PASSWORD,
        )
        for email_address in to if isinstance(to, list) else [to]:
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=email_address,
                msg=str(Email(from_=f'Zack Plauché <{EMAIL}>', to=email_address, subject=subject, body=body)).encode('utf-8'),
            )
