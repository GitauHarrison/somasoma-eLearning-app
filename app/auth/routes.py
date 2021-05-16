from flask import render_template, url_for, flash, request, redirect,\
    session
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from flask_login import current_user, login_user, logout_user,\
    login_required
from app.auth.forms import ClientRegistrationForm, LoginForm,\
    RequestPasswordResetForm, ResetPasswordForm, Enable2faForm,\
    Confirm2faForm, Disable2faForm, TeacherRegistrationForm
from app.auth.email import client_send_password_reset_email,\
    client_registration_email, payment_email,\
    teacher_send_password_reset_email, teacher_registration_email
from app.auth.twilio_verify_api import request_verification_token,\
    check_verification_token
from app.models import Client, Teacher


@bp.route('/login')
def login():
    return render_template('auth/all_users_login.html',
                           title='Login'
                           )


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# ---------------------
# Client Authentication
# ---------------------


@bp.route('/register/client', methods=['GET', 'POST'])
def client_registration():
    form = ClientRegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        client = Client(parent_full_name=form.parent_full_name.data,
                        parent_email=form.parent_email.data, 
                        verification_phone=form.verification_phone.data,
                        student_full_name=form.student_full_name.data,
                        student_email=form.student_email.data,
                        student_username=form.student_username.data,
                        student_course=form.student_course.data
                        )
        client.set_password(form.password.data)
        db.session.add(client)
        db.session.commit()
        flash("Check your email for instructions on next steps")
        if client:
            payment_email(client),
            client_registration_email(client)
        return redirect(url_for('main.home'))
    return render_template('auth/client_registration.html',
                           form=form,
                           title='Register'
                           )


@bp.route('/login/client', methods=['GET', 'POST'])
def client_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        client = Client.query.filter_by(student_username=form.username.data).first()
        if client is None or not client.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.client_login'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.client_paid_courses',
                                username=client.student_username)
        if client.two_factor_enabled():
            request_verification_token(client.verification_phone)
            session['username'] = client.student_username
            session['phone'] = client.verification_phone
            return redirect(url_for('auth.client_verify_2fa',
                                    username=client.student_username,
                                    next=next_page,
                                    remember='1' if form.remember_me.data else '0'
                                    ))
        login_user(client, remember=form.remember_me.data)
        return redirect(next_page)
    return render_template('auth/client_login.html',
                           form=form,
                           title='Client Login'
                           )


# Password reset

@bp.route('/login/client/request-password-reset', methods=['GET', 'POST'])
def client_request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        client = Client.query.filter_by(email=form.student_email.data).first()
        if client:
            client_send_password_reset_email(client)
        flash('Check your email for instructions to reset your password')
        return redirect(url_for('auth.client_login'))
    return render_template('auth/request_password_reset.html',
                           form=form,
                           title='Request Password Reset'
                           )


@bp.route('/login/client/reset-password/<token>', methods=['GET', 'POST'])
def client_reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    client = Client.verify_reset_password_token(token)
    if not client:
        return redirect(url_for('auth.client_login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        client.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset. Login to continue')
        return redirect(url_for('auth.client_login'))
    return render_template('auth/reset_password.html',
                           form=form,
                           title='Reset Password'
                           )


# End of password reset


# Client Two-factor authentication

@bp.route('/client/<username>/enable-2fa', methods=['GET', 'POST'])
@login_required
def client_enable_2fa(username):
    client = Client.query.filter_by(student_username=username).first_or_404()
    form = Enable2faForm()
    if form.validate_on_submit():
        session['phone'] = form.verification_phone.data
        request_verification_token(session['phone'])
        return redirect(url_for('auth.client_verify_2fa',
                                username=client.student_username))
    return render_template('auth/enable_2fa.html',
                           form=form,
                           title='Enable 2FA'
                           )


@bp.route('/client/<username>/confirm-2fa', methods=['GET', 'POST'])
def client_verify_2fa(username):
    client = Client.query.filter_by(student_username=username).first_or_404()
    form = Confirm2faForm()
    if form.validate_on_submit():
        phone = session['phone']
        if check_verification_token(phone, form.token.data):
            del session['phone']
            login_user(client)
            if client.is_authenticated:
                client.verification_phone = phone
                db.session.commit()
                flash('You have enabled two-factor authentication')
                return redirect(url_for('main.client_profile',
                                        username=client.student_username))
            else:
                username = session['username']
                del session['username']
                client = Client.query.filter_by(student_username=username).first()
                next_page = request.args.get('next')
                remember = request.args.get('remember', '0') == '1'
                login_user(client, remember=remember)
                return redirect(url_for(next_page))
        form.token.errors.append('Invalid token')
    return render_template('auth/verify_2fa.html',
                           form=form,
                           title='Verify Token'
                           )


@bp.route('/client/<username>/disable-2fa', methods=['GET', 'POST'])
def client_disable_2fa(username):
    client = Client.query.filter_by(student_username=username).first_or_404()
    form = Disable2faForm()
    if form.validate_on_submit():
        client.verification_phone = None
        db.session.commit()
        flash('You have disabled two-factor authentication')
        return redirect(url_for('main.client_profile',
                                username=client.student_username))
    return render_template('auth/disable_2fa.html',
                           form=form,
                           title='Disable 2FA'
                           )

# End of two-factor authentication

# ----------------------------
# End of Client Authentication
# ----------------------------


# ----------------------
# Teacher Authentication
# ----------------------

@bp.route('/register/teacher', methods=['GET', 'POST'])
def teacher_registration():
    form = TeacherRegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        teacher = Teacher(teacher_full_name=form.teacher_full_name.data,
                          teacher_email=form.teacher_email.data,
                          verification_phone=form.verification_phone.data,
                          teacher_username=form.teacher_username.data,
                          )
        teacher.set_password(form.password.data)
        db.session.add(teacher)
        db.session.commit()
        flash("Check your email for instructions on next steps")
        if teacher:
            teacher_registration_email(teacher)
        return redirect(url_for('main.home'))
    return render_template('auth/teacher_registration.html',
                           form=form,
                           title='Register'
                           )


@bp.route('/login/teacher', methods=['GET', 'POST'])
def teacher_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(teacher_username=form.username.data).first()
        if teacher is None or not teacher.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.teacher_login'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.teacher_profile',
                                username=teacher.teacher_username)
        if teacher.two_factor_enabled():
            request_verification_token(teacher.verification_phone)
            session['username'] = teacher.teacher_username
            session['phone'] = teacher.verification_phone
            return redirect(url_for('auth.teacher_verify_2fa',
                                    username=teacher.teacher_username,
                                    next=next_page,
                                    remember='1' if form.remember_me.data else '0'
                                    ))
        login_user(teacher, remember=form.remember_me.data)
        return redirect(next_page)
    return render_template('auth/teacher_login.html',
                           form=form,
                           title='Teacher Login'
                           )


# Password reset

@bp.route('/login/teacher/request-password-reset', methods=['GET', 'POST'])
def teacher_request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(email=form.teacher_email.data).first()
        if teacher:
            teacher_send_password_reset_email(teacher)
        flash('Check your email for instructions to reset your password')
        return redirect(url_for('auth.teacher_login'))
    return render_template('auth/request_password_reset.html',
                           form=form,
                           title='Request Password Reset'
                           )


@bp.route('/login/teacher/reset-password/<token>', methods=['GET', 'POST'])
def teacher_reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    teacher = Teacher.verify_reset_password_token(token)
    if not teacher:
        return redirect(url_for('auth.teacher_login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        teacher.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset. Login to continue')
        return redirect(url_for('auth.teacher_login'))
    return render_template('auth/reset_password.html',
                           form=form,
                           title='Reset Password'
                           )


# End of password reset


# Teacher Two-factor authentication

@bp.route('/teacher/<username>/enable-2fa', methods=['GET', 'POST'])
@login_required
def teacher_enable_2fa(username):
    teacher = Teacher.query.filter_by(teacher_username=username).first_or_404()
    form = Enable2faForm()
    if form.validate_on_submit():
        session['phone'] = form.verification_phone.data
        request_verification_token(session['phone'])
        return redirect(url_for('auth.teacher_verify_2fa',
                                username=teacher.teacher_username))
    return render_template('auth/enable_2fa.html',
                           form=form,
                           title='Enable 2FA'
                           )


@bp.route('/teacher/<username>/confirm-2fa', methods=['GET', 'POST'])
def teacher_verify_2fa(username):
    teacher = Teacher.query.filter_by(teacher_username=username).first_or_404()
    form = Confirm2faForm()
    if form.validate_on_submit():
        phone = session['phone']
        if check_verification_token(phone, form.token.data):
            del session['phone']
            login_user(teacher)
            if teacher.is_authenticated:
                teacher.verification_phone = phone
                db.session.commit()
                flash('You have enabled two-factor authentication')
                return redirect(url_for('main.teacher_profile',
                                        username=teacher.teacher_username))
            else:
                username = session['username']
                del session['username']
                teacher = Teacher.query.filter_by(teacher_username=username).first()
                next_page = request.args.get('next')
                remember = request.args.get('remember', '0') == '1'
                login_user(teacher, remember=remember)
                return redirect(url_for(next_page))
        form.token.errors.append('Invalid token')
    return render_template('auth/verify_2fa.html',
                           form=form,
                           title='Verify Token'
                           )


@bp.route('/teacher/<username>/disable-2fa', methods=['GET', 'POST'])
def teacher_disable_2fa(username):
    teacher = Teacher.query.filter_by(teacher_username=username).first_or_404()
    form = Disable2faForm()
    if form.validate_on_submit():
        teacher.verification_phone = None
        db.session.commit()
        flash('You have disabled two-factor authentication')
        return redirect(url_for('main.teacher_profile',
                                username=teacher.teacher_username))
    return render_template('auth/disable_2fa.html',
                           form=form,
                           title='Disable 2FA'
                           )

# End of two-factor authentication

# -----------------------------
# End of Teacher Authentication
# -----------------------------
