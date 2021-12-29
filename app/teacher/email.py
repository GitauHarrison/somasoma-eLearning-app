from flask import render_template, current_app
from app.email import send_email


def send_live_flask_chapter_1_comment_email(comment):
    token = comment.get_reset_password_token()
    send_email('[somasoma eLearning] Your Flask Chapter 1 Comment is Live!',
               sender=current_app.config['commentS'][0],
               recipients=[comment.student_email],
               text_body=render_template(
                   'teacher/email/flask_chapter_1_comment_email.txt',
                   comment=comment,
                   token=token
                   ),
               html_body=render_template(
                   'teacher/email/flask_chapter_1_comment_email.html',
                   comment=comment,
                   token=token
                   )
               )
