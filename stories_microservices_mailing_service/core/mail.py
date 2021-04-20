import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .config import EmailConfig


class SendMail(EmailConfig):

    def __init__(self, subject, body, to=None, subtype='html'):
        self.subject = subject
        self.body = body
        self.recipients = to or []
        self.subtype = subtype
        self.send_mail_recipient()

    def send_mail_recipient(self):
        for recipient in self.recipients:
            self.send_mail(recipient)

    def get_mail_message(self, recipient):
        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = self.EMAIL_HOST_USER
        message["To"] = recipient
        part = MIMEText(self.body, self.subtype)
        message.attach(part)
        return message

    def send_mail(self, recipient):
        message = self.get_mail_message(recipient)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.EMAIL_HOST, 465, context=context) as server:
            server.login(self.EMAIL_HOST_USER, self.EMAIL_HOST_PASSWORD)
            server.sendmail(
                self.EMAIL_HOST_USER, recipient, message.as_string()
            )
