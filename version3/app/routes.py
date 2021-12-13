from app import app
from flask import render_template
from app.forms import LoginForm, ParentRegistrationForm,\
    StudentRegistrationForm, RequestPasswordResetForm,\
    ResetPasswordForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
                           title='Log In',
                           form=form
                           )


@app.route('/parent-registration', methods=['GET', 'POST'])
def register_parent():
    form = ParentRegistrationForm()
    return render_template('register_parent.html',
                           title='Parent Registration',
                           form=form
                           )


@app.route('/student-registration', methods=['GET', 'POST'])
def student_parent():
    form = StudentRegistrationForm()
    return render_template('register_student.html',
                           title='Student Registration',
                           form=form
                           )


@app.route('/request-password-reset', methods=['GET', 'POST'])
def request_password_reset():
    form = RequestPasswordResetForm()
    return render_template('request_password_reset.html',
                           title='Request Password Reset',
                           form=form
                           )


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    return render_template('reset_password.html',
                           title='Reset Password',
                           form=form
                           )
