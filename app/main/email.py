from flask import render_template, current_app
from app.email import send_email


def send_flask_stories_email(admin):
    token = admin.get_reset_password_token()
    send_email('[somasoma eLearning] New Flask Story',
               sender=current_app.config['ADMINS'][0],
               recipients=[admin.admin_email],
               text_body=render_template(
                   'main/email/flask_course/review_story.txt',
                   admin=admin,
                   token=token),
               html_body=render_template(
                   'main/email/flask_course/review_story.html',
                   admin=admin,
                   token=token))
