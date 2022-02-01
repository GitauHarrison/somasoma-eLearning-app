from app import db
from app.student import bp
from flask import render_template, redirect, url_for, flash, request,\
    current_app, jsonify
from app.student.forms import CommentForm, EditProfileForm,\
    ChapterObjectivesForm, QuizForm, Chapter1Quiz1OptionsForm,\
    EmptyForm, Chapter1Quiz2OptionsForm, Chapter1Quiz3OptionsForm,\
    Chapter1Quiz4OptionsForm
from app.teacher.forms import PrivateMessageForm
from app.models import ChapterQuiz, TableOfContents, WebDevChapter1Comment,\
    CommunityComment, WebDevChapter1Objectives, WebDevChapter1Quiz,\
    WebDevChapter1Quiz1Options, Student, WebDevelopmentOverview, Chapter,\
    Teacher, WebDevChapter1Quiz2Options,\
    WebDevChapter1Quiz3Options, WebDevChapter1Quiz4Options, StudentMessage,\
    StudentNotification
from app.student.email import send_flask_chapter_1_comment_email
from flask_login import current_user, login_required
from datetime import datetime


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.student_last_seen = datetime.utcnow()
        db.session.commit()


# Dashboard routes


@bp.route('/dashboard/enrolled-courses')
@login_required
def dashboard_enrolled_courses():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    return render_template(
        'student/enrolled_courses.html',
        title='Enrolled Courses',
        student=student
        )


@bp.route('/dashboard/live-class')
@login_required
def dashboard_live_class():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    return render_template(
        'student/live_class.html',
        title='Live Class',
        student=student
        )


@bp.route('/dashboard/quizzes')
@login_required
def dashboard_quizzes():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    return render_template(
        'student/quizzes.html',
        title='General Course Quizzes',
        student=student
        )


@bp.route('/dashboard/explore-student-community')
@login_required
def dashboard_explore_student_community():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    # Explore student community comments form
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = CommunityComment(
            body=comment_form.comment.data,
            author=current_user
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('student.dashboard_student'))
    # Explore student community comments
    page = request.args.get('page', 1, type=int)
    comments = CommunityComment.query.order_by(
        CommunityComment.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
                    'student.dashboard_explore_student_community',
                    page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'student.dashboard_explore_student_community',
        page=comments.prev_num) \
        if comments.has_prev else None
    return render_template(
        'student/explore_student_community.html',
        title='Explore Student Community',
        student=student,
        comment_form=comment_form,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url
        )


@bp.route('/dashboard/my-community')
@login_required
def dashboard_my_community():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    # My community comments form
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = CommunityComment(
            body=comment_form.comment.data,
            author=current_user
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('student.dashboard_student'))
    # My community comments
    page = request.args.get('page', 1, type=int)
    comments = CommunityComment.query.filter_by(
        author=current_user
        ).order_by(
        CommunityComment.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    # My community comments
    my_comments = current_user.followed_comments().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
                    'student.dashboard_student',
                    page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'student.dashboard_student',
        page=comments.prev_num) \
        if comments.has_prev else None
    return render_template(
        'student/my_community.html',
        title='My Community',
        student=student,
        comment_form=comment_form,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,
        my_comments=my_comments.items
        )


@bp.route('/dashboard/account')
@login_required
def dashboard_account():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    return render_template(
        'student/account.html',
        title='Account',
        student=student
        )


@bp.route('/dashboard/analytics')
@login_required
def dashboard_analytics():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()

    # Dsiplaying the chapter
    course_chapters = Chapter.query.filter_by(
        allowed_status=True).order_by(
            Chapter.timestamp.asc())

    # Calculate the number of objectives achieved
    all_objectives = student.webdev_chapter1_objectives.order_by(
        WebDevChapter1Objectives.timestamp.desc()).all()
    objectives_list = []
    num_of_true_status = 0
    for objective in all_objectives:
        objectives_list.append(str(objective.objective_1))
        objectives_list.append(str(objective.objective_2))
        objectives_list.append(str(objective.objective_3))
        objectives_list.append(str(objective.objective_4))
        objectives_list.append(str(objective.objective_5))
    num_of_true_status = objectives_list[-5:].count("True")
    try:
        percentage_achieved = round(
            (num_of_true_status / len(objectives_list)) * 100, 2)
    except ZeroDivisionError:
        percentage_achieved = 0

    # Calculate total score
    quiz_1_score = 0
    quiz_1_answers_list = []
    quiz_1_answer = WebDevChapter1Quiz1Options.query.all()
    for answer in quiz_1_answer:
        quiz_1_answers_list.append(answer.answer)
    student_latest_answer_quiz_1 = len(quiz_1_answers_list) - 1
    if quiz_1_answers_list[student_latest_answer_quiz_1].lower() == "to display content in a webpage":
        quiz_1_score += 1
    else:
        quiz_1_score += 0

    quiz_2_score = 0
    quiz_2_answers_list = []
    quiz_2_answer = WebDevChapter1Quiz2Options.query.all()
    for answer in quiz_2_answer:
        quiz_2_answers_list.append(answer.answer)
    student_latest_answer_quiz_2 = len(quiz_2_answers_list) - 1
    if quiz_2_answers_list[student_latest_answer_quiz_2].lower() == "to style the contents of a webpage":
        quiz_2_score += 1
    else:
        quiz_2_score += 0

    quiz_3_score = 0
    quiz_3_answers_list = []
    quiz_3_answer = WebDevChapter1Quiz3Options.query.all()
    for answer in quiz_3_answer:
        quiz_3_answers_list.append(answer.answer)
    student_latest_answer_quiz_3 = len(quiz_3_answers_list) - 1
    if quiz_3_answers_list[student_latest_answer_quiz_3].lower() == "to create a database":
        quiz_3_score += 1
    else:
        quiz_3_score += 0

    quiz_4_score = 0
    quiz_4_answers_list = []
    quiz_4_answer = WebDevChapter1Quiz4Options.query.all()
    for answer in quiz_4_answer:
        quiz_4_answers_list.append(answer.answer)
    student_latest_answer_quiz_4 = len(quiz_4_answers_list) - 1
    if quiz_4_answers_list[student_latest_answer_quiz_4].lower() == "to enhance the creation of an app":
        quiz_4_score += 1
    else:
        quiz_4_score += 0

    # Calculate percentage
    total_score = quiz_1_score + quiz_2_score + quiz_3_score + quiz_4_score
    try:
        quiz_total_score_percentage = round((total_score / 4) * 100, 2)
    except ZeroDivisionError:
        quiz_total_score_percentage = 0

    return render_template(
        'student/analytics.html',
        title='Analytics',
        student=student,
        percentage_achieved=percentage_achieved,
        course_chapters=course_chapters,
        quiz_total_score_percentage=quiz_total_score_percentage
        )

# Profile routes


@bp.route('/profile/<student_full_name>')
@login_required
def profile_student(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name
        ).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = student.comments.order_by(
        CommunityComment.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'student.dashboard_explore_student_community',
        student_full_name=student_full_name,
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'student.dashboard_explore_student_community',
        student_full_name=student_full_name,
        page=comments.prev_num) \
        if comments.has_prev else None
    form = EmptyForm()
    return render_template(
        'student/profile_student.html',
        title='Student Profile',
        student=student,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,
        form=form
    )


@bp.route('/profile/<student_full_name>/popup/')
@login_required
def student_profile_popup(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name
        ).first()
    form = EmptyForm()
    return render_template(
        'student/profile_popup.html',
        student=student,
        title='Student Profile',
        form=form
        )


@bp.route('/edit-profile', methods=['GET', 'POST'])
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
        return redirect(url_for('student.dashboard_student'))
    elif request.method == 'GET':
        form.email.data = current_user.student_email
        form.about_me.data = current_user.student_about_me
    return render_template(
        'student/edit_profile_student.html',
        title='Edit Student Profile',
        form=form,
        student=student
    )


@bp.route('/send-message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    student = Student.query.filter_by(
        student_full_name=recipient).first_or_404()
    form = PrivateMessageForm()
    if form.validate_on_submit():
        msg = StudentMessage(
            author=current_user,
            recipient=student,
            body=form.message.data
        )
        db.session.add(msg)
        student.add_notification(
            'unread_message_count', student.new_messages())
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for(
            'student.send_message',
            recipient=recipient)
        )
    return render_template(
        'student/private_messages/send_messages.html',
        title='Send Private Message',
        form=form,
        student=student,
        recipient=recipient
    )


@bp.route('/view-messages')
@login_required
def view_messages():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first_or_404()
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        StudentMessage.timestamp.desc()
        ).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'student.view_messages',
        page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for(
        'student.view_messages',
        page=messages.prev_num) \
        if messages.has_prev else None
    form = EmptyForm()
    return render_template(
        'student/private_messages/view_messages.html',
        title='View Private Messages',
        messages=messages.items,
        next_url=next_url,
        prev_url=prev_url,
        form=form,
        student=student
    )


@bp.route('/student-notications')
@login_required
def student_notifications():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first_or_404()
    since = request.args.get('since', 0.0, type=float)
    notifications = student.notifications.filter(
        StudentNotification.timestamp > since).order_by(
        StudentNotification.timestamp.asc())
    return jsonify([{
        'student_full_name': n.student_full_name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])

# Followership routes


@bp.route('/follow/<student_full_name>', methods=['POST'])
@login_required
def follow_student(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name
        ).first()
    form = EmptyForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(
            student_full_name=student_full_name
            ).first()
        if student is None:
            flash(f'User {student_full_name} not found')
            return redirect(url_for('student.dashboard_student'))
        if student == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for(
                'student.profile_student',
                student_full_name=student_full_name
                )
            )
        current_user.follow(student)
        db.session.commit()
        flash(f'You are following {student.student_full_name}!')
        return redirect(url_for(
            'student.profile_student',
            student_full_name=student_full_name
            )
        )
    else:
        return redirect(url_for('student.dashboard_student'))


@bp.route('/unfollow/<student_full_name>', methods=['POST'])
@login_required
def unfollow_student(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name
        ).first()
    form = EmptyForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(
            student_full_name=student_full_name
            ).first()
        if student is None:
            flash(f'User {student_full_name} not found')
            return redirect(url_for('student.dashboard_student'))
        if student == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for(
                'student.profile_student',
                student_full_name=student_full_name
                )
            )
        current_user.unfollow(student)
        db.session.commit()
        flash(f'You are not following {student.student_full_name}!')
        return redirect(url_for(
            'student.profile_student',
            student_full_name=student_full_name
            )
        )
    else:
        return redirect(url_for('student.dashboard_student'))

# End of followership routes

# ========================================
# WEB DEVELOPMENT COURSE ROUTES
# ========================================

# Overview


@bp.route('/web-development-overview')
@login_required
def web_development_overview():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    allowed_course_overview = WebDevelopmentOverview.query.filter_by(
        allowed_status=True).order_by(
            WebDevelopmentOverview.timestamp.desc()
            ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)

    # Table of contents
    all_toc = TableOfContents.query.filter_by(
        title=student.student_course).order_by(
            TableOfContents.timestamp.asc()
            ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    return render_template(
        'student/web-development-course/web_development_overview.html',
        title='Web Development',
        student=student,
        allowed_course_overview=allowed_course_overview.items,
        all_toc=all_toc.items
        )

# Chapters


@bp.route('/web-development/chapter-1', methods=['GET', 'POST'])
@login_required
def web_development_chapter_1():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    teachers = Teacher.query.all()
    page = request.args.get('page', 1, type=int)

    # Table of Contents
    all_toc = TableOfContents.query.filter_by(
        title=student.student_course).order_by(
            TableOfContents.timestamp.asc()).paginate(
                page,
                current_app.config['POSTS_PER_PAGE'],
                False
                )

    # Dsiplaying the chapter
    course_chapters = Chapter.query.filter_by(
        allowed_status=True).order_by(
            Chapter.timestamp.asc()).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)

    # Chapter Comment form
    form = CommentForm()
    if form.validate_on_submit():
        comment = WebDevChapter1Comment(
            body=form.comment.data,
            author=current_user
        )
        db.session.add(comment)
        db.session.commit()
        for teacher in teachers:
            if teacher.teacher_course == student.student_course:
                send_flask_chapter_1_comment_email(teacher)
        flash('You will receive an email when your comment is approved.')
        return redirect(url_for(
            'student.web_development_chapter_1',
            _anchor='comments',
            student=student,
            title='Hello World',
            )
        )

    # Display student comments
    comments = WebDevChapter1Comment.query.filter_by(
        allowed_status=True).order_by(
            WebDevChapter1Comment.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'student.web_development_chapter_1',
        _anchor="comments",
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'student.web_development_chapter_1',
        _anchor='comments',
        page=comments.prev_num) \
        if comments.has_prev else None
    all_comments = len(WebDevChapter1Comment.query.filter_by(
        allowed_status=True).all()
        )

    # Chapter Objectives
    objectives_form = ChapterObjectivesForm()
    if objectives_form.validate_on_submit():
        objectives = WebDevChapter1Objectives(
            objective_1=objectives_form.objective_1.data,
            objective_2=objectives_form.objective_2.data,
            objective_3=objectives_form.objective_3.data,
            objective_4=objectives_form.objective_4.data,
            objective_5=objectives_form.objective_5.data,
            author=student
        )
        db.session.add(objectives)
        db.session.commit()
        flash('Your response has been saved')
        return redirect(url_for(
            'student.web_development_chapter_1',
            student_full_name=student.student_full_name,
            _anchor='objectives'
        ))

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
    num_of_true_status = objectives_list.count(True)
    try:
        percentage_achieved = round(
            (num_of_true_status / len(objectives_list)) * 100, 2
        )
    except ZeroDivisionError:
        percentage_achieved = 0
    # End of Calculate the number of objectives achieved

    return render_template(
        'student/web-development-course/web_development_chapter_1.html',
        title='Chapter 1: Introduction to Web Development',
        form=form,
        objectives_form=objectives_form,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,
        all_comments=all_comments,
        student=student,

        # Chapter
        course_chapters=course_chapters.items,

        # Table of Contents
        all_toc=all_toc.items,

        # Objectives achieved
        percentage_achieved=percentage_achieved,
        )


@bp.route('/web-development/chapter-2', methods=['GET', 'POST'])
@login_required
def web_development_chapter_2():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    form = CommentForm()
    return render_template(
        'student/web-development-course/web_development_chapter_2.html',
        title='Chapter 2: Working With Flask Templates',
        form=form,
        student=student
        )


@bp.route('/web-development/chapter-3', methods=['GET', 'POST'])
@login_required
def web_development_chapter_3():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    form = CommentForm()
    return render_template(
        'student/web-development-course/web_development_chapter_3.html',
        title='Chapter 3: Introduction to Web Forms',
        form=form,
        student=student
        )

# ===================================
# QUIZZES
# ===================================


@bp.route(
    '/web-development/chapter-1/quizzes/form',
    methods=['GET', 'POST']
    )
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
            'student.web_development_chapter_1_quizzes_form',
            student_full_name=student.student_full_name
        ))
    return render_template(
        'student/quizzes-forms/quiz_type_1.html',
        title='Quiz Type 1',
        student=student,
        form=form
        )

# Chhapter 1 quiz 1


@bp.route(
    '/web-development/chapter-1/quiz-1',
    methods=['GET', 'POST']
    )
@login_required
def web_development_chapter_1_quiz_1():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    quizzes = ChapterQuiz.query.order_by(
        ChapterQuiz.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_QUIZ_PAGE'], False)

    # Quiz 1
    quiz_1_form = Chapter1Quiz1OptionsForm()
    if quiz_1_form.validate_on_submit():
        answer = WebDevChapter1Quiz1Options(
            answer=quiz_1_form.answer.data)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 1 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_chapter_1_quiz_2',
            student_full_name=student.student_full_name,
            _anchor="quiz_1",
        ))
    return render_template(
        'student/web-development-course/quizzes/chapter_1/quiz_1.html',
        title='Chapter 1: Quiz 1',
        student=student,
        quizzes=quizzes.items,
        quiz_1_form=quiz_1_form
        )

# Chhapter 1 quiz 2


@bp.route(
    '/web-development/chapter-1/quiz-2',
    methods=['GET', 'POST']
    )
@login_required
def web_development_chapter_1_quiz_2():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    quizzes = ChapterQuiz.query.order_by(
        ChapterQuiz.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_QUIZ_PAGE'], False)

    # Quiz 2
    quiz_2_form = Chapter1Quiz2OptionsForm()
    if quiz_2_form.validate_on_submit():
        answer = WebDevChapter1Quiz2Options(
            answer=quiz_2_form.answer.data)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 2 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_chapter_1_quiz_3',
            student_full_name=student.student_full_name,
            _anchor="quiz_2",
        ))
    return render_template(
        'student/web-development-course/quizzes/chapter_1/quiz_2.html',
        title='Chapter 1: Quiz 2',
        student=student,
        quizzes=quizzes.items,
        quiz_2_form=quiz_2_form
        )

# Chhapter 1 quiz 3


@bp.route(
    '/web-development/chapter-1/quiz-3',
    methods=['GET', 'POST']
    )
@login_required
def web_development_chapter_1_quiz_3():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    quizzes = ChapterQuiz.query.order_by(
        ChapterQuiz.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_QUIZ_PAGE'], False)

    # Quiz 3
    quiz_3_form = Chapter1Quiz3OptionsForm()
    if quiz_3_form.validate_on_submit():
        answer = WebDevChapter1Quiz3Options(
            answer=quiz_3_form.answer.data)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 3 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_chapter_1_quiz_4',
            student_full_name=student.student_full_name,
            _anchor="quiz_2",
        ))
    return render_template(
        'student/web-development-course/quizzes/chapter_1/quiz_3.html',
        title='Chapter 1: Quiz 3',
        student=student,
        quizzes=quizzes.items,
        quiz_3_form=quiz_3_form
        )

# Chhapter 1 quiz 4


@bp.route(
    '/web-development/chapter-1/quiz-4',
    methods=['GET', 'POST']
    )
@login_required
def web_development_chapter_1_quiz_4():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    quizzes = ChapterQuiz.query.order_by(
        ChapterQuiz.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_QUIZ_PAGE'], False)

    # Quiz 4
    quiz_4_form = Chapter1Quiz4OptionsForm()
    if quiz_4_form.validate_on_submit():
        answer = WebDevChapter1Quiz4Options(
            answer=quiz_4_form.answer.data)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 4 answer have been added!',
              'Congratulations! You have completed the chapter 1 quiz!')
        return redirect(url_for(
            'student.web_development_chapter_1_total_score',
            student_full_name=student.student_full_name,
        ))
    return render_template(
        'student/web-development-course/quizzes/chapter_1/quiz_4.html',
        title='Chapter 1: Quiz 4',
        student=student,
        quizzes=quizzes.items,
        quiz_4_form=quiz_4_form
        )

# Chapter 1 total score


@bp.route(
    '/web-development/chapter-1/total-score',
    methods=['GET', 'POST']
    )
@login_required
def web_development_chapter_1_total_score():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    quizzes = ChapterQuiz.query.order_by(
        ChapterQuiz.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_QUIZ_PAGE'], False)

    # Calculate total score
    quiz_1_score = 0
    quiz_1_answers_list = []
    quiz_1_answer = WebDevChapter1Quiz1Options.query.all()
    for answer in quiz_1_answer:
        quiz_1_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_1 = len(quiz_1_answers_list) - 1
        if quiz_1_answers_list[student_latest_answer_quiz_1].lower() == "pip3 install flask":
            quiz_1_score += 1
        else:
            quiz_1_score += 0
    except IndexError:
        quiz_1_score += 0

    quiz_2_score = 0
    quiz_2_answers_list = []
    quiz_2_answer = WebDevChapter1Quiz2Options.query.all()
    for answer in quiz_2_answer:
        quiz_2_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_2 = len(quiz_2_answers_list) - 1
        if quiz_2_answers_list[student_latest_answer_quiz_2].lower() == "python":
            quiz_2_score += 1
        else:
            quiz_2_score += 0
    except IndexError:
        quiz_2_score += 0

    quiz_3_score = 0
    quiz_3_answers_list = []
    quiz_3_answer = WebDevChapter1Quiz3Options.query.all()
    for answer in quiz_3_answer:
        quiz_3_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_3 = len(quiz_3_answers_list) - 1
        if quiz_3_answers_list[student_latest_answer_quiz_3].lower() == "keeping the core simple but extensible":
            quiz_3_score += 1
        else:
            quiz_3_score += 0
    except IndexError:
        quiz_3_score += 0

    quiz_4_score = 0
    quiz_4_answers_list = []
    quiz_4_answer = WebDevChapter1Quiz4Options.query.all()
    for answer in quiz_4_answer:
        quiz_4_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_4 = len(quiz_4_answers_list) - 1
        if quiz_4_answers_list[student_latest_answer_quiz_4].lower() == "using the command flask run":
            quiz_4_score += 1
        else:
            quiz_4_score += 0
    except IndexError:
        quiz_4_score += 0

    # Calculate percentage
    total_score = quiz_1_score + quiz_2_score + quiz_3_score + quiz_4_score
    try:
        total_score_percentage = round((total_score / 4) * 100, 2)
    except ZeroDivisionError:
        total_score_percentage = 0

    return render_template(
        'student/web-development-course/quizzes/chapter_1/total_score.html',
        title='Chapter 1: Total Score',
        student=student,
        quizzes=quizzes.items,

        quiz_1_answers_list=quiz_1_answers_list,
        quiz_2_answers_list=quiz_2_answers_list,
        quiz_3_answers_list=quiz_3_answers_list,
        quiz_4_answers_list=quiz_4_answers_list,

        student_latest_answer_quiz_1=student_latest_answer_quiz_1,
        student_latest_answer_quiz_2=student_latest_answer_quiz_2,
        student_latest_answer_quiz_3=student_latest_answer_quiz_3,
        student_latest_answer_quiz_4=student_latest_answer_quiz_4,

        quiz_1_score=quiz_1_score,
        quiz_2_score=quiz_2_score,
        quiz_3_score=quiz_3_score,
        quiz_4_score=quiz_4_score,
        total_score=total_score,
        total_score_percentage=total_score_percentage
        )

# ========================================
# END OF WEB DEVELOPMENT COURSE ROUTES
# ========================================
