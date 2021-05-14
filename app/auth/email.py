from flask import render_template, current_app
from app.email import send_email


# Reset email

def client_send_password_reset_email(client):
    token = client.get_reset_password_token()
    send_email('[somasoma eLearning] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[client.email],
               text_body=render_template('auth/email/client_reset_password.txt',
                                         client=client,
                                         token=token
                                         ),
               html_body=render_template('auth/email/client_reset_password.html',
                                         client=client,
                                         token=token
                                         )
               )


# Registration details


def client_registration_email(client):
    send_email('[somasoma eLearning] Registration Details',
               sender=current_app.config['ADMINS'][0],
               recipients=[client.parent_email],
               text_body=render_template('auth/email/client_registration_email.txt',
                                         client=client),
               html_body=render_template('auth/email/client_registration_email.html',
                                         client=client))


# Payment email


def payment_email(client):
    send_email('[somasoma eLearning] Enrol Your Child',
               sender=current_app.config['ADMINS'][0],
               recipients=[client.parent_email],
               text_body=render_template('auth/email/enrolment_email.txt',
                                         client=client),
               html_body=render_template('auth/email/enrolment_email.html',
                                         client=client))
