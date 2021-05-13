from flask import render_template, url_for, flash, request, redirect,\
    session
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from flask_login import current_user, login_user, logout_user,\
    login_required
from app.auth.forms import ParentRegistrationForm, StudentRegistrationForm,\
    TeacherRegistrationForm, LoginForm, RquestPasswordResetForm,\
    ResetPasswordForm, Enable2faForm, Confirm2faForm, Disable2faForm
from app.auth.email import parent_send_password_reset_email,\
    student_send_password_reset_email, teacher_send_password_reset_email,\
    parent_registration_email, student_registration_email,\
    teacher_registration_email, payment_email
from app.auth.twilio_verify_api import request_verification_token,\
    check_verification_token
from app.models import Parent, Student, Teacher


# --------------------
# User Authentication
# --------------------


@bp.route('/register/parent', methods=['GET', 'POST'])
def parent_registration():
    form = ParentRegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        parent = Parent(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        username=form.username.data,
                        email=form.email.data,
                        verification_phone=form.verification_phone.data
                        )
        parent.set_password(form.password.data)
        db.session.add(parent)
        db.session.commit()
        flash('Congratulations! Next, register your child.')
        if parent:
            payment_email(parent),
            parent_registration_email(parent)
        return redirect(url_for('auth.student_registration'))
    return render_template('parent_registration.html',
                           form=form,
                           title='Register'
                           )


@bp.route('/register/student', methods=['GET', 'POST'])
def student_registration():
    form = StudentRegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.student_paid_courses'))
    if form.validate_on_submit():
        student = Student(first_name=form.first_name.data,
                          last_name=form.last_name.data,
                          username=form.username.data,
                          email=form.email.data,
                          verification_phone=form.verification_phone.data
                          )
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash("Check parent\'s email for enrolment details")
        if student:
            student_registration_email(student)
        return redirect(url_for('main.home'))
    return render_template('student_registration.html',
                           form=form,
                           title='Register'
                           )


@bp.route('/register/teacher', methods=['GET', 'POST'])
def teacher_registration():
    form = TeacherRegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        teacher = Teacher(first_name=form.first_name.data,
                          last_name=form.last_name.data,
                          username=form.username.data,
                          email=form.email.data,
                          verification_phone=form.verification_phone.data
                          )
        teacher.set_password(form.password.data)
        db.session.add(teacher)
        db.session.commit()
        flash('Congratulations! You have successfully registered as a teacher')
        if teacher:
            teacher_registration_email(teacher)
        return redirect(url_for('auth.login'))
    return render_template('teacher_registration.html',
                           form=form,
                           title='Register'
                           )


@bp.route('/login')
def login():
    return render_template('all_users_login.html',
                           title='Login'
                           )


@bp.route('/login/parent', methods=['GET', 'POST'])
def parent_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        parent = Parent.query.filter_by(username=form.username.data).first()
        if parent is None or not parent.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.parent_login'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.parent_profile',
                                username=parent.username)
        if parent.two_factor_enabled():
            request_verification_token(parent.verification_phone)
            session['username'] = parent.username
            session['phone'] = parent.verification_phone
            return redirect(url_for('auth.parent_verify_2fa',
                                    username=parent.username,
                                    next=next_page,
                                    remember='1' if form.remember_me.data else '0'
                                    ))
        login_user(parent, remember=form.remember_me.data)
        return redirect(next_page)
    return render_template('parent_login.html',
                           form=form,
                           title='Parent Login'
                           )


@bp.route('/login/student', methods=['GET', 'POST'])
def student_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(username=form.username.data).first()
        if student is None or not student.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.student_login'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.student_paid_courses',
                                username=student.username)
        if student.two_factor_enabled():
            request_verification_token(student.verification_phone)
            session['username'] = student.username
            session['phone'] = student.verification_phone
            return redirect(url_for('auth.student_verify_2fa',
                                    username=student.username,
                                    next=next_page,
                                    remember='1' if form.remember_me.data else '0'
                                    ))
        login_user(student, remember=form.remember_me.data)
        return redirect(next_page)
    return render_template('student_login.html',
                           form=form,
                           title='Student Login'
                           )


@bp.route('/login/teacher', methods=['GET', 'POST'])
def teacher_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(username=form.username.data).first()
        if teacher is None or not teacher.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.teacher_login'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.teacher_profile',
                                username=teacher.username)
        if teacher.two_factor_enabled():
            request_verification_token(teacher.verification_phone)
            session['username'] = teacher.username
            session['phone'] = teacher.verification_phone
            return redirect(url_for('auth.teacher_verify_2fa',
                                    username=teacher.username,
                                    next=next_page,
                                    remember='1' if form.remember_me.data else '0'
                                    ))
        login_user(teacher, remember=form.remember_me.data)
        return redirect(next_page)
    return render_template('teacher_login.html',
                           form=form,
                           title='Teacher Login'
                           )


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# Password reset

@bp.route('/login/parent/request-password-reset', methods=['GET', 'POST'])
def parent_request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RquestPasswordResetForm()
    if form.validate_on_submit():
        parent = Parent.query.filter_by(email=form.email.data).first()
        if parent:
            parent_send_password_reset_email(parent)
        flash('Check your email for instructions to reset your password')
        return redirect(url_for('auth.parent_login'))
    return render_template('request_password_reset.html',
                           form=form,
                           title='Request Password Reset'
                           )


@bp.route('/login/parent/reset-password/<token>', methods=['GET', 'POST'])
def parent_reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    parent = Parent.verify_reset_password_token(token)
    if not parent:
        return redirect(url_for('auth.parent_login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        parent.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset. Login to continue')
        return redirect(url_for('pauth.arent_login'))
    return render_template('reset_password.html',
                           form=form,
                           title='Reset Password'
                           )


@bp.route('/login/student/request-password-reset', methods=['GET', 'POST'])
def student_request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RquestPasswordResetForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student:
            student_send_password_reset_email(student)
        flash('Check your email for instructions to reset your password')
        return redirect(url_for('auth.student_login'))
    return render_template('request_password_reset.html',
                           form=form,
                           title='Request Password Reset'
                           )


@bp.route('/login/student/reset-password/<token>', methods=['GET', 'POST'])
def student_reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    student = Student.verify_reset_password_token(token)
    if not student:
        return redirect(url_for('auth.student_login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        student.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset. Login to continue')
        return redirect(url_for('auth.student_login'))
    return render_template('reset_password.html',
                           form=form,
                           title='Reset Password'
                           )


@bp.route('/login/teacher/request-password-reset', methods=['GET', 'POST'])
def teacher_request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RquestPasswordResetForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(email=form.email.data).first()
        if teacher:
            teacher_send_password_reset_email(teacher)
        flash('Check your email for instructions to reset your password')
        return redirect(url_for('auth.teacher_login'))
    return render_template('request_password_reset.html',
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
    return render_template('reset_password.html',
                           form=form,
                           title='Reset Password'
                           )
# End of password reset


# Two-factor authentication

@bp.route('/parent/<username>/enable-2fa', methods=['GET', 'POST'])
@login_required
def parent_enable_2fa(username):
    parent = Parent.query.filter_by(username=username).first_or_404()
    form = Enable2faForm()
    if form.validate_on_submit():
        session['phone'] = form.verification_phone.data
        request_verification_token(session['phone'])
        return redirect(url_for('auth.parent_verify_2fa', username=parent.username))
    return render_template('enable_2fa.html',
                           form=form,
                           title='Enable 2FA'
                           )


@bp.route('/parent/<username>/confirm-2fa', methods=['GET', 'POST'])
def parent_verify_2fa(username):
    parent = Parent.query.filter_by(username=username).first_or_404()
    form = Confirm2faForm()
    if form.validate_on_submit():
        phone = session['phone']
        if check_verification_token(phone, form.token.data):
            del session['phone']
            login_user(parent)
            if parent.is_authenticated:
                parent.verification_phone = phone
                db.session.commit()
                flash('You have enabled two-factor authentication')
                return redirect(url_for('main.parent_profile',
                                        username=parent.username))
            else:
                username = session['username']
                del session['username']
                parent = Parent.query.filter_by(username=username).first()
                next_page = request.args.get('next')
                remember = request.args.get('remember', '0') == '1'
                login_user(parent, remember=remember)
                return redirect(url_for(next_page))
        form.token.errors.append('Invalid token')
    return render_template('verify_2fa.html',
                           form=form,
                           title='Verify Token'
                           )


@bp.route('/parent/<username>/disable-2fa', methods=['GET', 'POST'])
def parent_disable_2fa(username):
    parent = Parent.query.filter_by(username=username).first_or_404()
    form = Disable2faForm()
    if form.validate_on_submit():
        parent.verification_phone = None
        db.session.commit()
        flash('You have disabled two-factor authentication')
        return redirect(url_for('main.parent_profile',
                                username=parent.username))
    return render_template('disable_2fa.html',
                           form=form,
                           title='Disable 2FA'
                           )


@bp.route('/student/<username>/enable-2fa', methods=['GET', 'POST'])
@login_required
def student_enable_2fa(username):
    student = Student.query.filter_by(username=username).first_or_404()
    form = Enable2faForm()
    if form.validate_on_submit():
        session['phone'] = form.verification_phone.data
        request_verification_token(session['phone'])
        return redirect(url_for('auth.student_verify_2fa',
                                username=student.username))
    return render_template('enable_2fa.html',
                           form=form,
                           title='Enable 2FA'
                           )


@bp.route('/student/<username>/confirm-2fa', methods=['GET', 'POST'])
def student_verify_2fa(username):
    student = Student.query.filter_by(username=username).first_or_404()
    form = Confirm2faForm()
    if form.validate_on_submit():
        phone = session['phone']
        if check_verification_token(phone, form.token.data):
            del session['phone']
            login_user(student)
            if student.is_authenticated:
                student.verification_phone = phone
                db.session.commit()
                flash('You have enabled two-factor authentication')
                return redirect(url_for('main.student_profile',
                                        username=student.username))
            else:
                username = session['username']
                del session['username']
                student = Student.query.filter_by(username=username).first()
                next_page = request.args.get('next')
                remember = request.args.get('remember', '0') == '1'
                login_user(student, remember=remember)
                return redirect(url_for(next_page))
        form.token.errors.append('Invalid token')
    return render_template('verify_2fa.html',
                           form=form,
                           title='Verify Token'
                           )


@bp.route('/student/<username>/disable-2fa', methods=['GET', 'POST'])
def student_disable_2fa(username):
    student = Student.query.filter_by(username=username).first_or_404()
    form = Disable2faForm()
    if form.validate_on_submit():
        student.verification_phone = None
        db.session.commit()
        flash('You have diabled two-factor authentication')
        return redirect(url_for('main.student_profile',
                                username=student.username))
    return render_template('disable_2fa.html',
                           form=form,
                           title='Disable 2FA'
                           )


@bp.route('/teacher/<username>/enable-2fa', methods=['GET', 'POST'])
@login_required
def teacher_enable_2fa(username):
    teacher = Teacher.query.filter_by(username=username).first_or_404()
    form = Enable2faForm()
    if form.validate_on_submit():
        session['phone'] = form.verification_phone.data
        request_verification_token(session['phone'])
        return redirect(url_for('auth.teacher_verify_2fa',
                                username=teacher.username))
    return render_template('enable_2fa.html',
                           form=form,
                           title='Enable 2FA'
                           )


@bp.route('/teacher/<username>/confirm-2fa', methods=['GET', 'POST'])
def teacher_verify_2fa(username):
    teacher = Teacher.query.filter_by(username=username).first_or_404()
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
                                        username=teacher.username))
            else:
                username = session['username']
                del session['username']
                teacher = Teacher.query.filter_by(username=username).first()
                next_page = request.args.get('next')
                remember = request.args.get('remember', '0') == '1'
                login_user(teacher, remember=remember)
                return redirect(url_for(next_page))
        form.token.errors.append('Invalid token')
    return render_template('verify_2fa.html',
                           form=form,
                           title='Verify Token'
                           )


@bp.route('/teacher/<username>/disable-2fa', methods=['GET', 'POST'])
def teacher_disable_2fa(username):
    teacher = Teacher.query.filter_by(username=username).first_or_404()
    form = Disable2faForm()
    if form.validate_on_submit():
        teacher.verification_phone = None
        db.session.commit()
        flash('You have diabled two-factor authentication')
        return redirect(url_for('main.teacher_profile',
                                username=teacher.username))
    return render_template('disable_2fa.html',
                           form=form,
                           title='Disable 2FA'
                           )
# End of two-factor authentication

# --------------------------
# End of User Authentication
# --------------------------
