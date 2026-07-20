from flask_mail import Message

from extensions import mail


def send_email(subject, recipient, email_body):
    msg = Message(subject=subject, recipients=[recipient], body=email_body)
    mail.send(msg)
