from app import app, db
from flask import render_template, url_for, redirect, flash, request
from app.forms import StudentRegistrationForm, ParentRegistrationForm,\
    TeacherRegistrationForm, LoginForm, RquestPasswordResetForm,\
    ResetPasswordForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Teacher, Student, Parent
from werkzeug.urls import url_parse


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
        flash(f'Congratulations! You have successfully registered {student.first_name} as a student')
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
            return redirect(url_for('login'))
        login_user(parent, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
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
            return redirect(url_for('login'))
        login_user(student, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
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
            return redirect(url_for('login'))
        login_user(teacher, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
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
