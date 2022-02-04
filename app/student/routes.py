from app import db
from app.student import bp
from flask import render_template, redirect, url_for, flash, request,\
    current_app, jsonify
from app.student.forms import CommentForm, EditProfileForm,\
    ChapterObjectivesForm, Chapter1Quiz1OptionsForm,\
    EmptyForm, Chapter1Quiz2OptionsForm, Chapter1Quiz3OptionsForm,\
    Chapter1Quiz4OptionsForm, Chapter2Quiz1OptionsForm,\
    Chapter2Quiz2OptionsForm, Chapter2Quiz3OptionsForm,\
    Chapter2Quiz4OptionsForm, Chapter2Quiz5OptionsForm,\
    Chapter1Quiz5OptionsForm, Chapter3Quiz1OptionsForm,\
    Chapter3Quiz2OptionsForm, Chapter3Quiz3OptionsForm,\
    Chapter3Quiz4OptionsForm, Chapter3Quiz5OptionsForm,\
    GeneralQuiz1Form, GeneralQuiz2Form, GeneralQuiz3Form,\
    GeneralQuiz4Form, GeneralQuiz5Form, GeneralQuiz6Form,\
    GeneralQuiz7Form, GeneralQuiz8Form, GeneralQuiz9Form,\
    GeneralQuiz10Form
from app.teacher.forms import PrivateMessageForm
from app.models import ChapterQuiz, TableOfContents, WebDevChapter1Comment,\
    CommunityComment, WebDevChapter1Objectives, WebDevChapter1Quiz,\
    WebDevChapter1Quiz1Options, Student, WebDevelopmentOverview, Chapter,\
    Teacher, WebDevChapter1Quiz2Options,\
    WebDevChapter1Quiz3Options, WebDevChapter1Quiz4Options, StudentMessage,\
    StudentNotification, WebDevChapter2Comment, WebDevChapter2Objectives,\
    WebDevChapter2Quiz1Options, WebDevChapter2Quiz2Options,\
    WebDevChapter2Quiz3Options, WebDevChapter2Quiz4Options, \
    WebDevChapter1Quiz5Options, WebDevChapter2Quiz5Options,\
    WebDevChapter3Comment, WebDevChapter3Objectives, \
    WebDevChapter3Quiz1Options, WebDevChapter3Quiz2Options,\
    WebDevChapter3Quiz3Options, WebDevChapter3Quiz4Options,\
    WebDevChapter3Quiz5Options, GeneralMultipleChoicesQuiz,\
    GeneralMultipleChoicesAnswer1, GeneralMultipleChoicesAnswer2,\
    GeneralMultipleChoicesAnswer3, GeneralMultipleChoicesAnswer4,\
    GeneralMultipleChoicesAnswer5, GeneralMultipleChoicesAnswer6,\
    GeneralMultipleChoicesAnswer7, GeneralMultipleChoicesAnswer8,\
    GeneralMultipleChoicesAnswer9, GeneralMultipleChoicesAnswer10
from app.student.email import send_flask_chapter_1_comment_email, \
    send_flask_chapter_2_comment_email, send_flask_chapter_3_comment_email
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
        allowed_status=True).all()

    # CHAPTER 1: Calculate the number of objectives achieved
    all_objectives = student.webdev_chapter1_objectives.all()
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
            (num_of_true_status / len(objectives_list[-5:])) * 100, 2
        )
    except ZeroDivisionError:
        percentage_achieved = 0
    # End of Calculate the number of objectives achieved

    # CHAPTER 2: Calculate the number of objectives achieved
    all_objectives_chapter_2 = student.webdev_chapter2_objectives.all()
    objectives_list_chapter_2 = []
    num_of_true_status_chapter_2 = 0
    for objective in all_objectives_chapter_2:
        objectives_list_chapter_2.append(str(objective.objective_1))
        objectives_list_chapter_2.append(str(objective.objective_2))
        objectives_list_chapter_2.append(str(objective.objective_3))
        objectives_list_chapter_2.append(str(objective.objective_4))
        objectives_list_chapter_2.append(str(objective.objective_5))
    num_of_true_status_chapter_2 = objectives_list_chapter_2[-5:].count("True")
    try:
        percentage_achieved_chapter_2 = round(
            (num_of_true_status_chapter_2 /
                len(objectives_list_chapter_2[-5:])) * 100, 2)
    except ZeroDivisionError:
        percentage_achieved_chapter_2 = 0
    # End of Calculate the number of objectives achieved

    # CHAPTER 3: Calculate the number of objectives achieved
    all_objectives_chapter_3 = student.webdev_chapter3_objectives.all()
    objectives_list_chapter_3 = []
    num_of_true_status_chapter_3 = 0
    for objective in all_objectives_chapter_3:
        objectives_list_chapter_3.append(str(objective.objective_1))
        objectives_list_chapter_3.append(str(objective.objective_2))
        objectives_list_chapter_3.append(str(objective.objective_3))
        objectives_list_chapter_3.append(str(objective.objective_4))
        objectives_list_chapter_3.append(str(objective.objective_5))
    num_of_true_status_chapter_3 = objectives_list_chapter_3[-5:].count("True")
    try:
        percentage_achieved_chapter_3 = round(
            (num_of_true_status_chapter_3 /
                len(objectives_list_chapter_3[-5:])) * 100, 2)
    except ZeroDivisionError:
        percentage_achieved_chapter_3 = 0
    # End of Calculate the number of objectives achieved

    # CHAPTER 1: Calculate total score
    quiz_1_score = 0
    quiz_1_answers_list = []
    quiz_1_answer = student.webdev_chapter1_quiz_1_options.all()
    for answer in quiz_1_answer:
        quiz_1_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_1 = len(quiz_1_answers_list) - 1
        if quiz_1_answers_list[student_latest_answer_quiz_1].lower() == \
                "pip3 install flask":
            quiz_1_score += 1
        else:
            quiz_1_score += 0
    except IndexError:
        quiz_1_score += 0

    quiz_2_score = 0
    quiz_2_answers_list = []
    quiz_2_answer = student.webdev_chapter1_quiz_2_options.all()
    for answer in quiz_2_answer:
        quiz_2_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_2 = len(quiz_2_answers_list) - 1
        if quiz_2_answers_list[student_latest_answer_quiz_2].lower() == \
                "python":
            quiz_2_score += 1
        else:
            quiz_2_score += 0
    except IndexError:
        quiz_2_score += 0

    quiz_3_score = 0
    quiz_3_answers_list = []
    quiz_3_answer = student.webdev_chapter1_quiz_3_options.all()
    for answer in quiz_3_answer:
        quiz_3_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_3 = len(quiz_3_answers_list) - 1
        if quiz_3_answers_list[student_latest_answer_quiz_3].lower() == \
                "keeping the core simple but extensible":
            quiz_3_score += 1
        else:
            quiz_3_score += 0
    except IndexError:
        quiz_3_score += 0

    quiz_4_score = 0
    quiz_4_answers_list = []
    quiz_4_answer = student.webdev_chapter1_quiz_4_options.all()
    for answer in quiz_4_answer:
        quiz_4_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_4 = len(quiz_4_answers_list) - 1
        if quiz_4_answers_list[student_latest_answer_quiz_4].lower() == \
                "using the command flask run":
            quiz_4_score += 1
        else:
            quiz_4_score += 0
    except IndexError:
        quiz_4_score += 0

    quiz_5_score = 0
    quiz_5_answers_list = []
    quiz_5_answer = student.webdev_chapter1_quiz_5_options.all()
    for answer in quiz_5_answer:
        quiz_5_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_5 = len(quiz_5_answers_list) - 1
        if quiz_5_answers_list[student_latest_answer_quiz_5].lower() == \
                "view functions":
            quiz_5_score += 1
        else:
            quiz_5_score += 0
    except IndexError:
        quiz_5_score += 0

    # CHAPTER 1: Calculate percentage
    total_score = quiz_1_score + quiz_2_score + quiz_3_score + quiz_4_score + \
        quiz_5_score
    try:
        total_score_percentage = round((total_score / 5) * 100, 2)
    except ZeroDivisionError:
        total_score_percentage = 0

    # CHAPTER 2: Calculate total score
    quiz_1_score_chapter_2 = 0
    quiz_1_answers_list_chapter_2 = []
    quiz_1_answer_chapter_2 = student.webdev_chapter2_quiz_1_options.all()
    for answer in quiz_1_answer_chapter_2:
        quiz_1_answers_list_chapter_2.append(answer.answer)
    try:
        student_latest_answer_quiz_1_chapter_2 = len(quiz_1_answers_list_chapter_2) - 1
        if quiz_1_answers_list_chapter_2[student_latest_answer_quiz_1_chapter_2].lower() == "to display content":
            quiz_1_score_chapter_2 += 1
        else:
            quiz_1_score_chapter_2 += 0
    except IndexError:
        quiz_1_score_chapter_2 += 0

    quiz_2_score_chapter_2 = 0
    quiz_2_answers_list_chapter_2 = []
    quiz_2_answer_chapter_2 = student.webdev_chapter2_quiz_2_options.all()
    for answer in quiz_2_answer_chapter_2:
        quiz_2_answers_list_chapter_2.append(answer.answer)
    try:
        student_latest_answer_quiz_2_chapter_2 = len(quiz_2_answers_list_chapter_2) - 1
        if quiz_2_answers_list_chapter_2[student_latest_answer_quiz_2_chapter_2].lower() == "html":
            quiz_2_score_chapter_2 += 1
        else:
            quiz_2_score_chapter_2 += 0
    except IndexError:
        quiz_2_score_chapter_2 += 0

    quiz_3_score_chapter_2 = 0
    quiz_3_answers_list_chapter_2 = []
    quiz_3_answer_chapter_2 = student.webdev_chapter2_quiz_3_options.all()
    for answer in quiz_3_answer_chapter_2:
        quiz_3_answers_list_chapter_2.append(answer.answer)
    try:
        student_latest_answer_quiz_3_chapter_2 = len(quiz_3_answers_list_chapter_2) - 1
        if quiz_3_answers_list_chapter_2[student_latest_answer_quiz_3_chapter_2].lower() == "jinja":
            quiz_3_score_chapter_2 += 1
        else:
            quiz_3_score_chapter_2 += 0
    except IndexError:
        quiz_3_score_chapter_2 += 0

    quiz_4_score_chapter_2 = 0
    quiz_4_answers_list_chapter_2 = []
    quiz_4_answer_chapter_2 = student.webdev_chapter2_quiz_4_options.all()
    for answer in quiz_4_answer_chapter_2:
        quiz_4_answers_list_chapter_2.append(answer.answer)
    try:
        student_latest_answer_quiz_4_chapter_2 = len(quiz_4_answers_list_chapter_2) - 1
        if quiz_4_answers_list_chapter_2[student_latest_answer_quiz_4_chapter_2].lower() == "view functions":
            quiz_4_score_chapter_2 += 1
        else:
            quiz_4_score_chapter_2 += 0
    except IndexError:
        quiz_4_score_chapter_2 += 0

    quiz_5_score_chapter_2 = 0
    quiz_5_answers_list_chapter_2 = []
    quiz_5_answer_chapter_2 = student.webdev_chapter2_quiz_5_options.all()
    for answer in quiz_5_answer_chapter_2:
        quiz_5_answers_list_chapter_2.append(answer.answer)
    try:
        student_latest_answer_quiz_5_chapter_2 = len(quiz_5_answers_list_chapter_2) - 1
        if quiz_5_answers_list_chapter_2[student_latest_answer_quiz_5_chapter_2].lower() == "view functions":
            quiz_5_score_chapter_2 += 1
        else:
            quiz_5_score_chapter_2 += 0
    except IndexError:
        quiz_5_score_chapter_2 += 0

    # CHAPTER 2: Calculate percentage
    total_score_chapter_2 = quiz_1_score_chapter_2 + quiz_2_score_chapter_2 + \
        quiz_3_score_chapter_2 + quiz_4_score_chapter_2 + quiz_5_score_chapter_2
    try:
        total_score_percentage_chapter_2 = round((total_score_chapter_2 / 5) * 100, 2)
    except ZeroDivisionError:
        total_score_percentage_chapter_2 = 0

    # CHAPTER 3: Calculate total score
    quiz_1_score_chapter_3 = 0
    quiz_1_answers_list_chapter_3 = []
    quiz_1_answer_chapter_3 = student.webdev_chapter3_quiz_1_options.all()
    for answer in quiz_1_answer_chapter_3:
        quiz_1_answers_list_chapter_3.append(answer.answer)
    try:
        student_latest_answer_quiz_1_chapter_3 = len(quiz_1_answers_list_chapter_3) - 1
        if quiz_1_answers_list_chapter_3[student_latest_answer_quiz_1_chapter_3].lower() == "to collect user data":
            quiz_1_score_chapter_3 += 1
        else:
            quiz_1_score_chapter_3 += 0
    except IndexError:
        quiz_1_score_chapter_3 += 0

    quiz_2_score_chapter_3 = 0
    quiz_2_answers_list_chapter_3 = []
    quiz_2_answer_chapter_3 = student.webdev_chapter3_quiz_2_options.all()
    for answer in quiz_2_answer_chapter_3:
        quiz_2_answers_list_chapter_3.append(answer.answer)
    try:
        student_latest_answer_quiz_2_chapter_3 = len(quiz_2_answers_list_chapter_3) - 1
        if quiz_2_answers_list_chapter_3[student_latest_answer_quiz_2_chapter_3].lower() == "flask-wtf":
            quiz_2_score_chapter_3 += 1
        else:
            quiz_2_score_chapter_3 += 0
    except IndexError:
        quiz_2_score_chapter_3 += 0

    quiz_3_score_chapter_3 = 0
    quiz_3_answers_list_chapter_3 = []
    quiz_3_answer_chapter_3 = student.webdev_chapter3_quiz_3_options.all()
    for answer in quiz_3_answer_chapter_3:
        quiz_3_answers_list_chapter_3.append(answer.answer)
    try:
        student_latest_answer_quiz_3_chapter_3 = len(quiz_3_answers_list_chapter_3) - 1
        if quiz_3_answers_list_chapter_3[student_latest_answer_quiz_3_chapter_3].lower() == "validationerror":
            quiz_3_score_chapter_3 += 1
        else:
            quiz_3_score_chapter_3 += 0
    except IndexError:
        quiz_3_score_chapter_3 += 0

    quiz_4_score_chapter_3 = 0
    quiz_4_answers_list_chapter_3 = []
    quiz_4_answer_chapter_3 = student.webdev_chapter3_quiz_4_options.all()
    for answer in quiz_4_answer_chapter_3:
        quiz_4_answers_list_chapter_3.append(answer.answer)
    try:
        student_latest_answer_quiz_4_chapter_3 = len(quiz_4_answers_list_chapter_3) - 1
        if quiz_4_answers_list_chapter_3[student_latest_answer_quiz_4_chapter_3].lower() == ".env":
            quiz_4_score_chapter_3 += 1
        else:
            quiz_4_score_chapter_3 += 0
    except IndexError:
        quiz_4_score_chapter_3 += 0

    quiz_5_score_chapter_3 = 0
    quiz_5_answers_list_chapter_3 = []
    quiz_5_answer_chapter_3 = student.webdev_chapter3_quiz_5_options.all()
    for answer in quiz_5_answer_chapter_3:
        quiz_5_answers_list_chapter_3.append(answer.answer)
    try:
        student_latest_answer_quiz_5_chapter_3 = len(quiz_5_answers_list_chapter_3) - 1
        if quiz_5_answers_list_chapter_3[student_latest_answer_quiz_5_chapter_3].lower() == "flask bootsrap":
            quiz_5_score_chapter_3 += 1
        else:
            quiz_5_score_chapter_3 += 0
    except IndexError:
        quiz_5_score_chapter_3 += 0

    # CHAPTER 3: Calculate percentage
    total_score_chapter_3 = quiz_1_score_chapter_3 + quiz_2_score_chapter_3 + \
        quiz_3_score_chapter_3 + quiz_4_score_chapter_3 + \
        quiz_5_score_chapter_3
    try:
        total_score_percentage_chapter_3 = round((total_score_chapter_3 / 5) * 100, 2)
    except ZeroDivisionError:
        total_score_percentage_chapter_3 = 0

    # === General multi-choice questions ===

    # Calculate total score
    multi_choice_quiz_1_score = 0
    multi_choice_quiz_1_answers_list = []
    multi_choice_quiz_1_answer = student.general_multi_choice_answer_1.all()
    for answer in multi_choice_quiz_1_answer:
        multi_choice_quiz_1_answers_list.append(answer.answer)
    try:
        multi_choice_student_latest_answer_quiz_1 = len(multi_choice_quiz_1_answers_list) - 1
        if multi_choice_quiz_1_answers_list[multi_choice_student_latest_answer_quiz_1].lower() == \
                "to collect user data":
            multi_choice_quiz_1_score += 1
        else:
            multi_choice_quiz_1_score += 0
    except IndexError:
        multi_choice_quiz_1_score += 0

    multi_choice_quiz_2_score = 0
    multi_choice_quiz_2_answers_list = []
    multi_choice_quiz_2_answer = student.general_multi_choice_answer_2.all()
    for answer in multi_choice_quiz_2_answer:
        quiz_2_answers_list.append(answer.answer)
    try:
        multi_choice_student_latest_answer_quiz_2 = len(multi_choice_quiz_2_answers_list) - 1
        if multi_choice_quiz_2_answers_list[multi_choice_student_latest_answer_quiz_2].lower() == \
                "flask-wtf":
            multi_choice_quiz_2_score += 1
        else:
            multi_choice_quiz_2_score += 0
    except IndexError:
        multi_choice_quiz_2_score += 0

    multi_choice_quiz_3_score = 0
    multi_choice_quiz_3_answers_list = []
    multi_choice_quiz_3_answer = student.general_multi_choice_answer_3.all()
    for answer in multi_choice_quiz_3_answer:
        multi_choice_quiz_3_answers_list.append(answer.answer)
    try:
        multi_choice_student_latest_answer_quiz_3 = len(multi_choice_quiz_3_answers_list) - 1
        if multi_choice_quiz_3_answers_list[multi_choice_student_latest_answer_quiz_3].lower() == \
                "validationerror":
            multi_choice_quiz_3_score += 1
        else:
            multi_choice_quiz_3_score += 0
    except IndexError:
        multi_choice_quiz_3_score += 0

    multi_choice_quiz_4_score = 0
    multi_choice_quiz_4_answers_list = []
    multi_choice_quiz_4_answer = student.general_multi_choice_answer_4.all()
    for answer in multi_choice_quiz_4_answer:
        multi_choice_quiz_4_answers_list.append(answer.answer)
    try:
        multi_choice_student_latest_answer_quiz_4 = len(multi_choice_quiz_4_answers_list) - 1
        if multi_choice_quiz_4_answers_list[multi_choice_student_latest_answer_quiz_4].lower() == \
                ".env":
            multi_choice_quiz_4_score += 1
        else:
            multi_choice_quiz_4_score += 0
    except IndexError:
        multi_choice_quiz_4_score += 0

    multi_choice_quiz_5_score = 0
    multi_choice_quiz_5_answers_list = []
    multi_choice_quiz_5_answer = student.general_multi_choice_answer_5.all()
    for answer in multi_choice_quiz_5_answer:
        multi_choice_quiz_5_answers_list.append(answer.answer)
    try:
        multi_choice_student_latest_answer_quiz_5 = len(multi_choice_quiz_5_answers_list) - 1
        if multi_choice_quiz_5_answers_list[multi_choice_student_latest_answer_quiz_5].lower() == \
                "flask bootsrap":
            multi_choice_quiz_5_score += 1
        else:
            multi_choice_quiz_5_score += 0
    except IndexError:
        multi_choice_quiz_5_score += 0

    multi_choice_quiz_6_score = 0
    multi_choice_quiz_6_answers_list = []
    multi_choice_quiz_6_answer = student.general_multi_choice_answer_6.all()
    for answer in multi_choice_quiz_6_answer:
        multi_choice_quiz_6_answers_list.append(answer.answer)
    try:
        multi_choice_student_latest_answer_quiz_6 = len(multi_choice_quiz_6_answers_list) - 1
        if multi_choice_quiz_6_answers_list[multi_choice_student_latest_answer_quiz_6].lower() == \
                "flask bootsrap":
            multi_choice_quiz_6_score += 1
        else:
            multi_choice_quiz_6_score += 0
    except IndexError:
        multi_choice_quiz_6_score += 0

    multi_choice_quiz_7_score = 0
    multi_choice_quiz_7_answers_list = []
    multi_choice_quiz_7_answer = student.general_multi_choice_answer_7.all()
    for answer in multi_choice_quiz_7_answer:
        multi_choice_quiz_7_answers_list.append(answer.answer)
    try:
        multi_choice_student_latest_answer_quiz_7 = len(multi_choice_quiz_7_answers_list) - 1
        if multi_choice_quiz_7_answers_list[multi_choice_student_latest_answer_quiz_7].lower() == \
                "flask bootsrap":
            multi_choice_quiz_7_score += 1
        else:
            multi_choice_quiz_7_score += 0
    except IndexError:
        multi_choice_quiz_7_score += 0

    multi_choice_quiz_8_score = 0
    multi_choice_quiz_8_answers_list = []
    multi_choice_quiz_8_answer = student.general_multi_choice_answer_8.all()
    for answer in multi_choice_quiz_8_answer:
        multi_choice_quiz_8_answers_list.append(answer.answer)
    try:
        multi_choice_student_latest_answer_quiz_8 = len(multi_choice_quiz_8_answers_list) - 1
        if multi_choice_quiz_8_answers_list[multi_choice_student_latest_answer_quiz_8].lower() == \
                "flask bootsrap":
            multi_choice_quiz_8_score += 1
        else:
            multi_choice_quiz_8_score += 0
    except IndexError:
        multi_choice_quiz_8_score += 0

    multi_choice_quiz_9_score = 0
    multi_choice_quiz_9_answers_list = []
    multi_choice_quiz_9_answer = student.general_multi_choice_answer_9.all()
    for answer in multi_choice_quiz_9_answer:
        multi_choice_quiz_9_answers_list.append(answer.answer)
    try:
        multi_choice_student_latest_answer_quiz_9 = len(multi_choice_quiz_9_answers_list) - 1
        if multi_choice_quiz_9_answers_list[multi_choice_student_latest_answer_quiz_9].lower() == \
                "flask bootsrap":
            multi_choice_quiz_9_score += 1
        else:
            multi_choice_quiz_9_score += 0
    except IndexError:
        multi_choice_quiz_9_score += 0

    multi_choice_quiz_10_score = 0
    multi_choice_quiz_10_answers_list = []
    multi_choice_quiz_10_answer = student.general_multi_choice_answer_10.all()
    for answer in multi_choice_quiz_10_answer:
        multi_choice_quiz_10_answers_list.append(answer.answer)
    try:
        multi_choice_student_latest_answer_quiz_10 = len(multi_choice_quiz_10_answers_list) - 1
        if multi_choice_quiz_10_answers_list[multi_choice_student_latest_answer_quiz_10].lower() == \
                "flask bootsrap":
            multi_choice_quiz_10_score += 1
        else:
            multi_choice_quiz_10_score += 0
    except IndexError:
        multi_choice_quiz_10_score += 0

    # Calculate percentage
    multi_choice_total_score = multi_choice_quiz_1_score + multi_choice_quiz_2_score + \
        multi_choice_quiz_3_score + multi_choice_quiz_4_score + \
        multi_choice_quiz_5_score + multi_choice_quiz_6_score + \
        multi_choice_quiz_7_score + multi_choice_quiz_8_score + \
        multi_choice_quiz_9_score + multi_choice_quiz_10_score
    try:
        multi_choice_total_score_percentage = round((multi_choice_total_score / 10) * 100, 2)
    except ZeroDivisionError:
        multi_choice_total_score_percentage = 0

    # === End of multi-choice questions ===

    return render_template(
        'student/analytics.html',
        title='Analytics',
        student=student,
        course_chapters=course_chapters,

        # Chapter 1
        percentage_achieved=percentage_achieved,
        total_score_percentage=total_score_percentage,

        # Chapter 2
        percentage_achieved_chapter_2=percentage_achieved_chapter_2,
        total_score_percentage_chapter_2=total_score_percentage_chapter_2,

        # Chapter 3
        percentage_achieved_chapter_3=percentage_achieved_chapter_3,
        total_score_percentage_chapter_3=total_score_percentage_chapter_3,

        # Multi-choice questions
        multi_choice_total_score_percentage=multi_choice_total_score_percentage
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
        student_full_name=current_user.student_full_name).first()
    page = request.args.get('page', 1, type=int)
    allowed_course_overview = WebDevelopmentOverview.query.filter_by(
        allowed_status=True).order_by(
            WebDevelopmentOverview.timestamp.desc()).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)

    # Table of contents
    all_toc = TableOfContents.query.filter_by(
        title=student.student_course).order_by(
            TableOfContents.timestamp.asc()).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)

    # CHAPTER 1: Calculate the number of objectives achieved
    all_objectives = student.webdev_chapter1_objectives.all()
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
            (num_of_true_status / len(objectives_list[-5:])) * 100, 2
        )
    except ZeroDivisionError:
        percentage_achieved = 0
    # End of Calculate the number of objectives achieved

    # CHAPTER 2: Calculate the number of objectives achieved
    all_objectives_chapter_2 = student.webdev_chapter2_objectives.all()
    objectives_list_chapter_2 = []
    num_of_true_status_chapter_2 = 0
    for objective in all_objectives_chapter_2:
        objectives_list_chapter_2.append(str(objective.objective_1))
        objectives_list_chapter_2.append(str(objective.objective_2))
        objectives_list_chapter_2.append(str(objective.objective_3))
        objectives_list_chapter_2.append(str(objective.objective_4))
        objectives_list_chapter_2.append(str(objective.objective_5))
    num_of_true_status_chapter_2 = objectives_list_chapter_2[-5:].count("True")
    try:
        percentage_achieved_chapter_2 = round(
            (num_of_true_status_chapter_2 /
                len(objectives_list_chapter_2[-5:])) * 100, 2)
    except ZeroDivisionError:
        percentage_achieved_chapter_2 = 0
    # End of Calculate the number of objectives achieved

    # CHAPTER 3: Calculate the number of objectives achieved
    all_objectives_chapter_3 = student.webdev_chapter3_objectives.all()
    objectives_list_chapter_3 = []
    num_of_true_status_chapter_3 = 0
    for objective in all_objectives_chapter_3:
        objectives_list_chapter_3.append(str(objective.objective_1))
        objectives_list_chapter_3.append(str(objective.objective_2))
        objectives_list_chapter_3.append(str(objective.objective_3))
        objectives_list_chapter_3.append(str(objective.objective_4))
        objectives_list_chapter_3.append(str(objective.objective_5))
    num_of_true_status_chapter_3 = objectives_list_chapter_3[-5:].count("True")
    try:
        percentage_achieved_chapter_3 = round(
            (num_of_true_status_chapter_3 /
                len(objectives_list_chapter_3[-5:])) * 100, 2)
    except ZeroDivisionError:
        percentage_achieved_chapter_3 = 0
    # End of Calculate the number of objectives achieved

    return render_template(
        'student/web-development-course/web_development_overview.html',
        title='Web Development',
        student=student,
        allowed_course_overview=allowed_course_overview.items,
        all_toc=all_toc.items,

        # Chapter 1 objectives
        percentage_achieved=percentage_achieved,

        # Chapter 2 objectives
        percentage_achieved_chapter_2=percentage_achieved_chapter_2,

        # Chapter 3 objectives
        percentage_achieved_chapter_3=percentage_achieved_chapter_3
        )

# Chapters


@bp.route('/web-development/chapter-1', methods=['GET', 'POST'])
@login_required
def web_development_chapter_1():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    teachers = Teacher.query.all()
    page = request.args.get('page', 1, type=int)

    # Table of Contents
    all_toc = TableOfContents.query.filter_by(
        title=student.student_course).order_by(
            TableOfContents.timestamp.asc()).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)

    # Dsiplaying the chapter
    course_chapters = Chapter.query.filter_by(allowed_status=True).all()

    # Chapter Comment form
    form = CommentForm()
    if form.validate_on_submit():
        comment = WebDevChapter1Comment(
            body=form.comment.data, author=student)
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
            WebDevChapter1Comment.timestamp.desc()).paginate(
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
        allowed_status=True).all())

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
            _anchor='objectives'))

    # CHAPTER 1: Calculate the number of objectives achieved
    all_objectives = student.webdev_chapter1_objectives.all()
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
            (num_of_true_status / len(objectives_list[-5:])) * 100, 2
        )
    except ZeroDivisionError:
        percentage_achieved = 0
    # End of Calculate the number of objectives achieved

    # CHAPTER 2: Calculate the number of objectives achieved
    all_objectives_chapter_2 = student.webdev_chapter2_objectives.all()
    objectives_list_chapter_2 = []
    num_of_true_status_chapter_2 = 0
    for objective in all_objectives_chapter_2:
        objectives_list_chapter_2.append(str(objective.objective_1))
        objectives_list_chapter_2.append(str(objective.objective_2))
        objectives_list_chapter_2.append(str(objective.objective_3))
        objectives_list_chapter_2.append(str(objective.objective_4))
        objectives_list_chapter_2.append(str(objective.objective_5))
    num_of_true_status_chapter_2 = objectives_list_chapter_2[-5:].count("True")
    try:
        percentage_achieved_chapter_2 = round(
            (num_of_true_status_chapter_2 /
                len(objectives_list_chapter_2[-5:])) * 100, 2)
    except ZeroDivisionError:
        percentage_achieved_chapter_2 = 0
    # End of Calculate the number of objectives achieved

    # CHAPTER 3: Calculate the number of objectives achieved
    all_objectives_chapter_3 = student.webdev_chapter3_objectives.all()
    objectives_list_chapter_3 = []
    num_of_true_status_chapter_3 = 0
    for objective in all_objectives_chapter_3:
        objectives_list_chapter_3.append(str(objective.objective_1))
        objectives_list_chapter_3.append(str(objective.objective_2))
        objectives_list_chapter_3.append(str(objective.objective_3))
        objectives_list_chapter_3.append(str(objective.objective_4))
        objectives_list_chapter_3.append(str(objective.objective_5))
    num_of_true_status_chapter_3 = objectives_list_chapter_3[-5:].count("True")
    try:
        percentage_achieved_chapter_3 = round(
            (num_of_true_status_chapter_3 /
                len(objectives_list_chapter_3[-5:])) * 100, 2)
    except ZeroDivisionError:
        percentage_achieved_chapter_3 = 0
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

        # Chapters
        course_chapters=course_chapters,

        # Table of Contents
        all_toc=all_toc.items,

        # Objectives achieved
        percentage_achieved=percentage_achieved,
        percentage_achieved_chapter_2=percentage_achieved_chapter_2,
        percentage_achieved_chapter_3=percentage_achieved_chapter_3
        )


@bp.route('/web-development/chapter-2', methods=['GET', 'POST'])
@login_required
def web_development_chapter_2():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    teachers = Teacher.query.all()
    page = request.args.get('page', 1, type=int)

    # Table of Contents
    all_toc = TableOfContents.query.filter_by(
        title=student.student_course).order_by(
            TableOfContents.timestamp.asc()).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)

    # Dsiplaying the chapter
    course_chapters = Chapter.query.filter_by(allowed_status=True).all()

    # Chapter Comment form
    form = CommentForm()
    if form.validate_on_submit():
        comment = WebDevChapter2Comment(
            body=form.comment.data, author=student)
        db.session.add(comment)
        db.session.commit()
        for teacher in teachers:
            if teacher.teacher_course == student.student_course:
                send_flask_chapter_2_comment_email(teacher)
        flash('You will receive an email when your comment is approved.')
        return redirect(url_for(
            'student.web_development_chapter_2',
            _anchor='comments',
            student=student,
            title='Hello World',
            )
        )

    # Display student comments
    comments = WebDevChapter2Comment.query.filter_by(
        allowed_status=True).order_by(
            WebDevChapter2Comment.timestamp.desc()).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'student.web_development_chapter_2',
        _anchor="comments",
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'student.web_development_chapter_2',
        _anchor='comments',
        page=comments.prev_num) \
        if comments.has_prev else None
    all_comments = len(WebDevChapter2Comment.query.filter_by(
        allowed_status=True).all())

    # Chapter Objectives
    objectives_form = ChapterObjectivesForm()
    if objectives_form.validate_on_submit():
        objectives = WebDevChapter2Objectives(
            objective_1=objectives_form.objective_1.data,
            objective_2=objectives_form.objective_2.data,
            objective_3=objectives_form.objective_3.data,
            objective_4=objectives_form.objective_4.data,
            objective_5=objectives_form.objective_5.data,
            author=student)
        db.session.add(objectives)
        db.session.commit()
        flash('Your response has been saved')
        return redirect(url_for(
            'student.web_development_chapter_2',
            student_full_name=student.student_full_name,
            _anchor='objectives'))

    # CHAPTER 1: Calculate the number of objectives achieved
    all_objectives = student.webdev_chapter1_objectives.all()
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
            (num_of_true_status / len(objectives_list[-5:])) * 100, 2
        )
    except ZeroDivisionError:
        percentage_achieved = 0
    # End of Calculate the number of objectives achieved

    # CHAPTER 2: Calculate the number of objectives achieved
    all_objectives_chapter_2 = student.webdev_chapter2_objectives.all()
    objectives_list_chapter_2 = []
    num_of_true_status_chapter_2 = 0
    for objective in all_objectives_chapter_2:
        objectives_list_chapter_2.append(str(objective.objective_1))
        objectives_list_chapter_2.append(str(objective.objective_2))
        objectives_list_chapter_2.append(str(objective.objective_3))
        objectives_list_chapter_2.append(str(objective.objective_4))
        objectives_list_chapter_2.append(str(objective.objective_5))
    num_of_true_status_chapter_2 = objectives_list_chapter_2[-5:].count("True")
    try:
        percentage_achieved_chapter_2 = round(
            (num_of_true_status_chapter_2 /
                len(objectives_list_chapter_2[-5:])) * 100, 2)
    except ZeroDivisionError:
        percentage_achieved_chapter_2 = 0
    # End of Calculate the number of objectives achieved

    # CHAPTER 3: Calculate the number of objectives achieved
    all_objectives_chapter_3 = student.webdev_chapter3_objectives.all()
    objectives_list_chapter_3 = []
    num_of_true_status_chapter_3 = 0
    for objective in all_objectives_chapter_3:
        objectives_list_chapter_3.append(str(objective.objective_1))
        objectives_list_chapter_3.append(str(objective.objective_2))
        objectives_list_chapter_3.append(str(objective.objective_3))
        objectives_list_chapter_3.append(str(objective.objective_4))
        objectives_list_chapter_3.append(str(objective.objective_5))
    num_of_true_status_chapter_3 = objectives_list_chapter_3[-5:].count("True")
    try:
        percentage_achieved_chapter_3 = round(
            (num_of_true_status_chapter_3 /
                len(objectives_list_chapter_3[-5:])) * 100, 2)
    except ZeroDivisionError:
        percentage_achieved_chapter_3 = 0
    # End of Calculate the number of objectives achieved

    return render_template(
        'student/web-development-course/web_development_chapter_2.html',
        title='Chapter 2: Flask Templates',
        form=form,
        student=student,
        objectives_form=objectives_form,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,
        all_comments=all_comments,

        # Chapters
        course_chapters=course_chapters,

        # Table of Contents
        all_toc=all_toc.items,

        # Objectives achieved
        percentage_achieved=percentage_achieved,
        percentage_achieved_chapter_2=percentage_achieved_chapter_2,
        percentage_achieved_chapter_3=percentage_achieved_chapter_3
        )


@bp.route('/web-development/chapter-3', methods=['GET', 'POST'])
@login_required
def web_development_chapter_3():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    teachers = Teacher.query.all()
    page = request.args.get('page', 1, type=int)

    # Table of Contents
    all_toc = TableOfContents.query.filter_by(
        title=student.student_course).order_by(
            TableOfContents.timestamp.asc()).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)

    # Dsiplaying the chapter
    course_chapters = Chapter.query.filter_by(allowed_status=True).all()

    # Chapter Comment form
    form = CommentForm()
    if form.validate_on_submit():
        comment = WebDevChapter3Comment(
            body=form.comment.data, author=student)
        db.session.add(comment)
        db.session.commit()
        for teacher in teachers:
            if teacher.teacher_course == student.student_course:
                send_flask_chapter_3_comment_email(teacher)
        flash('You will receive an email when your comment is approved.')
        return redirect(url_for(
            'student.web_development_chapter_3',
            _anchor='comments',
            student=student,
            title='Hello World',
            )
        )

    # Display student comments
    comments = WebDevChapter3Comment.query.filter_by(
        allowed_status=True).order_by(
            WebDevChapter3Comment.timestamp.desc()).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'student.web_development_chapter_3',
        _anchor="comments",
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'student.web_development_chapter_3',
        _anchor='comments',
        page=comments.prev_num) \
        if comments.has_prev else None
    all_comments = len(WebDevChapter3Comment.query.filter_by(
        allowed_status=True).all())

    # Chapter Objectives
    objectives_form = ChapterObjectivesForm()
    if objectives_form.validate_on_submit():
        objectives = WebDevChapter3Objectives(
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
            'student.web_development_chapter_3',
            student_full_name=student.student_full_name,
            _anchor='objectives'))

    # CHAPTER 1: Calculate the number of objectives achieved
    all_objectives = student.webdev_chapter1_objectives.all()
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
            (num_of_true_status / len(objectives_list[-5:])) * 100, 2
        )
    except ZeroDivisionError:
        percentage_achieved = 0
    # End of Calculate the number of objectives achieved

    # CHAPTER 2: Calculate the number of objectives achieved
    all_objectives_chapter_2 = student.webdev_chapter2_objectives.all()
    objectives_list_chapter_2 = []
    num_of_true_status_chapter_2 = 0
    for objective in all_objectives_chapter_2:
        objectives_list_chapter_2.append(str(objective.objective_1))
        objectives_list_chapter_2.append(str(objective.objective_2))
        objectives_list_chapter_2.append(str(objective.objective_3))
        objectives_list_chapter_2.append(str(objective.objective_4))
        objectives_list_chapter_2.append(str(objective.objective_5))
    num_of_true_status_chapter_2 = objectives_list_chapter_2[-5:].count("True")
    try:
        percentage_achieved_chapter_2 = round(
            (num_of_true_status_chapter_2 /
                len(objectives_list_chapter_2[-5:])) * 100, 2)
    except ZeroDivisionError:
        percentage_achieved_chapter_2 = 0
    # End of Calculate the number of objectives achieved

    # CHAPTER 3: Calculate the number of objectives achieved
    all_objectives_chapter_3 = student.webdev_chapter3_objectives.all()
    objectives_list_chapter_3 = []
    num_of_true_status_chapter_3 = 0
    for objective in all_objectives_chapter_3:
        objectives_list_chapter_3.append(str(objective.objective_1))
        objectives_list_chapter_3.append(str(objective.objective_2))
        objectives_list_chapter_3.append(str(objective.objective_3))
        objectives_list_chapter_3.append(str(objective.objective_4))
        objectives_list_chapter_3.append(str(objective.objective_5))
    num_of_true_status_chapter_3 = objectives_list_chapter_3[-5:].count("True")
    try:
        percentage_achieved_chapter_3 = round(
            (num_of_true_status_chapter_3 /
                len(objectives_list_chapter_3[-5:])) * 100, 2)
    except ZeroDivisionError:
        percentage_achieved_chapter_3 = 0
    # End of Calculate the number of objectives achieved

    return render_template(
        'student/web-development-course/web_development_chapter_3.html',
        title='Chapter 3: Introduction to Web Forms',
        form=form,
        student=student,
        objectives_form=objectives_form,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,
        all_comments=all_comments,

        # Chapters
        course_chapters=course_chapters,

        # Table of Contents
        all_toc=all_toc.items,

        # Objectives achieved
        percentage_achieved=percentage_achieved,
        percentage_achieved_chapter_2=percentage_achieved_chapter_2,
        percentage_achieved_chapter_3=percentage_achieved_chapter_3
        )

# ==================================
# ======== CHAPTER QUIZES ==========
# ==================================

# Chapter 1 quiz 1


@bp.route(
    '/web-development/chapter-1/quiz-1', methods=['GET', 'POST'])
@login_required
def web_development_chapter_1_quiz_1():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 1
    quiz_1_form = Chapter1Quiz1OptionsForm()
    if quiz_1_form.validate_on_submit():
        answer = WebDevChapter1Quiz1Options(
            answer=quiz_1_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 1 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_chapter_1_quiz_2',
            student_full_name=student.student_full_name,
            _anchor="quiz_1"))
    return render_template(
        'student/web-development-course/quizzes/chapter_1/quiz_1.html',
        title='Chapter 1: Quiz 1',
        student=student,
        quizzes=quizzes,
        quiz_1_form=quiz_1_form
        )

# Chhapter 1 quiz 2


@bp.route(
    '/web-development/chapter-1/quiz-2', methods=['GET', 'POST'])
@login_required
def web_development_chapter_1_quiz_2():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 2
    quiz_2_form = Chapter1Quiz2OptionsForm()
    if quiz_2_form.validate_on_submit():
        answer = WebDevChapter1Quiz2Options(
            answer=quiz_2_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 2 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_chapter_1_quiz_3',
            student_full_name=student.student_full_name,
            _anchor="quiz_2"))
    return render_template(
        'student/web-development-course/quizzes/chapter_1/quiz_2.html',
        title='Chapter 1: Quiz 2',
        student=student,
        quizzes=quizzes,
        quiz_2_form=quiz_2_form
        )

# Chhapter 1 quiz 3


@bp.route(
    '/web-development/chapter-1/quiz-3', methods=['GET', 'POST'])
@login_required
def web_development_chapter_1_quiz_3():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 3
    quiz_3_form = Chapter1Quiz3OptionsForm()
    if quiz_3_form.validate_on_submit():
        answer = WebDevChapter1Quiz3Options(
            answer=quiz_3_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 3 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_chapter_1_quiz_4',
            student_full_name=student.student_full_name,
            _anchor="quiz_2"))
    return render_template(
        'student/web-development-course/quizzes/chapter_1/quiz_3.html',
        title='Chapter 1: Quiz 3',
        student=student,
        quizzes=quizzes,
        quiz_3_form=quiz_3_form
        )

# Chhapter 1 quiz 4


@bp.route(
    '/web-development/chapter-1/quiz-4', methods=['GET', 'POST'])
@login_required
def web_development_chapter_1_quiz_4():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 4
    quiz_4_form = Chapter1Quiz4OptionsForm()
    if quiz_4_form.validate_on_submit():
        answer = WebDevChapter1Quiz4Options(
            answer=quiz_4_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 4 answer have been added!',
              'Congratulations! You have completed the chapter 1 quiz!')
        return redirect(url_for(
            'student.web_development_chapter_1_quiz_5',
            student_full_name=student.student_full_name))
    return render_template(
        'student/web-development-course/quizzes/chapter_1/quiz_4.html',
        title='Chapter 1: Quiz 4',
        student=student,
        quizzes=quizzes,
        quiz_4_form=quiz_4_form
        )


# Chhapter 1 quiz 5


@bp.route(
    '/web-development/chapter-1/quiz-5', methods=['GET', 'POST'])
@login_required
def web_development_chapter_1_quiz_5():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 5
    quiz_5_form = Chapter1Quiz5OptionsForm()
    if quiz_5_form.validate_on_submit():
        answer = WebDevChapter1Quiz5Options(
            answer=quiz_5_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 4 answer have been added!',
              'Congratulations! You have completed the chapter 1 quiz!')
        return redirect(url_for(
            'student.web_development_chapter_1_total_score',
            student_full_name=student.student_full_name))
    return render_template(
        'student/web-development-course/quizzes/chapter_1/quiz_5.html',
        title='Chapter 1: Quiz 5',
        student=student,
        quizzes=quizzes,
        quiz_5_form=quiz_5_form
        )


# Chapter 2 quiz 1


@bp.route(
    '/web-development/chapter-2/quiz-1', methods=['GET', 'POST'])
@login_required
def web_development_chapter_2_quiz_1():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 1
    quiz_1_form = Chapter2Quiz1OptionsForm()
    if quiz_1_form.validate_on_submit():
        answer = WebDevChapter2Quiz1Options(
            answer=quiz_1_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 1 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_chapter_2_quiz_2',
            student_full_name=student.student_full_name,
            _anchor="quiz_1"))
    return render_template(
        'student/web-development-course/quizzes/chapter_2/quiz_1.html',
        title='Chapter 2: Quiz 1',
        student=student,
        quizzes=quizzes,
        quiz_1_form=quiz_1_form
        )

# Chapter 2 quiz 2


@bp.route(
    '/web-development/chapter-2/quiz-2', methods=['GET', 'POST'])
@login_required
def web_development_chapter_2_quiz_2():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 2
    quiz_2_form = Chapter2Quiz2OptionsForm()
    if quiz_2_form.validate_on_submit():
        answer = WebDevChapter2Quiz2Options(
            answer=quiz_2_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 2 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_chapter_2_quiz_3',
            student_full_name=student.student_full_name,
            _anchor="quiz_2"))
    return render_template(
        'student/web-development-course/quizzes/chapter_2/quiz_2.html',
        title='Chapter 2: Quiz 2',
        student=student,
        quizzes=quizzes,
        quiz_2_form=quiz_2_form
        )

# Chapter 2 quiz 3


@bp.route(
    '/web-development/chapter-2/quiz-3', methods=['GET', 'POST'])
@login_required
def web_development_chapter_2_quiz_3():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 3
    quiz_3_form = Chapter2Quiz3OptionsForm()
    if quiz_3_form.validate_on_submit():
        answer = WebDevChapter2Quiz3Options(
            answer=quiz_3_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 3 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_chapter_2_quiz_4',
            student_full_name=student.student_full_name,
            _anchor="quiz_3"))
    return render_template(
        'student/web-development-course/quizzes/chapter_2/quiz_3.html',
        title='Chapter 2: Quiz 3',
        student=student,
        quizzes=quizzes,
        quiz_3_form=quiz_3_form
        )

# Chapter 2 quiz 4


@bp.route(
    '/web-development/chapter-2/quiz-4', methods=['GET', 'POST'])
@login_required
def web_development_chapter_2_quiz_4():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 4
    quiz_4_form = Chapter2Quiz4OptionsForm()
    if quiz_4_form.validate_on_submit():
        answer = WebDevChapter2Quiz4Options(
            answer=quiz_4_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 3 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_chapter_2_quiz_5',
            student_full_name=student.student_full_name,
            _anchor="quiz_4"))
    return render_template(
        'student/web-development-course/quizzes/chapter_2/quiz_4.html',
        title='Chapter 2: Quiz 4',
        student=student,
        quizzes=quizzes,
        quiz_4_form=quiz_4_form
        )


# Chapter 2 quiz 5


@bp.route(
    '/web-development/chapter-2/quiz-5', methods=['GET', 'POST'])
@login_required
def web_development_chapter_2_quiz_5():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 4
    quiz_5_form = Chapter2Quiz5OptionsForm()
    if quiz_5_form.validate_on_submit():
        answer = WebDevChapter2Quiz5Options(
            answer=quiz_5_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 4 answer have been added!',
              'Congratulations! You have completed the chapter 2 quiz!')
        return redirect(url_for(
            'student.web_development_chapter_2_total_score',
            student_full_name=student.student_full_name,
            _anchor="quiz_5"))
    return render_template(
        'student/web-development-course/quizzes/chapter_2/quiz_5.html',
        title='Chapter 2: Quiz 5',
        student=student,
        quizzes=quizzes,
        quiz_5_form=quiz_5_form
        )


# Chapter 3 quiz 1


@bp.route(
    '/web-development/chapter-3/quiz-1', methods=['GET', 'POST'])
@login_required
def web_development_chapter_3_quiz_1():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 1
    quiz_1_form = Chapter3Quiz1OptionsForm()
    if quiz_1_form.validate_on_submit():
        answer = WebDevChapter3Quiz1Options(
            answer=quiz_1_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 1 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_chapter_3_quiz_2',
            student_full_name=student.student_full_name,
            _anchor="quiz_1"))
    return render_template(
        'student/web-development-course/quizzes/chapter_3/quiz_1.html',
        title='Chapter 3: Quiz 1',
        student=student,
        quizzes=quizzes,
        quiz_1_form=quiz_1_form
        )

# Chapter 3 quiz 2


@bp.route(
    '/web-development/chapter-3/quiz-2', methods=['GET', 'POST'])
@login_required
def web_development_chapter_3_quiz_2():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 2
    quiz_2_form = Chapter3Quiz2OptionsForm()
    if quiz_2_form.validate_on_submit():
        answer = WebDevChapter3Quiz2Options(
            answer=quiz_2_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 2 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_chapter_3_quiz_3',
            student_full_name=student.student_full_name,
            _anchor="quiz_2"))
    return render_template(
        'student/web-development-course/quizzes/chapter_3/quiz_2.html',
        title='Chapter 3: Quiz 2',
        student=student,
        quizzes=quizzes,
        quiz_2_form=quiz_2_form
        )

# Chapter 3 quiz 3


@bp.route(
    '/web-development/chapter-3/quiz-3', methods=['GET', 'POST'])
@login_required
def web_development_chapter_3_quiz_3():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 3
    quiz_3_form = Chapter3Quiz3OptionsForm()
    if quiz_3_form.validate_on_submit():
        answer = WebDevChapter3Quiz3Options(
            answer=quiz_3_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 3 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_chapter_3_quiz_4',
            student_full_name=student.student_full_name,
            _anchor="quiz_3"))
    return render_template(
        'student/web-development-course/quizzes/chapter_3/quiz_3.html',
        title='Chapter 3: Quiz 3',
        student=student,
        quizzes=quizzes,
        quiz_3_form=quiz_3_form
        )

# Chapter 3 quiz 4


@bp.route(
    '/web-development/chapter-3/quiz-4', methods=['GET', 'POST'])
@login_required
def web_development_chapter_3_quiz_4():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 4
    quiz_4_form = Chapter3Quiz4OptionsForm()
    if quiz_4_form.validate_on_submit():
        answer = WebDevChapter3Quiz4Options(
            answer=quiz_4_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 4 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_chapter_3_quiz_5',
            student_full_name=student.student_full_name,
            _anchor="quiz_4"))
    return render_template(
        'student/web-development-course/quizzes/chapter_3/quiz_4.html',
        title='Chapter 3: Quiz 4',
        student=student,
        quizzes=quizzes,
        quiz_4_form=quiz_4_form
        )


# Chapter 3 quiz 5


@bp.route(
    '/web-development/chapter-3/quiz-5', methods=['GET', 'POST'])
@login_required
def web_development_chapter_3_quiz_5():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Quiz 4
    quiz_5_form = Chapter3Quiz5OptionsForm()
    if quiz_5_form.validate_on_submit():
        answer = WebDevChapter3Quiz5Options(
            answer=quiz_5_form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 5 answer have been added!',
              'Congratulations! You have completed the chapter 3 quiz!')
        return redirect(url_for(
            'student.web_development_chapter_3_total_score',
            student_full_name=student.student_full_name,
            _anchor="quiz_5"))
    return render_template(
        'student/web-development-course/quizzes/chapter_3/quiz_5.html',
        title='Chapter 3: Quiz 5',
        student=student,
        quizzes=quizzes,
        quiz_5_form=quiz_5_form
        )


# Chapter 1 total score


@bp.route('/web-development/chapter-1/total-score')
@login_required
def web_development_chapter_1_total_score():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Calculate total score
    quiz_1_score = 0
    quiz_1_answers_list = []
    quiz_1_answer = student.webdev_chapter1_quiz_1_options.all()
    for answer in quiz_1_answer:
        quiz_1_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_1 = len(quiz_1_answers_list) - 1
        if quiz_1_answers_list[student_latest_answer_quiz_1].lower() == \
                "pip3 install flask":
            quiz_1_score += 1
        else:
            quiz_1_score += 0
    except IndexError:
        quiz_1_score += 0

    quiz_2_score = 0
    quiz_2_answers_list = []
    quiz_2_answer = student.webdev_chapter1_quiz_2_options.all()
    for answer in quiz_2_answer:
        quiz_2_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_2 = len(quiz_2_answers_list) - 1
        if quiz_2_answers_list[student_latest_answer_quiz_2].lower() == \
                "python":
            quiz_2_score += 1
        else:
            quiz_2_score += 0
    except IndexError:
        quiz_2_score += 0

    quiz_3_score = 0
    quiz_3_answers_list = []
    quiz_3_answer = student.webdev_chapter1_quiz_3_options.all()
    for answer in quiz_3_answer:
        quiz_3_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_3 = len(quiz_3_answers_list) - 1
        if quiz_3_answers_list[student_latest_answer_quiz_3].lower() == \
                "keeping the core simple but extensible":
            quiz_3_score += 1
        else:
            quiz_3_score += 0
    except IndexError:
        quiz_3_score += 0

    quiz_4_score = 0
    quiz_4_answers_list = []
    quiz_4_answer = student.webdev_chapter1_quiz_4_options.all()
    for answer in quiz_4_answer:
        quiz_4_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_4 = len(quiz_4_answers_list) - 1
        if quiz_4_answers_list[student_latest_answer_quiz_4].lower() == \
                "using the command flask run":
            quiz_4_score += 1
        else:
            quiz_4_score += 0
    except IndexError:
        quiz_4_score += 0

    quiz_5_score = 0
    quiz_5_answers_list = []
    quiz_5_answer = student.webdev_chapter1_quiz_5_options.all()
    for answer in quiz_5_answer:
        quiz_5_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_5 = len(quiz_5_answers_list) - 1
        if quiz_5_answers_list[student_latest_answer_quiz_5].lower() == \
                "view functions":
            quiz_5_score += 1
        else:
            quiz_5_score += 0
    except IndexError:
        quiz_5_score += 0

    # Calculate percentage
    total_score = quiz_1_score + quiz_2_score + quiz_3_score + quiz_4_score + \
        quiz_5_score
    try:
        total_score_percentage = round((total_score / 5) * 100, 2)
    except ZeroDivisionError:
        total_score_percentage = 0

    return render_template(
        'student/web-development-course/quizzes/chapter_1/total_score.html',
        title='Chapter 1: Total Score',
        student=student,
        quizzes=quizzes,

        quiz_1_answers_list=quiz_1_answers_list,
        quiz_2_answers_list=quiz_2_answers_list,
        quiz_3_answers_list=quiz_3_answers_list,
        quiz_4_answers_list=quiz_4_answers_list,
        quiz_5_answers_list=quiz_5_answers_list,

        student_latest_answer_quiz_1=student_latest_answer_quiz_1,
        student_latest_answer_quiz_2=student_latest_answer_quiz_2,
        student_latest_answer_quiz_3=student_latest_answer_quiz_3,
        student_latest_answer_quiz_4=student_latest_answer_quiz_4,
        student_latest_answer_quiz_5=student_latest_answer_quiz_5,

        quiz_1_score=quiz_1_score,
        quiz_2_score=quiz_2_score,
        quiz_3_score=quiz_3_score,
        quiz_4_score=quiz_4_score,
        quiz_5_score=quiz_5_score,
        total_score=total_score,
        total_score_percentage=total_score_percentage
        )


# Chapter 2 total score


@bp.route('/web-development/chapter-2/total-score')
@login_required
def web_development_chapter_2_total_score():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Calculate total score
    quiz_1_score = 0
    quiz_1_answers_list = []
    quiz_1_answer = student.webdev_chapter2_quiz_1_options.all()
    for answer in quiz_1_answer:
        quiz_1_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_1 = len(quiz_1_answers_list) - 1
        if quiz_1_answers_list[student_latest_answer_quiz_1].lower() == \
                "to display content":
            quiz_1_score += 1
        else:
            quiz_1_score += 0
    except IndexError:
        quiz_1_score += 0

    quiz_2_score = 0
    quiz_2_answers_list = []
    quiz_2_answer = student.webdev_chapter2_quiz_2_options.all()
    for answer in quiz_2_answer:
        quiz_2_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_2 = len(quiz_2_answers_list) - 1
        if quiz_2_answers_list[student_latest_answer_quiz_2].lower() == \
                "html":
            quiz_2_score += 1
        else:
            quiz_2_score += 0
    except IndexError:
        quiz_2_score += 0

    quiz_3_score = 0
    quiz_3_answers_list = []
    quiz_3_answer = student.webdev_chapter2_quiz_3_options.all()
    for answer in quiz_3_answer:
        quiz_3_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_3 = len(quiz_3_answers_list) - 1
        if quiz_3_answers_list[student_latest_answer_quiz_3].lower() == \
                "jinja":
            quiz_3_score += 1
        else:
            quiz_3_score += 0
    except IndexError:
        quiz_3_score += 0

    quiz_4_score = 0
    quiz_4_answers_list = []
    quiz_4_answer = student.webdev_chapter2_quiz_4_options.all()
    for answer in quiz_4_answer:
        quiz_4_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_4 = len(quiz_4_answers_list) - 1
        if quiz_4_answers_list[student_latest_answer_quiz_4].lower() == \
                "view functions":
            quiz_4_score += 1
        else:
            quiz_4_score += 0
    except IndexError:
        quiz_4_score += 0

    quiz_5_score = 0
    quiz_5_answers_list = []
    quiz_5_answer = student.webdev_chapter2_quiz_5_options.all()
    for answer in quiz_5_answer:
        quiz_5_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_5 = len(quiz_5_answers_list) - 1
        if quiz_5_answers_list[student_latest_answer_quiz_5].lower() == \
                "css":
            quiz_5_score += 1
        else:
            quiz_5_score += 0
    except IndexError:
        quiz_5_score += 0

    # Calculate percentage
    total_score = quiz_1_score + quiz_2_score + quiz_3_score + quiz_4_score + \
        quiz_5_score
    try:
        total_score_percentage = round((total_score / 5) * 100, 2)
    except ZeroDivisionError:
        total_score_percentage = 0

    return render_template(
        'student/web-development-course/quizzes/chapter_2/total_score.html',
        title='Chapter 2: Total Score',
        student=student,
        quizzes=quizzes,

        quiz_1_answers_list=quiz_1_answers_list,
        quiz_2_answers_list=quiz_2_answers_list,
        quiz_3_answers_list=quiz_3_answers_list,
        quiz_4_answers_list=quiz_4_answers_list,
        quiz_5_answers_list=quiz_5_answers_list,

        student_latest_answer_quiz_1=student_latest_answer_quiz_1,
        student_latest_answer_quiz_2=student_latest_answer_quiz_2,
        student_latest_answer_quiz_3=student_latest_answer_quiz_3,
        student_latest_answer_quiz_4=student_latest_answer_quiz_4,
        student_latest_answer_quiz_5=student_latest_answer_quiz_5,

        quiz_1_score=quiz_1_score,
        quiz_2_score=quiz_2_score,
        quiz_3_score=quiz_3_score,
        quiz_4_score=quiz_4_score,
        quiz_5_score=quiz_5_score,
        total_score=total_score,
        total_score_percentage=total_score_percentage
        )


# Chapter 3 total score


@bp.route('/web-development/chapter-3/total-score')
@login_required
def web_development_chapter_3_total_score():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = ChapterQuiz.query.filter_by(allowed_status=True).all()

    # Calculate total score
    quiz_1_score = 0
    quiz_1_answers_list = []
    quiz_1_answer = student.webdev_chapter3_quiz_1_options.all()
    for answer in quiz_1_answer:
        quiz_1_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_1 = len(quiz_1_answers_list) - 1
        if quiz_1_answers_list[student_latest_answer_quiz_1].lower() == \
                "to collect user data":
            quiz_1_score += 1
        else:
            quiz_1_score += 0
    except IndexError:
        quiz_1_score += 0

    quiz_2_score = 0
    quiz_2_answers_list = []
    quiz_2_answer = student.webdev_chapter3_quiz_2_options.all()
    for answer in quiz_2_answer:
        quiz_2_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_2 = len(quiz_2_answers_list) - 1
        if quiz_2_answers_list[student_latest_answer_quiz_2].lower() == \
                "flask-wtf":
            quiz_2_score += 1
        else:
            quiz_2_score += 0
    except IndexError:
        quiz_2_score += 0

    quiz_3_score = 0
    quiz_3_answers_list = []
    quiz_3_answer = student.webdev_chapter3_quiz_3_options.all()
    for answer in quiz_3_answer:
        quiz_3_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_3 = len(quiz_3_answers_list) - 1
        if quiz_3_answers_list[student_latest_answer_quiz_3].lower() == \
                "validationerror":
            quiz_3_score += 1
        else:
            quiz_3_score += 0
    except IndexError:
        quiz_3_score += 0

    quiz_4_score = 0
    quiz_4_answers_list = []
    quiz_4_answer = student.webdev_chapter3_quiz_4_options.all()
    for answer in quiz_4_answer:
        quiz_4_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_4 = len(quiz_4_answers_list) - 1
        if quiz_4_answers_list[student_latest_answer_quiz_4].lower() == \
                ".env":
            quiz_4_score += 1
        else:
            quiz_4_score += 0
    except IndexError:
        quiz_4_score += 0

    quiz_5_score = 0
    quiz_5_answers_list = []
    quiz_5_answer = student.webdev_chapter3_quiz_5_options.all()
    for answer in quiz_5_answer:
        quiz_5_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_5 = len(quiz_5_answers_list) - 1
        if quiz_5_answers_list[student_latest_answer_quiz_5].lower() == \
                "flask bootsrap":
            quiz_5_score += 1
        else:
            quiz_5_score += 0
    except IndexError:
        quiz_5_score += 0

    # Calculate percentage
    total_score = quiz_1_score + quiz_2_score + quiz_3_score + quiz_4_score + \
        quiz_5_score
    try:
        total_score_percentage = round((total_score / 5) * 100, 2)
    except ZeroDivisionError:
        total_score_percentage = 0

    return render_template(
        'student/web-development-course/quizzes/chapter_3/total_score.html',
        title='Chapter 3: Total Score',
        student=student,
        quizzes=quizzes,

        quiz_1_answers_list=quiz_1_answers_list,
        quiz_2_answers_list=quiz_2_answers_list,
        quiz_3_answers_list=quiz_3_answers_list,
        quiz_4_answers_list=quiz_4_answers_list,
        quiz_5_answers_list=quiz_5_answers_list,

        student_latest_answer_quiz_1=student_latest_answer_quiz_1,
        student_latest_answer_quiz_2=student_latest_answer_quiz_2,
        student_latest_answer_quiz_3=student_latest_answer_quiz_3,
        student_latest_answer_quiz_4=student_latest_answer_quiz_4,
        student_latest_answer_quiz_5=student_latest_answer_quiz_5,

        quiz_1_score=quiz_1_score,
        quiz_2_score=quiz_2_score,
        quiz_3_score=quiz_3_score,
        quiz_4_score=quiz_4_score,
        quiz_5_score=quiz_5_score,
        total_score=total_score,
        total_score_percentage=total_score_percentage
        )

# ========================================
# END OF WEB DEVELOPMENT COURSE ROUTES
# ========================================

# =========================================
# ==== GENERAL MULTIPLE CHOICE QUIZZES ====
# =========================================


@bp.route(
    '/web-development/general-multichoice-questions/quiz-1',
    methods=['GET', 'POST'])
@login_required
def web_development_general_quiz_1():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = GeneralMultipleChoicesQuiz.query.filter_by(
        allowed_status=True).all()
    form = GeneralQuiz1Form()
    if form.validate_on_submit():
        answer = GeneralMultipleChoicesAnswer1(
            answer=form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 1 answer have been recorded!', 'success')
        return redirect(url_for(
            'student.web_development_general_quiz_2',
            student_full_name=student.student_full_name))
    return render_template(
        'student/web-development-course/quizzes/general/quiz_1.html',
        title='General Quiz 1',
        student=student,
        form=form,
        quizzes=quizzes
        )


@bp.route(
    '/web-development/general-multichoice-questions/quiz-2',
    methods=['GET', 'POST'])
@login_required
def web_development_general_quiz_2():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = GeneralMultipleChoicesQuiz.query.filter_by(
        allowed_status=True).all()
    form = GeneralQuiz2Form()
    if form.validate_on_submit():
        answer = GeneralMultipleChoicesAnswer2(
            answer=form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 2 answer have been recorded!', 'success')
        return redirect(url_for(
            'student.web_development_general_quiz_3',
            student_full_name=student.student_full_name))
    return render_template(
        'student/web-development-course/quizzes/general/quiz_2.html',
        title='General Quiz 2',
        student=student,
        form=form,
        quizzes=quizzes
        )


@bp.route(
    '/web-development/general-multichoice-questions/quiz-3',
    methods=['GET', 'POST'])
@login_required
def web_development_general_quiz_3():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = GeneralMultipleChoicesQuiz.query.filter_by(
        allowed_status=True).all()
    form = GeneralQuiz3Form()
    if form.validate_on_submit():
        answer = GeneralMultipleChoicesAnswer3(
            answer=form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 3 answer have been recorded!', 'success')
        return redirect(url_for(
            'student.web_development_general_quiz_4',
            student_full_name=student.student_full_name))
    return render_template(
        'student/web-development-course/quizzes/general/quiz_3.html',
        title='General Quiz 3',
        student=student,
        form=form,
        quizzes=quizzes
        )


@bp.route(
    '/web-development/general-multichoice-questions/quiz-4',
    methods=['GET', 'POST'])
@login_required
def web_development_general_quiz_4():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = GeneralMultipleChoicesQuiz.query.filter_by(
        allowed_status=True).all()
    form = GeneralQuiz4Form()
    if form.validate_on_submit():
        answer = GeneralMultipleChoicesAnswer4(
            answer=form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 4 answer have been recorded!', 'success')
        return redirect(url_for(
            'student.web_development_general_quiz_5',
            student_full_name=student.student_full_name))
    return render_template(
        'student/web-development-course/quizzes/general/quiz_4.html',
        title='General Quiz 4',
        student=student,
        form=form,
        quizzes=quizzes
        )


@bp.route(
    '/web-development/general-multichoice-questions/quiz-5',
    methods=['GET', 'POST'])
@login_required
def web_development_general_quiz_5():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = GeneralMultipleChoicesQuiz.query.filter_by(
        allowed_status=True).all()
    form = GeneralQuiz5Form()
    if form.validate_on_submit():
        answer = GeneralMultipleChoicesAnswer5(
            answer=form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 5 answer have been recorded!', 'success')
        return redirect(url_for(
            'student.web_development_general_quiz_6',
            student_full_name=student.student_full_name))
    return render_template(
        'student/web-development-course/quizzes/general/quiz_5.html',
        title='General Quiz 5',
        student=student,
        form=form,
        quizzes=quizzes
        )


@bp.route(
    '/web-development/general-multichoice-questions/quiz-6',
    methods=['GET', 'POST'])
@login_required
def web_development_general_quiz_6():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = GeneralMultipleChoicesQuiz.query.filter_by(
        allowed_status=True).all()
    form = GeneralQuiz6Form()
    if form.validate_on_submit():
        answer = GeneralMultipleChoicesAnswer6(
            answer=form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 6 answer have been recorded!', 'success')
        return redirect(url_for(
            'student.web_development_general_quiz_7',
            student_full_name=student.student_full_name))
    return render_template(
        'student/web-development-course/quizzes/general/quiz_6.html',
        title='General Quiz 6',
        student=student,
        form=form,
        quizzes=quizzes
        )


@bp.route(
    '/web-development/general-multichoice-questions/quiz-7',
    methods=['GET', 'POST'])
@login_required
def web_development_general_quiz_7():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = GeneralMultipleChoicesQuiz.query.filter_by(
        allowed_status=True).all()
    form = GeneralQuiz7Form()
    if form.validate_on_submit():
        answer = GeneralMultipleChoicesAnswer7(
            answer=form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 7 answer have been recorded!', 'success')
        return redirect(url_for(
            'student.web_development_general_quiz_8',
            student_full_name=student.student_full_name))
    return render_template(
        'student/web-development-course/quizzes/general/quiz_7.html',
        title='General Quiz 7',
        student=student,
        form=form,
        quizzes=quizzes
        )


@bp.route(
    '/web-development/general-multichoice-questions/quiz-8',
    methods=['GET', 'POST'])
@login_required
def web_development_general_quiz_8():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = GeneralMultipleChoicesQuiz.query.filter_by(
        allowed_status=True).all()
    form = GeneralQuiz8Form()
    if form.validate_on_submit():
        answer = GeneralMultipleChoicesAnswer8(
            answer=form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 8 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_general_quiz_9',
            student_full_name=student.student_full_name))
    return render_template(
        'student/web-development-course/quizzes/general/quiz_8.html',
        title='General Quiz 8',
        student=student,
        form=form,
        quizzes=quizzes
        )


@bp.route(
    '/web-development/general-multichoice-questions/quiz-9',
    methods=['GET', 'POST'])
@login_required
def web_development_general_quiz_9():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = GeneralMultipleChoicesQuiz.query.filter_by(
        allowed_status=True).all()
    form = GeneralQuiz9Form()
    if form.validate_on_submit():
        answer = GeneralMultipleChoicesAnswer9(
            answer=form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 9 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_general_quiz_10',
            student_full_name=student.student_full_name))
    return render_template(
        'student/web-development-course/quizzes/general/quiz_9.html',
        title='General Quiz 9',
        student=student,
        form=form,
        quizzes=quizzes
        )


@bp.route(
    '/web-development/general-multichoice-questions/quiz-10',
    methods=['GET', 'POST'])
@login_required
def web_development_general_quiz_10():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = GeneralMultipleChoicesQuiz.query.filter_by(
        allowed_status=True).all()
    form = GeneralQuiz10Form()
    if form.validate_on_submit():
        answer = GeneralMultipleChoicesAnswer10(
            answer=form.answer.data, author=student)
        db.session.add(answer)
        db.session.commit()
        flash('Your quiz 10 answer have been added!', 'success')
        return redirect(url_for(
            'student.web_development_general_quiz_total_score',
            student_full_name=student.student_full_name))
    return render_template(
        'student/web-development-course/quizzes/general/quiz_10.html',
        title='General Quiz 10',
        student=student,
        form=form,
        quizzes=quizzes
        )


# General multiple choice total score


@bp.route('/web-development/general-multichoice-questions/total-score')
@login_required
def web_development_general_quiz_total_score():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name).first()
    quizzes = GeneralMultipleChoicesQuiz.query.filter_by(
        allowed_status=True).all()

    # Calculate total score
    quiz_1_score = 0
    quiz_1_answers_list = []
    quiz_1_answer = student.general_multi_choice_answer_1.all()
    for answer in quiz_1_answer:
        quiz_1_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_1 = len(quiz_1_answers_list) - 1
        if quiz_1_answers_list[student_latest_answer_quiz_1].lower() == \
                "to collect user data":
            quiz_1_score += 1
        else:
            quiz_1_score += 0
    except IndexError:
        quiz_1_score += 0

    quiz_2_score = 0
    quiz_2_answers_list = []
    quiz_2_answer = student.general_multi_choice_answer_2.all()
    for answer in quiz_2_answer:
        quiz_2_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_2 = len(quiz_2_answers_list) - 1
        if quiz_2_answers_list[student_latest_answer_quiz_2].lower() == \
                "flask-wtf":
            quiz_2_score += 1
        else:
            quiz_2_score += 0
    except IndexError:
        quiz_2_score += 0

    quiz_3_score = 0
    quiz_3_answers_list = []
    quiz_3_answer = student.general_multi_choice_answer_3.all()
    for answer in quiz_3_answer:
        quiz_3_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_3 = len(quiz_3_answers_list) - 1
        if quiz_3_answers_list[student_latest_answer_quiz_3].lower() == \
                "validationerror":
            quiz_3_score += 1
        else:
            quiz_3_score += 0
    except IndexError:
        quiz_3_score += 0

    quiz_4_score = 0
    quiz_4_answers_list = []
    quiz_4_answer = student.general_multi_choice_answer_4.all()
    for answer in quiz_4_answer:
        quiz_4_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_4 = len(quiz_4_answers_list) - 1
        if quiz_4_answers_list[student_latest_answer_quiz_4].lower() == \
                ".env":
            quiz_4_score += 1
        else:
            quiz_4_score += 0
    except IndexError:
        quiz_4_score += 0

    quiz_5_score = 0
    quiz_5_answers_list = []
    quiz_5_answer = student.general_multi_choice_answer_5.all()
    for answer in quiz_5_answer:
        quiz_5_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_5 = len(quiz_5_answers_list) - 1
        if quiz_5_answers_list[student_latest_answer_quiz_5].lower() == \
                "flask bootsrap":
            quiz_5_score += 1
        else:
            quiz_5_score += 0
    except IndexError:
        quiz_5_score += 0

    quiz_6_score = 0
    quiz_6_answers_list = []
    quiz_6_answer = student.general_multi_choice_answer_6.all()
    for answer in quiz_6_answer:
        quiz_6_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_6 = len(quiz_6_answers_list) - 1
        if quiz_6_answers_list[student_latest_answer_quiz_6].lower() == \
                "flask bootsrap":
            quiz_6_score += 1
        else:
            quiz_6_score += 0
    except IndexError:
        quiz_6_score += 0

    quiz_7_score = 0
    quiz_7_answers_list = []
    quiz_7_answer = student.general_multi_choice_answer_7.all()
    for answer in quiz_7_answer:
        quiz_7_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_7 = len(quiz_7_answers_list) - 1
        if quiz_7_answers_list[student_latest_answer_quiz_7].lower() == \
                "flask bootsrap":
            quiz_7_score += 1
        else:
            quiz_7_score += 0
    except IndexError:
        quiz_7_score += 0

    quiz_8_score = 0
    quiz_8_answers_list = []
    quiz_8_answer = student.general_multi_choice_answer_8.all()
    for answer in quiz_8_answer:
        quiz_8_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_8 = len(quiz_8_answers_list) - 1
        if quiz_8_answers_list[student_latest_answer_quiz_8].lower() == \
                "flask bootsrap":
            quiz_8_score += 1
        else:
            quiz_8_score += 0
    except IndexError:
        quiz_8_score += 0

    quiz_9_score = 0
    quiz_9_answers_list = []
    quiz_9_answer = student.general_multi_choice_answer_9.all()
    for answer in quiz_9_answer:
        quiz_9_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_9 = len(quiz_9_answers_list) - 1
        if quiz_9_answers_list[student_latest_answer_quiz_9].lower() == \
                "flask bootsrap":
            quiz_9_score += 1
        else:
            quiz_9_score += 0
    except IndexError:
        quiz_9_score += 0

    quiz_10_score = 0
    quiz_10_answers_list = []
    quiz_10_answer = student.general_multi_choice_answer_10.all()
    for answer in quiz_10_answer:
        quiz_10_answers_list.append(answer.answer)
    try:
        student_latest_answer_quiz_10 = len(quiz_10_answers_list) - 1
        if quiz_10_answers_list[student_latest_answer_quiz_10].lower() == \
                "flask bootsrap":
            quiz_10_score += 1
        else:
            quiz_10_score += 0
    except IndexError:
        quiz_10_score += 0

    # Calculate percentage
    total_score = quiz_1_score + quiz_2_score + quiz_3_score + quiz_4_score + \
        quiz_5_score + quiz_6_score + quiz_7_score + quiz_8_score + \
        quiz_9_score + quiz_10_score
    try:
        total_score_percentage = round((total_score / 10) * 100, 2)
    except ZeroDivisionError:
        total_score_percentage = 0

    return render_template(
        'student/web-development-course/quizzes/chapter_3/total_score.html',
        title='General Multi-choice Quiz: Total Score',
        student=student,
        quizzes=quizzes,

        quiz_1_answers_list=quiz_1_answers_list,
        quiz_2_answers_list=quiz_2_answers_list,
        quiz_3_answers_list=quiz_3_answers_list,
        quiz_4_answers_list=quiz_4_answers_list,
        quiz_5_answers_list=quiz_5_answers_list,
        quiz_6_answers_list=quiz_6_answers_list,
        quiz_7_answers_list=quiz_7_answers_list,
        quiz_8_answers_list=quiz_8_answers_list,
        quiz_9_answers_list=quiz_9_answers_list,
        quiz_10_answers_list=quiz_10_answers_list,

        student_latest_answer_quiz_1=student_latest_answer_quiz_1,
        student_latest_answer_quiz_2=student_latest_answer_quiz_2,
        student_latest_answer_quiz_3=student_latest_answer_quiz_3,
        student_latest_answer_quiz_4=student_latest_answer_quiz_4,
        student_latest_answer_quiz_5=student_latest_answer_quiz_5,
        student_latest_answer_quiz_6=student_latest_answer_quiz_6,
        student_latest_answer_quiz_7=student_latest_answer_quiz_7,
        student_latest_answer_quiz_8=student_latest_answer_quiz_8,
        student_latest_answer_quiz_9=student_latest_answer_quiz_9,
        student_latest_answer_quiz_10=student_latest_answer_quiz_10,

        quiz_1_score=quiz_1_score,
        quiz_2_score=quiz_2_score,
        quiz_3_score=quiz_3_score,
        quiz_4_score=quiz_4_score,
        quiz_5_score=quiz_5_score,
        quiz_6_score=quiz_6_score,
        quiz_7_score=quiz_7_score,
        quiz_8_score=quiz_8_score,
        quiz_9_score=quiz_9_score,
        quiz_10_score=quiz_10_score,

        total_score=total_score,
        total_score_percentage=total_score_percentage
        )

# ================================================
# ==== END OF GENERAL MULTIPLE CHOICE QUIZZES ====
# ================================================
