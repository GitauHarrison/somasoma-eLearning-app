from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, ParentRegistrationForm,\
    StudentRegistrationForm, RequestPasswordResetForm,\
    ResetPasswordForm
from app.models import Client
from flask_login import current_user, login_user, logout_user, login_required    


@app.route('/')
@app.route('/student-dashboard')
@login_required
def student_dashboard():
    return render_template('student_dashboard.html')


@app.route('/parent-dashboard')
@login_required
def parent_dashboard():
    return render_template('parent_dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        parent = Client.query.filter_by(parent_email=form.email.data).first()
        student = Client.query.filter_by(student_email=form.email.data).first()
        if parent is None or not parent.check_parent_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        elif student is None or not student.check_student_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        if parent:
            login_user(parent, remember=form.remember_me.data)
            return redirect(url_for('parent_dashboard'))
        if student:
            login_user(student, remember=form.remember_me.data)
            return redirect(url_for('student_dashboard'))
    return render_template('login.html',
                           title='Log In',
                           form=form
                           )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/parent-registration', methods=['GET', 'POST'])
def register_parent():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ParentRegistrationForm()
    if form.validate_on_submit():
        parent = Client(parent_full_name=form.parent_full_name.data,
                        parent_email=form.parent_email.data,
                        parent_phone=form.parent_phone.data,
                        parent_occupation=form.parent_occupation.data,
                        parent_residence=form.parent_residence.data,
                        )
        parent.set_parent_password(form.parent_password.data)
        db.session.add(parent)
        db.session.commit()
        flash('Parent successfully registered!')
        return redirect(url_for('register_student'))
    return render_template('register_parent.html',
                           title='Parent Registration',
                           form=form
                           )


@app.route('/student-registration', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        student = Client(student_full_name=form.student_full_name.data,
                         student_email=form.student_email.data,
                         student_phone=form.student_phone.data,
                         student_school=form.student_school.data,
                         student_age=form.student_age.data
                         )
        student.set_student_password(form.student_password.data)
        db.session.add(student)
        db.session.commit()
        flash('Student successfully registered!')
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
