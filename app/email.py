from flask_mail import Message
from flask import current_app, render_template
from threading import Thread

from app import mail, app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_reset_password_email(user, token):
    msg = Message(
        "[ToDo] request to reset your password",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email],
        html=render_template(
            'reset_password_email.html', user=user, token=token))
    Thread(target=send_async_email, args=(app, msg)).start()
