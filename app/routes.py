from app import app
from flask import render_template
from app.forms import StudentRegistrationForm, ParentRegistrationForm,\
    TeacherRegistrationForm, LoginForm, RquestPasswordResetForm,\
    ResetPasswordForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# --------------------
# User Authentication
# --------------------


@app.route('/register/student/', methods=['GET', 'POST'])
def student_registration():
    form = StudentRegistrationForm()
    return render_template('student_registration.html',
                           form=form,
                           title='Register'
                           )


@app.route('/register/parent/', methods=['GET', 'POST'])
def parent_registration():
    form = ParentRegistrationForm()
    return render_template('parent_registration.html',
                           form=form,
                           title='Register'
                           )


@app.route('/register/teacher/', methods=['GET', 'POST'])
def teacher_registration():
    form = TeacherRegistrationForm()
    return render_template('teacher_registration.html',
                           form=form,
                           title='Register'
                           )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
                           form=form,
                           title='Login'
                           )


@app.route('/request-password-reset', methods=['GET', 'POST'])
def request_password_reset():
    form = RquestPasswordResetForm()
    return render_template('request_password_reset.html',
                           form=form,
                           title='Request Password Reset'
                           )


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    return render_template('reset_password.html',
                           form=form,
                           title='Reset Password'
                           )

# --------------------------
# End of User Authentication
# --------------------------
