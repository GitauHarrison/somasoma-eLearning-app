from flask_mail import Message
from app import mail, app
from flask import render_template
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def parent_send_password_reset_email(parent):
    token = parent.get_reset_password_token()
    send_email('[somasoma eLearning] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[parent.email],
               text_body=render_template('email/reset_password/parent_reset_password.txt',
                                         parent=parent,
                                         token=token
                                         ),
               html_body=render_template('email/reset_password/parent_reset_password.html',
                                         parent=parent,
                                         token=token
                                         )
               )


def student_send_password_reset_email(student):
    token = student.get_reset_password_token()
    send_email('[somasoma eLearning] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[student.email],
               text_body=render_template('email/reset_password/student_reset_password.txt',
                                         student=student,
                                         token=token
                                         ),
               html_body=render_template('email/reset_password/student_reset_password.html',
                                         student=student,
                                         token=token
                                         )
               )


def teacher_send_password_reset_email(teacher):
    token = teacher.get_reset_password_token()
    send_email('[somasoma eLearning] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[teacher.email],
               text_body=render_template('email/reset_password/teacher_reset_password.txt',
                                         teacher=teacher,
                                         token=token
                                         ),
               html_body=render_template('email/reset_password/teacher_reset_password.html',
                                         teacher=teacher,
                                         token=token
                                         )
               )
