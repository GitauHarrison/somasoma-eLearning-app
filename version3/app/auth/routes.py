from app import db
from app.auth import bp
from flask import render_template, redirect, url_for, flash, session,\
    request
from app.auth.forms import LoginForm, StudentRegistrationForm,\
    RequestPasswordResetForm, ResetPasswordForm, Enable2faForm,\
    Disable2faForm, Confirm2faForm, ParentRegistrationForm, \
    TeacherRegistrationForm
from app.models import Parent, Student, Teacher
from app.auth.twilio_verify_api import check_verification_token,\
    request_verification_token
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@bp.route('/parent/login', methods=['GET', 'POST'])
def login_parent():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_parent'))
    form = LoginForm()
    if form.validate_on_submit():
        parent = Parent.query.filter_by(parent_email=form.email.data).first()
        if parent is None or not parent.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login_parent'))
        login_user(parent, remember=form.remember_me.data)
        return redirect(url_for('dashboard_parent'))
    return render_template('auth/login_parent.html',
                           title='Parent Login',
                           form=form
                           )


@bp.route('/teacher/login', methods=['GET', 'POST'])
def login_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_teacher'))
    form = LoginForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(
            teacher_email=form.email.data
            ).first()
        if teacher is None or not teacher.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login_teacher'))
        login_user(teacher, remember=form.remember_me.data)
        return redirect(url_for('dashboard_teacher'))
    return render_template('auth/login_teacher.html',
                           title='Teacher Login',
                           form=form
                           )


@bp.route('/student/login', methods=['GET', 'POST'])
def login_student():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_student'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(
            student_email=form.email.data
            ).first()
        if student is None or not student.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login_student'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.dashboard_student')
        if student.two_factor_student_enabled():
            request_verification_token(student.student_phone)
            session['student_email'] = student.student_email
            session['phone'] = student.student_phone
            return redirect(url_for(
                'auth.verify_2fa_student',
                next=next_page,
                remember='1' if form.remember_me.data else '0'
                )
            )
        login_user(student, remember=form.remember_me.data)
        flash(f'Welcome {student.student_full_name}!')
        return redirect(next_page)
    return render_template('auth/login_student.html',
                           title='Student Login',
                           form=form
                           )


@bp.route('/student/logout')
def logout_student():
    logout_user()
    return redirect(url_for('auth.login_student'))


@bp.route('/parent/logout')
def logout_parent():
    logout_user()
    return redirect(url_for('auth.login_parent'))


@bp.route('/teacher/logout')
def logout_teacher():
    logout_user()
    return redirect(url_for('auth.login_teacher'))


@bp.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_student'))
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        student = Student(
            student_full_name=form.student_full_name.data,
            student_email=form.student_email.data,
            student_phone=form.student_phone.data,
            student_school=form.student_school.data,
            student_age=form.student_age.data,
            student_course=form.student_course.data
        )
        student.set_password(form.student_password.data)
        db.session.add(student)
        db.session.commit()
        flash(
            'Student successfully registered. Student can login to continue!'
            )
        return redirect(url_for('auth.login_student'))
    return render_template('auth/register_student.html',
                           title='Student Registration',
                           form=form
                           )


@bp.route('/register/parent', methods=['GET', 'POST'])
def register_parent():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_parent'))
    form = ParentRegistrationForm()
    if form.validate_on_submit():
        parent = Parent(
            parent_full_name=form.parent_full_name.data,
            parent_email=form.parent_email.data,
            parent_phone=form.parent_phone.data,
            parent_occupation=form.parent_occupation.data,
            parent_residence=form.parent_residence.data
        )
        parent.set_password(form.parent_password.data)
        db.session.add(parent)
        db.session.commit()
        flash(
            'Parent successfully registered. You can now register your child!'
            )
        return redirect(url_for('auth.register_student'))
    return render_template('auth/register_parent.html',
                           title='Parent Registration',
                           form=form
                           )


@bp.route('/register/teacher', methods=['GET', 'POST'])
def register_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_teacher'))
    form = TeacherRegistrationForm()
    if form.validate_on_submit():
        teacher = Teacher(
            teacher_full_name=form.teacher_full_name.data,
            teacher_email=form.teacher_email.data,
            teacher_phone=form.teacher_phone.data,
            teacher_residence=form.teacher_residence.data,
            teacher_course=form.teacher_course.data
        )
        teacher.set_password(form.teacher_password.data)
        db.session.add(teacher)
        db.session.commit()
        flash('Teacher successfully registered. Login to continue!')
        return redirect(url_for('auth.login_teacher'))
    return render_template('auth/register_teacher.html',
                           title='Teacher Registration',
                           form=form
                           )


@bp.route('/request-password-reset', methods=['GET', 'POST'])
def request_password_reset():
    form = RequestPasswordResetForm()
    return render_template('auth/request_password_reset.html',
                           title='Request Password Reset',
                           form=form
                           )


@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    return render_template('auth/reset_password.html',
                           title='Reset Password',
                           form=form
                           )

# Two-factor authentication


@bp.route('/student/enable-2fa', methods=['GET', 'POST'])
@login_required
def enable_2fa_student():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first_or_404()
    form = Enable2faForm()
    if form.validate_on_submit():
        session['phone'] = form.verification_phone.data
        request_verification_token(session['phone'])
        return redirect(url_for('auth.verify_2fa_student'))
    return render_template('auth/enable_2fa.html',
                           form=form,
                           title='Enable 2fa',
                           student=student
                           )


@bp.route('/student/verify-2fa', methods=['GET', 'POST'])
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
                return redirect(url_for(
                    'main.dashboard_student',
                    _anchor='account')
                    )
            else:
                student_email = session['student_email']
                del session['student_email']
                student = Student.query.filter_by(
                    student_email=student_email
                    ).first()
                next_page = request.args.get('next')
                remember = request.args.get('remember', '0') == '1'
                login_user(student, remember=remember)
                return redirect(next_page)
        form.token.errors.append('Invalid token')
    return render_template('auth/verify_2fa.html',
                           form=form,
                           title='Verify Token'
                           )


@bp.route('/student/disable-2fa', methods=['GET', 'POST'])
@login_required
def disable_2fa_student():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first_or_404()
    form = Disable2faForm()
    if form.validate_on_submit():
        current_user.student_phone = None
        db.session.commit()
        flash('You have disabled two-factor authentication')
        return redirect(url_for('main.dashboard_student', _anchor='account'))
    return render_template(
        'auth/disable_2fa.html',
        form=form,
        title='Disable 2fa',
        student=student
        )
