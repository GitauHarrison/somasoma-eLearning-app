from app import app, db
from flask import render_template, redirect, url_for, flash, session,\
    request
from app.forms import LoginForm, ClientRegistrationForm,\
    RequestPasswordResetForm, ResetPasswordForm, CommentForm,\
    Enable2faForm, Disable2faForm, Confirm2faForm
from app.models import Client
from app.twilio_verify_api import check_verification_token,\
    request_verification_token
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


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
        return redirect(url_for('dashboard_parent'))
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
        return redirect(url_for('dashboard_student'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Client.query.filter_by(student_email=form.email.data).first()
        if student is None or not student.check_student_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login_student'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard_student')
        if student.two_factor_student_enabled():
            request_verification_token(student.student_phone)
            session['student_email'] = student.student_email
            session['phone'] = student.student_phone
            return redirect(url_for('verify_2fa_student',
                                    next=next_page,
                                    remember='1' if form.remember_me.data else '0'
                                    )
                            )
        login_user(student, remember=form.remember_me.data)
        return redirect(next_page)
    return render_template('login.html',
                           title='Student Login',
                           form=form
                           )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/client/register', methods=['GET', 'POST'])
def register_client():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
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

# Two-factor authentication


@app.route('/student/enable-2fa', methods=['GET', 'POST'])
@login_required
def enable_2fa_student():
    form = Enable2faForm()
    if form.validate_on_submit():
        session['phone'] = form.verification_phone.data
        request_verification_token(session['phone'])
        return redirect(url_for('verify_2fa_student'))
    return render_template('enable_2fa.html',
                           form=form,
                           title='Enable 2fa'
                           )


@app.route('/student/verify-2fa', methods=['GET', 'POST'])
def verify_2fa_student():
    form = Confirm2faForm()
    if form.validate_on_submit():
        phone = session['phone']
        if check_verification_token(phone, form.token.data):
            del session['phone']
            if current_user.is_authenticated:
                current_user.student_phone = phone
                db.session.commit()
                flash('You have enabled two-factor authentication')
                return redirect(url_for('dashboard_student', _anchor='account'))
            else:
                student_email = session['student_email']
                del session['student_email']
                student = Client.query.filter_by(student_email=student_email).first()
                next_page = request.args.get('next')
                remember = request.args.get('remember', '0') == '1'
                login_user(student, remember=remember)
                return redirect(next_page)
        form.token.errors.append('Invalid token')
    return render_template('verify_2fa.html',
                           form=form,
                           title='Verify Token'
                           )


@app.route('/student/disable-2fa', methods=['GET', 'POST'])
@login_required
def disable_2fa_student():
    form = Disable2faForm()
    if form.validate_on_submit():
        current_user.student_phone = None
        db.session.commit()
        flash('You have disabled two-factor authentication')
        return redirect(url_for('dashboard_student', _anchor='account'))
    return render_template('disable_2fa.html',
                           form=form,
                           title='Disable 2fa'
                           )

# ========================================
# END OF AUTHENTICATION ROUTES
# ========================================
