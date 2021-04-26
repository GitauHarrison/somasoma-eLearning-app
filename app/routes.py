from app import app, db
from flask import render_template, url_for, redirect, flash, request
from app.forms import StudentRegistrationForm, ParentRegistrationForm,\
    TeacherRegistrationForm, LoginForm, RquestPasswordResetForm,\
    ResetPasswordForm, ParentEditProfileForm, StudentEditProfileForm,\
    TeacherEditProfileForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Teacher, Student, Parent
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# --------------------
# User Authentication
# --------------------


@app.route('/register/parent/', methods=['GET', 'POST'])
def parent_registration():
    form = ParentRegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        flash('Congratulations! You have successfully registered as a parent')
        return redirect(url_for('student_registration'))
    return render_template('parent_registration.html',
                           form=form,
                           title='Register'
                           )


@app.route('/register/student/', methods=['GET', 'POST'])
def student_registration():
    form = StudentRegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        flash('Congratulations! You have successfully registered '
              f'{student.first_name} as a student')
        return redirect(url_for('login'))
    return render_template('student_registration.html',
                           form=form,
                           title='Register'
                           )


@app.route('/register/teacher/', methods=['GET', 'POST'])
def teacher_registration():
    form = TeacherRegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('login'))
    return render_template('teacher_registration.html',
                           form=form,
                           title='Register'
                           )


@app.route('/login')
def login():
    return render_template('all_users_login.html', title='Login')


@app.route('/login/parent/', methods=['GET', 'POST'])
def parent_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        parent = Parent.query.filter_by(username=form.username.data).first()
        if parent is None or not parent.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('parent_login'))
        login_user(parent, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('parent_profile',
                                username=current_user.username)
        return redirect(next_page)
    return render_template('login.html',
                           form=form,
                           title='Parent Login'
                           )


@app.route('/login/student', methods=['GET', 'POST'])
def student_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(username=form.username.data).first()
        if student is None or not student.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('student_login'))
        login_user(student, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('student_profile',
                                username=current_user.username)
        return redirect(next_page)
    return render_template('login.html',
                           form=form,
                           title='Student Login'
                           )


@app.route('/login/teacher', methods=['GET', 'POST'])
def teacher_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(username=form.username.data).first()
        if teacher is None or not teacher.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('teacher_login'))
        login_user(teacher, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('teacher_profile',
                                username=current_user.username)
        return redirect(next_page)
    return render_template('login.html',
                           form=form,
                           title='Teacher Login'
                           )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login/request-password-reset', methods=['GET', 'POST'])
def request_password_reset():
    form = RquestPasswordResetForm()
    return render_template('request_password_reset.html',
                           form=form,
                           title='Request Password Reset'
                           )


@app.route('/login/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    return render_template('reset_password.html',
                           form=form,
                           title='Reset Password'
                           )

# --------------------------
# End of User Authentication
# --------------------------


# ------------
# User Profile
# ------------

@app.route('/profile/parent/<username>')
@login_required
def parent_profile(username):
    parent = Parent.query.filter_by(username=username).first_or_404()
    print(parent)
    print(parent.username)
    return render_template('parent_profile.html',
                           parent=parent,
                           title='Parent Profile'
                           )


@app.route('/profile/parent/<username>/edit-profile', methods=['GET', 'POST'])
def edit_parent_profile(username):
    parent = Parent.query.filter_by(username=username).first_or_404()
    form = ParentEditProfileForm(parent.username)
    if form.validate_on_submit():
        parent.username = form.username.data
        parent.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('parent_profile',
                                username=parent.username))
    elif request.method == 'GET':
        form.username.data = parent.username
        form.about_me.data = parent.about_me
    return render_template('edit_profile.html',
                           form=form,
                           title='Edit Parent Profile'
                           )


@app.route('/profile/parent/<username>/delete-account')
def delete_parent_account(username):
    parent = Parent.query.filter_by(username=username).first_or_404()
    db.session.delete(parent)
    db.session.commit()
    flash(f'Your parent account {parent.username} was successfully deleted')
    return redirect(url_for('home'))


@app.route('/profile/student/<username>')
@login_required
def student_profile(username):
    student = Student.query.filter_by(username=username).first_or_404()
    return render_template('student_profile.html',
                           student=student,
                           title='Student Profile'
                           )


@app.route('/profile/student/<username>/edit-profile', methods=['GET', 'POST'])
def edit_student_profile(username):
    student = Student.query.filter_by(username=username).first_or_404()
    form = StudentEditProfileForm(student.username)
    if form.validate_on_submit():
        student.username = form.username.data
        student.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('student_profile',
                                username=student.username))
    elif request.method == 'GET':
        form.username.data = student.username
        form.about_me.data = student.about_me
    return render_template('edit_profile.html',
                           form=form,
                           title='Edit Student Profile'
                           )


@app.route('/profile/student/<username>/delete-account')
def delete_student_account(username):
    student = Student.query.filter_by(username=username).first_or_404()
    db.session.delete(student)
    db.session.commit()
    flash(f'Your student account {student.username} was successfully deleted')
    return redirect(url_for('home'))


@app.route('/profile/teacher/<username>')
@login_required
def teacher_profile(username):
    teacher = Teacher.query.filter_by(username=username).first_or_404()
    return render_template('teacher_profile.html',
                           teacher=teacher,
                           title='Teacher Profile'
                           )


@app.route('/profile/teacher/<username>/edit-profile', methods=['GET', 'POST'])
def edit_teacher_profile(username):
    teacher = Teacher.query.filter_by(username=username).first_or_404()
    form = TeacherEditProfileForm(teacher.username)
    if form.validate_on_submit():
        teacher.username = form.username.data
        teacher.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('teacher_profile',
                                username=teacher.username))
    elif request.method == 'GET':
        form.username.data = teacher.username
        form.about_me.data = teacher.about_me
    return render_template('edit_profile.html',
                           form=form,
                           title='Edit Teacher Profile'
                           )


@app.route('/profile/teacher/<username>/delete-account')
def delete_teacher_account(username):
    teacher = Teacher.query.filter_by(username=username).first_or_404()
    db.session.delete(teacher)
    db.session.commit()
    flash(f'Your teacher account {teacher.username} was successfully deleted')
    return redirect(url_for('home'))


# -------------------
# End of User Profile
# -------------------
