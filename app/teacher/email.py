from flask import render_template, current_app
from app.email import send_email


def send_live_flask_chapter_1_comment_email(student):
    token = student.get_reset_password_token()
    send_email('[somasoma eLearning] Your chapter 1 (Hello World) comment is Live!',
               sender=current_app.config['ADMINS'][0],
               recipients=[student.student_email],
               text_body=render_template(
                   'student/email/chapter_1/live_comment_email.txt',
                   student=student,
                   token=token
                   ),
               html_body=render_template(
                   'student/email/chapter_1/live_comment_email.html',
                   student=student,
                   token=token
                   )
               )


def send_live_flask_chapter_2_comment_email(student):
    token = student.get_reset_password_token()
    send_email('[somasoma eLearning] Your Chapter 2 (Flask Templates) comment is Live!',
               sender=current_app.config['ADMINS'][0],
               recipients=[student.student_email],
               text_body=render_template(
                   'student/email/chapter_2/live_comment_email.txt',
                   student=student,
                   token=token
                   ),
               html_body=render_template(
                   'student/email/chapter_2/live_comment_email.html',
                   student=student,
                   token=token
                   )
               )


def send_live_flask_chapter_3_comment_email(student):
    token = student.get_reset_password_token()
    send_email(
        '[somasoma eLearning] Your Chapter 3 (Introduction to Web Forms) comment is Live!',
        sender=current_app.config['ADMINS'][0],
        recipients=[student.student_email],
        text_body=render_template(
            'student/email/chapter_2/live_comment_email.txt',
            student=student,
            token=token),
        html_body=render_template(
            'student/email/chapter_2/live_comment_email.html',
            student=student,
            token=token)
    )
