from flask import render_template, current_app
from app.email import send_email


def send_flask_chapter_1_comment_email(teacher):
    token = teacher.get_reset_password_token()
    send_email('[somasoma eLearning] Flask: Chapter 1 Comment',
               sender=current_app.config['ADMINS'][0],
               recipients=[teacher.teacher_email],
               text_body=render_template(
                   'teacher/email/flask_chapter_1_comment.txt',
                   teacher=teacher,
                   token=token
                   ),
               html_body=render_template(
                   'teacher/email/flask_chapter_1_comment.html',
                   teacher=teacher,
                   token=token
                   )
               )
