from flask import render_template, current_app
from app.email import send_email


def send_registration_details_student(student):
    token = student.get_reset_password_token()
    send_email('[somasoma eLearning] Your Registration Details',
               sender=current_app.config['ADMINS'][0],
               recipients=[student.student_email],
               text_body=render_template(
                   'admin/email/student_registration_email.txt',
                   student=student,
                   token=token
                   ),
               html_body=render_template(
                   'admin/email/student_registration_email.html',
                   student=student,
                   token=token
                   )
               )


def send_registration_details_parent(parent):
    token = parent.get_reset_password_token()
    send_email('[somasoma eLearning] Your Registration Details',
               sender=current_app.config['ADMINS'][0],
               recipients=[parent.student_email],
               text_body=render_template(
                   'admin/email/parent_registration_email.txt',
                   parent=parent,
                   token=token
                   ),
               html_body=render_template(
                   'admin/email/parent_registration_email.html',
                   parent=parent,
                   token=token
                   )
               )
