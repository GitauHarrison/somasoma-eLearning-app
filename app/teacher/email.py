from flask import render_template, current_app
from app.email import send_email


def send_live_flask_chapter_1_comment_email(student):
    token = student.get_reset_password_token()
    send_email('[somasoma eLearning] Your Flask Chapter 1 comment is Live!',
               sender=current_app.config['ADMINS'][0],
               recipients=[student.student_email],
               text_body=render_template(
                   'student/email/flask_chapter_1_comment_email.txt',
                   student=student,
                   token=token
                   ),
               html_body=render_template(
                   'student/email/flask_chapter_1_comment_email.html',
                   student=student,
                   token=token
                   )
               )
