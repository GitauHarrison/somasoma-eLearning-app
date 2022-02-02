from flask import render_template, current_app
from app.email import send_email


def send_flask_chapter_1_comment_email(teacher):
    token = teacher.get_reset_password_token()
    send_email('[somasoma eLearning] Chapter 1 (Hello World) Comment',
               sender=current_app.config['ADMINS'][0],
               recipients=[teacher.teacher_email],
               text_body=render_template(
                   'teacher/email/chapter_1/new_comment_email.txt',
                   teacher=teacher,
                   token=token
                   ),
               html_body=render_template(
                   'teacher/email/chapter_1/new_comment_email.html',
                   teacher=teacher,
                   token=token
                   )
               )


def send_flask_chapter_2_comment_email(teacher):
    token = teacher.get_reset_password_token()
    send_email('[somasoma eLearning] Chapter 2 (Flask Templates) Comment',
               sender=current_app.config['ADMINS'][0],
               recipients=[teacher.teacher_email],
               text_body=render_template(
                   'teacher/email/chapter_2/new_comment_email.txt',
                   teacher=teacher,
                   token=token
                   ),
               html_body=render_template(
                   'teacher/email/chapter_2/new_comment_email.html',
                   teacher=teacher,
                   token=token
                   )
               )
