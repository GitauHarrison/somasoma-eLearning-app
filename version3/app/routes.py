from app import app, db
from flask import render_template, redirect, url_for, flash, session,\
    request, abort
from app.forms import LoginForm, ClientRegistrationForm,\
    RequestPasswordResetForm, ResetPasswordForm, CommentForm,\
    Enable2faForm, Disable2faForm, Confirm2faForm, EditProfileForm,\
    Chapter1WebDevelopmentForm
from app.models import WebDevChapter1Comment, Client, CommunityComment, WebDevChapter1Objectives
from app.twilio_verify_api import check_verification_token,\
    request_verification_token
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request_student():
    if current_user.is_authenticated:
        current_user.student_last_seen = datetime.utcnow()
        db.session.commit()


@app.before_request
def before_request_parent():
    if current_user.is_authenticated:
        current_user.parent_last_seen = datetime.utcnow()
        db.session.commit()

# ========================================
# MAIN ROUTES
# ========================================


@app.route('/student/<student_full_name>/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_student(student_full_name):
    student = Client.query.filter_by(student_full_name=student_full_name).first()
    page = request.args.get('page', 1, type=int)
    comments = CommunityComment.query.order_by(CommunityComment.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
                    'dashboard_student', student_full_name=student_full_name,
                    page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('dashboard_student', page=comments.prev_num) \
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
        percentage_achieved = round((num_of_true_status / len(objectives_list)) * 100, 2)
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
                           percentage_achieved=percentage_achieved
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


@app.route('/student/<student_full_name>/profile')
@login_required
def profile_student(student_full_name):
    student = Client.query.filter_by(student_full_name=student_full_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = student.comments.order_by(CommunityComment.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('dashboard_student', page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('dashboard_student', page=comments.prev_num) \
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
                           form=form
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
        return redirect(url_for('dashboard_student', student_full_name=current_user.student_full_name))
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
            return redirect(url_for('verify_2fa_student', student_full_name=student.student_full_name,
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


@app.route('/student//enable-2fa', methods=['GET', 'POST'])
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


@app.route('/student//verify-2fa', methods=['GET', 'POST'])
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

# ========================================
# WEB DEVELOPMENT COURSE ROUTES
# ========================================


@app.route('/student/web-development-overview')
@login_required
def web_development_overview():
    return render_template('web-development-course/web_development_overview.html',
                           title='Web Development'
                           )


@app.route('/student/web-development/chapter-1', methods=['GET', 'POST'])
@login_required
def web_development_chapter_1():
    page = request.args.get('page', 1, type=int)
    comments = WebDevChapter1Comment.query.order_by(WebDevChapter1Comment.timestamp.desc()).paginate(
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
                                _anchor='comments'
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
    return render_template('web-development-course/web_development_chapter_1.html',
                           title='Chapter 1: Introduction to Web Development',
                           form=form,
                           objectives_form=objectives_form,
                           comments=comments.items,
                           next_url=next_url,
                           prev_url=prev_url,
                           all_comments=all_comments
                           )


@app.route('/student/web-development/chapter-1/objectives-status')
@login_required
def web_development_chapter_1_objectives_status():
    page = request.args.get('page', 1, type=int)
    objectives = WebDevChapter1Objectives.query.order_by(WebDevChapter1Objectives.timestamp.desc()).paginate(
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
    return render_template('web-development-course/chapter_1_objectives_status.html',
                           title='Chapter 1: Achievement Status',
                           objectives=objectives.items,
                           next_url=next_url,
                           prev_url=prev_url
                           )


@app.route('/student/web-development/chapter-2', methods=['GET', 'POST'])
@login_required
def web_development_chapter_2():
    form = CommentForm()
    return render_template('web-development-course/web_development_chapter_2.html',
                           title='Chapter 2: What is HTML?',
                           form=form
                           )

# ========================================
# END OF WEB DEVELOPMENT COURSE ROUTES
# ========================================
