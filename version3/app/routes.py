from app import app, db
from flask import render_template, redirect, url_for, flash, session,\
    request, abort
from app.forms import LoginForm, StudentRegistrationForm,\
    RequestPasswordResetForm, ResetPasswordForm, CommentForm,\
    Enable2faForm, Disable2faForm, Confirm2faForm, EditProfileForm,\
    Chapter1WebDevelopmentForm, QuizForm, Chapter1QuizOptionsForm,\
    ParentRegistrationForm, TeacherRegistrationForm
from app.models import WebDevChapter1Comment, CommunityComment,\
    WebDevChapter1Objectives, WebDevChapter1Quiz, WebDevChapter1QuizOptions,\
    Parent, Student, Teacher
from app.twilio_verify_api import check_verification_token,\
    request_verification_token
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.student_last_seen = datetime.utcnow()
        db.session.commit()


# ========================================
# MAIN ROUTES
# ========================================


@app.route('/student/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_student():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    comments = CommunityComment.query.order_by(
        CommunityComment.timestamp.desc()
        ).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
                    'dashboard_student',
                    page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'dashboard_student',
        page=comments.prev_num) \
        if comments.has_prev else None
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = CommunityComment(
            body=comment_form.comment.data,
            author=current_user
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('dashboard_student'))

    # Calculate the number of objectives achieved
    all_objectives = student.webdev_chapter1_objectives.order_by(
        WebDevChapter1Objectives.timestamp.desc()).all()
    objectives_list = []
    num_of_true_status = 0
    for objective in all_objectives:
        objectives_list.append(objective.objective_1)
        objectives_list.append(objective.objective_2)
        objectives_list.append(objective.objective_3)
        objectives_list.append(objective.objective_4)
        objectives_list.append(objective.objective_5)
        objectives_list.append(objective.objective_6)
        objectives_list.append(objective.objective_7)
    num_of_true_status = objectives_list.count(True)
    try:
        percentage_achieved = round(
            (num_of_true_status / len(objectives_list)) * 100, 2
        )
    except ZeroDivisionError:
        abort(404)
    return render_template(
                           'dashboard_student.html',
                           title='Student Dashboard',
                           comment_form=comment_form,
                           comments=comments.items,
                           next_url=next_url,
                           prev_url=prev_url,
                           all_objectives=all_objectives,
                           percentage_achieved=percentage_achieved,
                           student=student
                           )


@app.route('/parent/dashboard')
@login_required
def dashboard_parent():
    parent = Parent.query.filter_by(
        parent_full_name=current_user.parent_full_name
        ).first()
    return render_template(
        'dashboard_parent.html',
        title='Parent Dashboard',
        parent=parent
        )


@app.route('/teacher/dashboard')
@login_required
def dashboard_teacher():
    return render_template('dashboard_teacher.html')


@app.route('/login')
def login():
    return render_template('login.html',
                           title='Login'
                           )


@app.route('/student/<student_full_name>/profile')
@login_required
def profile_student(student_full_name):
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = student.comments.order_by(
        CommunityComment.timestamp.desc()
        ).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'dashboard_student', student_full_name=student_full_name,
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'dashboard_student', student_full_name=student_full_name,
        page=comments.prev_num) \
        if comments.has_prev else None
    return render_template('profile_student.html',
                           title='Profile',
                           student=student,
                           comments=comments.items,
                           next_url=next_url,
                           prev_url=prev_url
                           )


@app.route('/student/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile_student():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    form = EditProfileForm(current_user.student_email)
    if form.validate_on_submit():
        current_user.student_email = form.email.data
        current_user.student_about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('dashboard_student'))
    elif request.method == 'GET':
        form.email.data = current_user.student_email
        form.about_me.data = current_user.student_about_me
    return render_template('edit_profile_student.html',
                           title='Edit Profile',
                           form=form,
                           student=student
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
        parent = Parent.query.filter_by(parent_email=form.email.data).first()
        if parent is None or not parent.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login_parent'))
        login_user(parent, remember=form.remember_me.data)
        return redirect(url_for('dashboard_parent'))
    return render_template('login_parent.html',
                           title='Parent Login',
                           form=form
                           )


@app.route('/teacher/login', methods=['GET', 'POST'])
def login_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_teacher'))
    form = LoginForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(teacher_email=form.email.data).first()
        if teacher is None or not teacher.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login_teacher'))
        login_user(teacher, remember=form.remember_me.data)
        return redirect(url_for('dashboard_teacher'))
    return render_template('login_teacher.html',
                           title='Teacher Login',
                           form=form
                           )


@app.route('/student/login', methods=['GET', 'POST'])
def login_student():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_student'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(
            student_email=form.email.data
            ).first()
        if student is None or not student.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login_student'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard_student')
        if student.two_factor_student_enabled():
            request_verification_token(student.student_phone)
            session['student_email'] = student.student_email
            session['phone'] = student.student_phone
            return redirect(url_for(
                'verify_2fa_student',
                next=next_page,
                remember='1' if form.remember_me.data else '0'
                )
            )
        login_user(student, remember=form.remember_me.data)
        return redirect(next_page)
    return render_template('login_student.html',
                           title='Student Login',
                           form=form
                           )


@app.route('/student/logout')
def logout_student():
    logout_user()
    return redirect(url_for('login_student'))


@app.route('/parent/logout')
def logout_parent():
    logout_user()
    return redirect(url_for('login_parent'))


@app.route('/teacher/logout')
def logout_teacher():
    logout_user()
    return redirect(url_for('login_teacher'))


@app.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_student'))
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
        flash('Student successfully registered. Student can login to continue!')
        return redirect(url_for('login_student'))
    return render_template('register_student.html',
                           title='Student Registration',
                           form=form
                           )


@app.route('/register/parent', methods=['GET', 'POST'])
def register_parent():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_parent'))
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
        flash('Parent successfully registered. You can now register your child!')
        return redirect(url_for('register_student'))
    return render_template('register_parent.html',
                           title='Parent Registration',
                           form=form
                           )


@app.route('/register/teacher', methods=['GET', 'POST'])
def register_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_teacher'))
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
        return redirect(url_for('login_teacher'))
    return render_template('register_teacher.html',
                           title='Teacher Registration',
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
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first_or_404()
    form = Enable2faForm()
    if form.validate_on_submit():
        session['phone'] = form.verification_phone.data
        request_verification_token(session['phone'])
        return redirect(url_for('verify_2fa_student'))
    return render_template('enable_2fa.html',
                           form=form,
                           title='Enable 2fa',
                           student=student
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
                return redirect(url_for(
                    'dashboard_student',
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
    return render_template('verify_2fa.html',
                           form=form,
                           title='Verify Token'
                           )


@app.route('/student/disable-2fa', methods=['GET', 'POST'])
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
        return redirect(url_for('dashboard_student', _anchor='account'))
    return render_template(
        'disable_2fa.html',
        form=form,
        title='Disable 2fa',
        student=student
        )

# ========================================
# END OF AUTHENTICATION ROUTES
# ========================================

# ========================================
# WEB DEVELOPMENT COURSE ROUTES
# ========================================

# Overview


@app.route('/student/web-development-overview')
@login_required
def web_development_overview():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    return render_template(
        'web-development-course/web_development_overview.html',
        title='Web Development',
        student=student
        )

# Chapters


@app.route('/student/web-development/chapter-1', methods=['GET', 'POST'])
@login_required
def web_development_chapter_1():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    comments = WebDevChapter1Comment.query.order_by(
        WebDevChapter1Comment.timestamp.desc()
        ).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
                       'web_development_chapter_1',
                       _anchor="comments",
                       page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
                       'web_development_chapter_1',
                       _anchor='comments',
                       page=comments.prev_num) \
        if comments.has_prev else None
    form = CommentForm()
    if form.validate_on_submit():
        comment = WebDevChapter1Comment(
            body=form.comment.data,
            author=current_user
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for(
                                'web_development_chapter_1',
                                _anchor='comments',
                                student=student
                                )
                        )
    all_comments = len(WebDevChapter1Comment.query.all())

    # Objectives form
    objectives_form = Chapter1WebDevelopmentForm()
    if objectives_form.validate_on_submit():
        objectives = WebDevChapter1Objectives(
            objective_1=objectives_form.objective_1.data,
            objective_2=objectives_form.objective_2.data,
            objective_3=objectives_form.objective_3.data,
            objective_4=objectives_form.objective_4.data,
            objective_5=objectives_form.objective_5.data,
            objective_6=objectives_form.objective_6.data,
            objective_7=objectives_form.objective_7.data,
            author=current_user
        )
        db.session.add(objectives)
        db.session.commit()
        flash('Your response has been saved')
        return redirect(url_for(
            'web_development_chapter_1',
            _anchor='objectives'
        ))
    return render_template(
        'web-development-course/web_development_chapter_1.html',
        title='Chapter 1: Introduction to Web Development',
        form=form,
        objectives_form=objectives_form,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,
        all_comments=all_comments,
        student=student
        )


@app.route('/student/web-development/chapter-2', methods=['GET', 'POST'])
@login_required
def web_development_chapter_2():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    form = CommentForm()
    return render_template(
        'web-development-course/web_development_chapter_2.html',
        title='Chapter 2: What is HTML?',
        form=form,
        student=student
        )

# Objectives


@app.route('/student/web-development/chapter-1/objectives-status')
@login_required
def web_development_chapter_1_objectives_status():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    objectives = WebDevChapter1Objectives.query.order_by(
        WebDevChapter1Objectives.timestamp.desc()
        ).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
                       'web_development_chapter_1_objectives_status',
                       _anchor="objectives",
                       page=objectives.next_num) \
        if objectives.has_next else None
    prev_url = url_for(
                       'web_development_chapter_1_objectives_status',
                       _anchor='objectives',
                       page=objectives.prev_num) \
        if objectives.has_prev else None
    return render_template(
        'web-development-course/chapter_1_objectives_status.html',
        title='Chapter 1: Achievement Status',
        objectives=objectives.items,
        next_url=next_url,
        prev_url=prev_url,
        student=student
        )


# Quizzes


@app.route('/student/web-development/chapter-1/quizzes/form', methods=['GET', 'POST'])
@login_required
def web_development_chapter_1_quizzes_form():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    form = QuizForm()
    if form.validate_on_submit():
        quiz = WebDevChapter1Quiz(
            title=form.title.data,
            body=form.body.data
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Your quiz has been added!', 'success')
        return redirect(url_for(
            'web_development_chapter_1_quizzes_form',
            student_full_name=student.student_full_name
        ))
    return render_template(
        'quizzes-forms/quiz_type_1.html',
        title='Quiz Type 1',
        student=student,
        form=form
        )


@app.route('/student/<student_full_name>/web-development/chapter-1/quizzes', methods=['GET', 'POST'])
@login_required
def web_development_chapter_1_quiz():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    options = WebDevChapter1QuizOptions.query.order_by(
        WebDevChapter1QuizOptions.timestamp.asc()
        ).paginate(
        page, app.config['POSTS_PER_QUIZ_PAGE'], False)
    quizzes = WebDevChapter1Quiz.query.order_by(
        WebDevChapter1Quiz.timestamp.asc()
        ).paginate(
        page, app.config['POSTS_PER_QUIZ_PAGE'], False)
    next_url = url_for(
                        'web_development_chapter_1_quiz',
                        student_full_name=student.student_full_name,
                        _anchor="quizzes",
                        page=quizzes.next_num) \
        if quizzes.has_next else None
    prev_url = url_for(
                        'web_development_chapter_1_quiz',
                        student_full_name=student.student_full_name,
                        _anchor='quizzes',
                        page=quizzes.prev_num) \
        if quizzes.has_prev else None
    form = Chapter1QuizOptionsForm()
    return render_template(
        'web-development-course/chapter_1_quizzes.html',
        title='Chapter 1: Quizzes',
        student=student,
        quizzes=quizzes.items,
        options=options.items,
        form=form,
        next_url=next_url,
        prev_url=prev_url
        )

# ========================================
# END OF WEB DEVELOPMENT COURSE ROUTES
# ========================================
