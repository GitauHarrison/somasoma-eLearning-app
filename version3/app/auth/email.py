from flask import render_template, current_app
from app.email import send_email

# ================================
# PASSWORD RESET
# ================================


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

# ================================
# END OF PASSWORD RESET
# ================================


# ================================
# REGISSTRATION EMAIL
# ================================


def send_registration_details_student(student):
    token = student.get_reset_password_token()
    send_email('[somasoma eLearning] Student Registration Details',
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
    send_email('[somasoma eLearning] Parent Registration Details',
               sender=current_app.config['ADMINS'][0],
               recipients=[parent.parent_email],
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

# ================================
# END OF REGISTRATION EMAIL
# ================================
