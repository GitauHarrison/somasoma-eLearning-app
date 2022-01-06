from app import db
from app.auth import bp
from flask import render_template, redirect, url_for, flash, session,\
    request
from app.auth.forms import LoginForm, StudentRegistrationForm,\
    RequestPasswordResetForm, ResetPasswordForm, Enable2faForm,\
    Disable2faForm, Confirm2faForm, ParentRegistrationForm, \
    AdminRegistrationForm
from app.models import Parent, Student, Teacher, Admin
from app.auth.twilio_verify_api import check_verification_token,\
    request_verification_token
from app.auth.email import send_password_reset_email_student,\
    send_password_reset_email_admin, send_registration_details_parent,\
    send_registration_details_student, send_password_reset_email_teacher
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@bp.route('/login')
def login():
    return render_template(
        'auth/login.html',
        title='Login')


@bp.route('/login/parent', methods=['GET', 'POST'])
def login_parent():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_account'))
    form = LoginForm()
    if form.validate_on_submit():
        parent = Parent.query.filter_by(parent_email=form.email.data).first()
        if parent is None or not parent.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login_parent'))
        login_user(parent, remember=form.remember_me.data)
        flash(f'Welcome {parent.parent_full_name}!')
        return redirect(url_for('main.dashboard_account'))
    return render_template(
        'auth/login_parent.html',
        title='Parent Login',
        form=form
        )


@bp.route('/login/teacher', methods=['GET', 'POST'])
def login_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('teacher.dashboard_account'))
    form = LoginForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(
            teacher_email=form.email.data
            ).first()
        if teacher is None or not teacher.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login_teacher'))
        login_user(teacher, remember=form.remember_me.data)
        flash(f'Welcome {teacher.teacher_full_name}!')
        return redirect(url_for('teacher.dashboard_account'))
    return render_template(
        'auth/login_teacher.html',
        title='Teacher Login',
        form=form
        )


@bp.route('/login/student', methods=['GET', 'POST'])
def login_student():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard_enrolled_courses'))
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
            next_page = url_for('student.dashboard_enrolled_courses')
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
    return render_template(
        'auth/login_student.html',
        title='Student Login',
        form=form
        )


@bp.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard_account'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(
            admin_email=form.email.data
            ).first()
        if admin is None or not admin.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login_admin'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.dashboard_account')
        if admin.two_factor_admin_enabled():
            request_verification_token(admin.admin_phone)
            session['admin_email'] = admin.admin_email
            session['phone'] = admin.admin_phone
            return redirect(url_for(
                'auth.verify_2fa_admin',
                next=next_page,
                remember='1' if form.remember_me.data else '0'
                )
            )
        login_user(admin, remember=form.remember_me.data)
        flash(f'Welcome {admin.admin_full_name}!')
        return redirect(next_page)
    return render_template(
        'auth/login_admin.html',
        title='Admin Login',
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


@bp.route('/admin/logout')
def logout_admin():
    logout_user()
    return redirect(url_for('auth.login_admin'))


@bp.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard_enrolled_courses'))
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
        send_registration_details_student(student)
        flash(
            'Student successfully registered. Check your email for '
            'further instructions!'
            )
        return redirect(url_for('main.home'))
    return render_template(
        'auth/register_user.html',
        title='Student Registration',
        form=form
        )


@bp.route('/register/parent', methods=['GET', 'POST'])
def register_parent():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_account'))
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
        send_registration_details_parent(parent)
        flash(
            'Parent successfully registered. You can now register your child!'
            )
        return redirect(url_for('auth.register_student'))
    return render_template(
        'auth/register_user.html',
        title='Parent Registration',
        form=form
        )


@bp.route('/register/admin', methods=['GET', 'POST'])
def register_admin():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard_account'))
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        admin = Admin(
            admin_full_name=form.admin_full_name.data,
            admin_email=form.admin_email.data,
            admin_phone=form.admin_phone.data
        )
        admin.set_password(form.admin_password.data)
        db.session.add(admin)
        db.session.commit()
        flash('Admin successfully registered. Login to continue!')
        return redirect(url_for('auth.login_admin'))
    return render_template(
        'auth/register_user.html',
        title='Admin Registration',
        form=form
        )


# =================================================
# PASSWORD RESET
# =================================================

# Student

@bp.route('/request-password-reset', methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard_enrolled_courses'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(
            student_email=form.email.data
            ).first()
        if student:
            send_password_reset_email_student(student)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login_student'))
    return render_template(
        'auth/password-reset/request_password_reset.html',
        title='Request Password Reset',
        form=form
        )


@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard_enrolled_courses'))
    student = Student.verify_reset_password_token(token)
    if not student:
        return redirect(url_for('student.dashboard_enrolled_courses'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        student.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login_student'))
    return render_template(
        'auth/password-reset/reset_password.html',
        title='Reset Password',
        form=form
        )

# Admin


@bp.route('/admin/request-password-reset', methods=['GET', 'POST'])
def request_password_reset_admin():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard_account'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(
            admin_email=form.email.data
            ).first()
        if admin:
            send_password_reset_email_admin(admin)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login_admin'))
    return render_template(
        'auth/password-reset/request_password_reset_admin.html',
        title='Request Password Reset for Admin',
        form=form
        )


@bp.route('/admin/reset-password/<token>', methods=['GET', 'POST'])
def reset_password_admin(token):
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard_account'))
    admin = Admin.verify_reset_password_token(token)
    if not admin:
        return redirect(url_for('admin.dashboard_account'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        admin.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login_admin'))
    return render_template(
        'auth/password-reset/reset_password_admin.html',
        title='Reset Password for Admin',
        form=form
        )


# Teacher


@bp.route('/teacher/request-password-reset', methods=['GET', 'POST'])
def request_password_reset_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('teacher.dashboard_account'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(
            teacher_email=form.email.data
            ).first()
        if teacher:
            send_password_reset_email_teacher(teacher)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login_teacher'))
    return render_template(
        'auth/password-reset/request_password_reset_teacher.html',
        title='Request Password Reset for Teacher',
        form=form
        )


@bp.route('/teacher/reset-password/<token>', methods=['GET', 'POST'])
def reset_password_teacher(token):
    if current_user.is_authenticated:
        return redirect(url_for('teacher.dashboard_account'))
    teacher = Teacher.verify_reset_password_token(token)
    if not teacher:
        return redirect(url_for('teacher.dashboard_account'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        teacher.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login_teacher'))
    return render_template(
        'auth/password-reset/reset_password_teacher.html',
        title='Reset Password for Teacher',
        form=form
        )

# =================================================
# END OF PASSWORD RESET
# =================================================

# =================================================
# TWO-FACTOR AUTHENTICATION
# =================================================

# Student


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
    return render_template(
        'auth/two-factor-auth/student/enable_2fa.html',
        form=form,
        title='Enable 2fa',
        student=student
        )


@bp.route('/student/verify-2fa', methods=['GET', 'POST'])
def verify_2fa_student():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first_or_404()
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
                    'student.dashboard_account',
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
    return render_template(
        'auth/two-factor-auth/student/verify_2fa.html',
        form=form,
        title='Verify Token',
        student=student
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
        return redirect(url_for(
            'student.dashboard_account',
            _anchor='account'
            )
        )
    return render_template(
        'auth/two-factor-auth/student/disable_2fa.html',
        form=form,
        title='Disable 2fa',
        student=student
        )

# Admin


@bp.route('/admin/enable-2fa', methods=['GET', 'POST'])
@login_required
def enable_2fa_admin():
    admin = Admin.query.filter_by(
        admin_full_name=current_user.admin_full_name
        ).first_or_404()
    form = Enable2faForm()
    if form.validate_on_submit():
        session['phone'] = form.verification_phone.data
        request_verification_token(session['phone'])
        return redirect(url_for('auth.verify_2fa_admin'))
    return render_template(
        'auth/two-factor-auth/admin/enable_2fa_admin.html',
        form=form,
        title='Enable 2fa for Admin',
        admin=admin
        )


@bp.route('/admin/verify-2fa', methods=['GET', 'POST'])
def verify_2fa_admin():
    form = Confirm2faForm()
    if form.validate_on_submit():
        phone = session['phone']
        if check_verification_token(phone, form.token.data):
            del session['phone']
            if current_user.is_authenticated:
                current_user.admin_phone = phone
                db.session.commit()
                flash('You have enabled two-factor authentication')
                return redirect(url_for(
                    'admin.dashboard_account',
                    _anchor='account')
                    )
            else:
                admin_email = session['admin_email']
                del session['admin_email']
                admin = Admin.query.filter_by(
                    admin_email=admin_email
                    ).first()
                next_page = request.args.get('next')
                remember = request.args.get('remember', '0') == '1'
                login_user(admin, remember=remember)
                return redirect(next_page)
        form.token.errors.append('Invalid token')
    return render_template(
        'auth/two-factor-auth/admin/verify_2fa_admin.html',
        form=form,
        title='Verify Token for Admin'
        )


@bp.route('/admin/disable-2fa', methods=['GET', 'POST'])
@login_required
def disable_2fa_admin():
    admin = Admin.query.filter_by(
        admin_full_name=current_user.admin_full_name
        ).first_or_404()
    form = Disable2faForm()
    if form.validate_on_submit():
        current_user.admin_phone = None
        db.session.commit()
        flash('You have disabled two-factor authentication')
        return redirect(url_for('admin.dashboard_account', _anchor='account'))
    return render_template(
        'auth/two-factor-auth/admin/disable_2fa_admin.html',
        form=form,
        title='Disable 2fa for Admin',
        admin=admin
        )

# Teacher


@bp.route('/teacher/enable-2fa', methods=['GET', 'POST'])
@login_required
def enable_2fa_teacher():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first_or_404()
    form = Enable2faForm()
    if form.validate_on_submit():
        session['phone'] = form.verification_phone.data
        request_verification_token(session['phone'])
        return redirect(url_for('auth.verify_2fa_teacher'))
    return render_template(
        'auth/two-factor-auth/teacher/enable_2fa_teacher.html',
        form=form,
        title='Enable 2fa for Teacher',
        teacher=teacher
        )


@bp.route('/teacher/verify-2fa', methods=['GET', 'POST'])
def verify_2fa_teacher():
    form = Confirm2faForm()
    if form.validate_on_submit():
        phone = session['phone']
        if check_verification_token(phone, form.token.data):
            del session['phone']
            if current_user.is_authenticated:
                current_user.teacher_phone = phone
                db.session.commit()
                flash('You have enabled two-factor authentication')
                return redirect(url_for(
                    'teacher.dashboard_account',
                    _anchor='account')
                    )
            else:
                teacher_email = session['teacher_email']
                del session['teacher_email']
                teacher = Teacher.query.filter_by(
                    teacher_email=teacher_email
                    ).first()
                next_page = request.args.get('next')
                remember = request.args.get('remember', '0') == '1'
                login_user(teacher, remember=remember)
                return redirect(next_page)
        form.token.errors.append('Invalid token')
    return render_template(
        'auth/two-factor-auth/teacher/verify_2fa_teacher.html',
        form=form,
        title='Verify Token for Teacher'
        )


@bp.route('/teacher/disable-2fa', methods=['GET', 'POST'])
@login_required
def disable_2fa_teacher():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first_or_404()
    form = Disable2faForm()
    if form.validate_on_submit():
        current_user.teacher_phone = None
        db.session.commit()
        flash('You have disabled two-factor authentication')
        return redirect(url_for(
            'teacher.dashboard_account',
            _anchor='account'
            )
        )
    return render_template(
        'auth/two-factor-auth/teacher/disable_2fa_teacher.html',
        form=form,
        title='Disable 2fa for Teacher',
        teacher=teacher
        )

# =================================================
# TWO-FACTOR AUTHENTICATION
# =================================================
