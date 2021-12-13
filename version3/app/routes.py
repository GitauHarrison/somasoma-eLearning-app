from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, ClientRegistrationForm,\
    RequestPasswordResetForm, ResetPasswordForm, CommentForm
from app.models import Client
from flask_login import current_user, login_user, logout_user, login_required    


# ========================================
# MAIN ROUTES
# ========================================

@app.route('/student/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_student():
    comment_form = CommentForm()
    return render_template(
                           'dashboard_student.html',
                           comment_form=comment_form
                           )


@app.route('/parent/dashboard')
@login_required
def dashboard_parent():
    return render_template('dashboard_parent.html')


@app.route('/teacher/dashboard')
@login_required
def dashboard_teacher():
    return render_template('dashboard_teacher.html')


@app.route('/login')
def login():
    return render_template('login_users.html',
                           title='Login'
                           )


# ========================================
# END OF MAIN ROUTES
# ========================================

# ========================================
# AUTHENTICATION ROUTES
# ========================================

@app.route('/parent/login', methods=['GET', 'POST'])
def login_parent():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        parent = Client.query.filter_by(parent_email=form.email.data).first()
        if parent is None or not parent.check_parent_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login_parent'))
        login_user(parent, remember=form.remember_me.data)
        return redirect(url_for('dashboard_parent'))
    return render_template('login.html',
                           title='Parent Login',
                           form=form
                           )


@app.route('/student/login', methods=['GET', 'POST'])
def login_student():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Client.query.filter_by(student_email=form.email.data).first()
        if student is None or not student.check_student_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login_student'))
        login_user(student, remember=form.remember_me.data)
        return redirect(url_for('dashboard_student'))
    return render_template('login.html',
                           title='Student Login',
                           form=form
                           )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/parent-registration', methods=['GET', 'POST'])
def register_client():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ClientRegistrationForm()
    if form.validate_on_submit():
        client = Client(parent_full_name=form.parent_full_name.data,
                        parent_email=form.parent_email.data,
                        parent_phone=form.parent_phone.data,
                        parent_occupation=form.parent_occupation.data,
                        parent_residence=form.parent_residence.data,
                        student_full_name=form.student_full_name.data,
                        student_email=form.student_email.data,
                        student_phone=form.student_phone.data,
                        student_school=form.student_school.data,
                        student_age=form.student_age.data
                        )
        client.set_parent_password(form.parent_password.data)
        client.set_student_password(form.student_password.data)
        db.session.add(client)
        db.session.commit()
        flash('Parent and Student successfully registered. Login to continue!')
        return redirect(url_for('login'))
    return render_template('register_client.html',
                           title='Client Registration',
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

# ========================================
# END OF AUTHENTICATION ROUTES
# ========================================
