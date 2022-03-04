from flask import render_template, current_app
from app.email import send_email


def send_registration_details_teacher(teacher):
    token = teacher.get_reset_password_token()
    send_email('[somasoma eLearning] Your Teacher Registration Details',
               sender=current_app.config['ADMINS'][0],
               recipients=[teacher.teacher_email],
               text_body=render_template(
                   'admin/email/teacher_registration_email.txt',
                   teacher=teacher,
                   token=token),
               html_body=render_template(
                   'admin/email/teacher_registration_email.html',
                   teacher=teacher,
                   token=token))


def send_flask_stories_email(student):
    token = student.get_reset_password_token()
    send_email('[somasoma eLearning] Your Flask Story is Live!',
               sender=current_app.config['ADMINS'][0],
               recipients=[student.email],
               text_body=render_template(
                   'admin/email/flask_story_email.txt',
                   student=student,
                   token=token),
               html_body=render_template(
                   'admin/email/flask_story_email.html',
                   student=student,
                   token=token))
