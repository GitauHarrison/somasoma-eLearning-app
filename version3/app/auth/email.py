from flask import render_template, current_app
from app.email import send_email


def send_password_reset_email_student(student):
    token = student.get_reset_password_token()
    send_email('[somasoma eLearning] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[student.student_email],
               text_body=render_template(
                   'auth/email/reset_password_student.txt',
                   student=student,
                   token=token
                   ),
               html_body=render_template(
                   'auth/email/reset_password_student.html',
                   student=student,
                   token=token
                   )
               )


def send_password_reset_email_admin(admin):
    token = admin.get_reset_password_token()
    send_email('[somasoma eLearning] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[admin.admin_email],
               text_body=render_template(
                   'auth/email/reset_password_admin.txt',
                   admin=admin,
                   token=token
                   ),
               html_body=render_template(
                   'auth/email/reset_password_admin.html',
                   admin=admin,
                   token=token
                   )
               )