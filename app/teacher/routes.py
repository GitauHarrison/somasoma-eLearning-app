from crypt import methods
from app import db
from datetime import datetime
from app.teacher import bp
from flask_login import login_required, current_user
from flask import render_template, flash, request, redirect, url_for,\
    current_app, jsonify
from app.models import Teacher, TeacherCommunityComment, Student,\
    CommunityComment, WebDevelopmentOverview, TableOfContents, Chapter,\
    WebDevChapter1Comment, ChapterQuiz, BlogArticles,\
    Events, TeacherMessage, TeacherNotifications, WebDevChapter2Comment,\
    WebDevChapter3Comment, GeneralMultipleChoicesQuiz
from app.teacher.forms import EditProfileForm, CommentForm, EmptyForm,\
    WebDevelopmentOverviewForm, TableOfContentsForm, ChapterForm,\
    ChapterQuizForm, BlogArticlesForm, EventsForm,\
    PrivateMessageForm, GeneralOwnChoiceQuizForm
from app.teacher.email import send_live_flask_chapter_1_comment_email, \
    send_live_flask_chapter_2_comment_email,\
    send_live_flask_chapter_3_comment_email
from werkzeug.utils import secure_filename
import os


def chapter1_objectives(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name).first()

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

    # Chart for chapter 1 objectives
    objectives_attempts = {}
    for k, v in enumerate(all_objectives):
        objectives_attempts[k+1] = v
    print(objectives_attempts)
    print(len(objectives_list))
    chapter1_obj_attempts_chart_labels = list(objectives_attempts.keys())
    chapter1_obj_attempts_chart_data = []
    for i in range(0, len(objectives_list), 5):
        all_num_true_status = objectives_list[i:i+5].count("True")
        len_of_attempt = len(objectives_list[i:i+5])
        print(all_num_true_status, objectives_list[i:i+5])
        try:
            chapter1_obj_attempts_chart_data.append(
                round((all_num_true_status / len_of_attempt) * 100, 2))
        except ZeroDivisionError:
            chapter1_obj_attempts_chart_data.append(0)
    print('Chatper 1 Obj Labels: ', chapter1_obj_attempts_chart_labels)
    print('Chapter 1 Obj Values: ', chapter1_obj_attempts_chart_data, '\n\n')
    return percentage_achieved, chapter1_obj_attempts_chart_labels, \
        chapter1_obj_attempts_chart_data


def chapter2_objectives(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name).first()

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

    # Chart for chapter 2
    objectives_attempts_chapter2 = {}
    for k, v in enumerate(all_objectives_chapter_2):
        objectives_attempts_chapter2[k+1] = v
    obj_attempts_chart_labels_chapter2 = list(
        objectives_attempts_chapter2.keys())
    obj_attempts_chart_data_chapter2 = []
    for i in range(0, len(objectives_list_chapter_2), 5):
        all_num_true_status_chapter2 = \
            objectives_list_chapter_2[i:i+5].count("True")
        len_of_attempt_chapter2 = len(objectives_list_chapter_2[i:i+5])
        print(
            all_num_true_status_chapter2, objectives_list_chapter_2[i:i+5])
        try:
            obj_attempts_chart_data_chapter2.append(
                round(
                    (all_num_true_status_chapter2 /
                        len_of_attempt_chapter2) * 100, 2))
        except ZeroDivisionError:
            obj_attempts_chart_data_chapter2.append(0)
    print('Chapter 2 Obj Labels: ', obj_attempts_chart_labels_chapter2)
    print('Chapter 2 Obj Values: ', obj_attempts_chart_data_chapter2, '\n\n')
    # End of Calculate the number of objectives achieved
    return percentage_achieved_chapter_2, obj_attempts_chart_labels_chapter2, \
        obj_attempts_chart_data_chapter2


def chapter3_objectives(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name).first()

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

    # Chart for chapter 3
    objectives_attempts_chapter3 = {}
    for k, v in enumerate(all_objectives_chapter_3):
        objectives_attempts_chapter3[k+1] = v
    obj_attempts_chart_labels_chapter3 = list(
        objectives_attempts_chapter3.keys())
    obj_attempts_chart_data_chapter3 = []
    for i in range(0, len(objectives_list_chapter_3), 5):
        all_num_true_status_chapter3 = \
            objectives_list_chapter_3[i:i+5].count("True")
        len_of_attempt_chapter3 = len(objectives_list_chapter_3[i:i+5])
        print(
            all_num_true_status_chapter3, objectives_list_chapter_3[i:i+5])
        try:
            obj_attempts_chart_data_chapter3.append(
                round(
                    (all_num_true_status_chapter3 /
                        len_of_attempt_chapter3) * 100, 2))
        except ZeroDivisionError:
            obj_attempts_chart_data_chapter3.append(0)
    print('Chapter 3 Obj Labels: ', obj_attempts_chart_labels_chapter3)
    print('Chapter 3 Obj Values: ', obj_attempts_chart_data_chapter3, '\n\n')
    # End of Calculate the number of objectives achieved
    return percentage_achieved_chapter_3, obj_attempts_chart_labels_chapter3, \
        obj_attempts_chart_data_chapter3


def chapter1_total_score(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name).first()

    chapter1_total_score = student.webdev_chapter1_quiz_total_scores.all()

    # Keys as labels for chatJS
    quiz_attempts_chapter1 = {}
    for k, v in enumerate(chapter1_total_score):
        quiz_attempts_chapter1[k+1] = v
    quiz_attempts_chart_labels_chapter1 = list(
        quiz_attempts_chapter1.keys())

    # Data as values for chatJS
    chapter1_total_score_list = []
    int_total_score_list_chapter1 = []
    for score in chapter1_total_score:
        chapter1_total_score_list.append(score.total_score)
    int_total_score_list_chapter1 = \
        [int(float(i)) for i in chapter1_total_score_list]
    print('Chapter 1 Quiz Total Score: ', chapter1_total_score_list, 'Length : ', len(chapter1_total_score_list), ' Keys: ', quiz_attempts_chart_labels_chapter1)
    print('Int total score list: ', int_total_score_list_chapter1)
    return int_total_score_list_chapter1, quiz_attempts_chart_labels_chapter1


def chapter2_total_score(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name).first()

    chapter2_total_score = student.webdev_chapter2_quiz_total_scores.all()

    # Keys as labels for chatJS
    quiz_attempts_chapter2 = {}
    for k, v in enumerate(chapter2_total_score):
        quiz_attempts_chapter2[k+1] = v
    quiz_attempts_chart_labels_chapter2 = list(
        quiz_attempts_chapter2.keys())

    chapter2_total_score_list = []
    int_total_score_list_chapter2 = []
    for score in chapter2_total_score:
        chapter2_total_score_list.append(score.total_score)
    int_total_score_list_chapter2 = \
        [int(float(i)) for i in chapter2_total_score_list]
    print('Chapter 2 Quiz Total Score: ', chapter2_total_score_list, 'Length : ', len(chapter2_total_score_list), ' Keys: ', quiz_attempts_chart_labels_chapter2)
    return int_total_score_list_chapter2, quiz_attempts_chart_labels_chapter2


def chapter3_total_score(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name).first()

    chapter3_total_score = student.webdev_chapter3_quiz_total_scores.all()

    # Keys as labels for chatJS
    quiz_attempts_chapter3 = {}
    for k, v in enumerate(chapter3_total_score):
        quiz_attempts_chapter3[k+1] = v
    quiz_attempts_chart_labels_chapter3 = list(
        quiz_attempts_chapter3.keys())

    chapter3_total_score_list = []
    int_total_score_list_chapter3 = []
    for score in chapter3_total_score:
        chapter3_total_score_list.append(score.total_score)
    int_total_score_list_chapter3 = \
        [int(float(i)) for i in chapter3_total_score_list]
    print('Chapter 3 Quiz Total Score: ', chapter3_total_score_list, 'Length : ', len(chapter3_total_score_list), ' Keys: ', quiz_attempts_chart_labels_chapter3)
    return int_total_score_list_chapter3, quiz_attempts_chart_labels_chapter3


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.teacher_last_seen = datetime.utcnow()
        db.session.commit()


# Dashboard routes


@bp.route('/dashboard/account')
@login_required
def dashboard_account():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name).first()
    return render_template(
        'teacher/account.html',
        title='Account',
        teacher=teacher
        )


@bp.route('/dashboard/all-students')
@login_required
def dashboard_your_students():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name).first()
    students = Student.query.filter_by(
        student_course=teacher.teacher_course).order_by(
        Student.student_last_seen.desc()).all()
    all_students = len(students)
    return render_template(
        'teacher/your_students.html',
        title='All Students',
        teacher=teacher,
        students=students,
        all_students=all_students
        )


@bp.route('/dashboard/explore-teachers', methods=['GET', 'POST'])
@login_required
def dashboard_explore_teachers():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name).first()
    page = request.args.get('page', 1, type=int)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = TeacherCommunityComment(
            body=comment_form.comment.data,
            author=current_user
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('teacher.dashboard_explore_teachers'))
    comments = TeacherCommunityComment.query.order_by(
        TeacherCommunityComment.timestamp.desc()
        ).paginate(
            page,
            current_app.config['POSTS_PER_PAGE'],
            False
            )
    next_url = url_for(
        'teacher.dashboard_explore_teachers',
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'teacher.dashboard_explore_teachers',
        page=comments.prev_num) \
        if comments.has_prev else None
    return render_template(
        'teacher/explore_teachers.html',
        title='Explore Teachers',
        teacher=teacher,
        next_url=next_url,
        prev_url=prev_url,
        comments=comments.items,
        comment_form=comment_form
        )


@bp.route('/dashboard/my-teacher-community')
@login_required
def dashboard_my_teacher_community():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name).first()
    page = request.args.get('page', 1, type=int)
    comments = TeacherCommunityComment.query.order_by(
        TeacherCommunityComment.timestamp.desc()
        ).paginate(
            page,
            current_app.config['POSTS_PER_PAGE'],
            False
            )
    my_comments = current_user.followed_comments().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    my_next_url = url_for(
        'teacher.dashboard_my_teacher_community',
        page=comments.next_num) \
        if comments.has_next else None
    my_prev_url = url_for(
        'teacher.dashboard_my_teacher_community',
        page=comments.prev_num) \
        if comments.has_prev else None
    return render_template(
        'teacher/my_teacher_community.html',
        title='My Community',
        teacher=teacher,
        comments=comments.items,
        my_comments=my_comments.items,
        my_next_url=my_next_url,
        my_prev_url=my_prev_url
        )


@bp.route('/dashboard/student-community')
@login_required
def dashboard_student_community():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name).first()
    page = request.args.get('page', 1, type=int)
    comments = CommunityComment.query.order_by(
        CommunityComment.timestamp.desc()
        ).paginate(
            page,
            current_app.config['POSTS_PER_PAGE'],
            False
            )
    # Students community comments
    student_comments = CommunityComment.query.order_by(
        CommunityComment.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    student_next_url = url_for(
        'teacher.dashboard_student_community',
        page=comments.next_num) \
        if comments.has_next else None
    student_prev_url = url_for(
        'teacher.dashboard_student_community',
        page=comments.prev_num) \
        if comments.has_prev else None
    return render_template(
        'teacher/student_community.html',
        title='Student Community',
        teacher=teacher,
        comments=comments.items,
        student_comments=student_comments.items,
        student_next_url=student_next_url,
        student_prev_url=student_prev_url
        )


@bp.route('/dashboard/comment-moderation-links')
@login_required
def dashboard_comment_moderation():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name).first()
    course_chapters = Chapter.query.filter_by(
        course=teacher.teacher_course).all()
    return render_template(
        'teacher/comment_moderation.html',
        title='Comment Moderation',
        teacher=teacher,
        course_chapters=course_chapters
        )


@bp.route('/dashboard/manage-course', methods=['GET', 'POST'])
@login_required
def dashboard_manage_course():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name).first()

    # Manage Course Overview
    course_overview_form = WebDevelopmentOverviewForm()
    if course_overview_form.validate_on_submit():
        course_overview = WebDevelopmentOverview(
            title=course_overview_form.title.data,
            overview=course_overview_form.body.data,
            youtube_link=course_overview_form.youtube_link.data,
        )
        db.session.add(course_overview)
        db.session.commit()
        flash('Your course overview has been posted!', 'success')
        return redirect(url_for('teacher.review_course_overview'))

    # Manage Course Table of Contents
    table_of_contents_form = TableOfContentsForm()
    if table_of_contents_form.validate_on_submit():
        table_of_contents = TableOfContents(
            title=table_of_contents_form.title.data,
            chapter=table_of_contents_form.chapter.data,
            link=table_of_contents_form.link.data,
        )
        db.session.add(table_of_contents)
        db.session.commit()
        flash('Your table of contents has been updated!', 'success')
        return redirect(url_for('teacher.review_table_of_contents'))

    # Chapters
    chapter_form = ChapterForm()
    if chapter_form.validate_on_submit():
        chapter = Chapter(
            course=chapter_form.course.data,
            chapter=chapter_form.chapter.data,
            chapter_link=chapter_form.chapter_link.data,
            comment_moderation_link=chapter_form.comment_moderation_link.data,
            chapter_quiz_1_link=chapter_form.chapter_quiz_1_link.data,
            overview=chapter_form.overview.data,
            accomplish=chapter_form.accomplish.data,
            youtube_link=chapter_form.youtube_link.data,
            conclusion=chapter_form.conclusion.data,
            objective_1=chapter_form.objective_1.data,
            objective_2=chapter_form.objective_2.data,
            objective_3=chapter_form.objective_3.data,
            objective_4=chapter_form.objective_4.data,
            objective_5=chapter_form.objective_5.data,
        )
        db.session.add(chapter)
        db.session.commit()
        flash(f'{chapter} has been added!', 'success')
        return redirect(url_for('teacher.review_chapters'))

    # Chapter Quiz
    chapter_quiz_form = ChapterQuizForm()
    if chapter_quiz_form.validate_on_submit():
        chapter_quiz = ChapterQuiz(
            course=chapter_quiz_form.course.data,
            chapter=chapter_quiz_form.chapter.data,
            quiz_1=chapter_quiz_form.quiz_1.data,
            quiz_2=chapter_quiz_form.quiz_2.data,
            quiz_3=chapter_quiz_form.quiz_3.data,
            quiz_4=chapter_quiz_form.quiz_4.data,
            quiz_5=chapter_quiz_form.quiz_5.data
        )
        db.session.add(chapter_quiz)
        db.session.commit()
        flash('Chapter quiz has been added!', 'success')
        return redirect(url_for('teacher.review_chapter_quiz'))

    # General mulitple choices quiz
    mulitple_choice_quiz_form = GeneralOwnChoiceQuizForm()
    if mulitple_choice_quiz_form.validate_on_submit():
        chapter_quiz = GeneralMultipleChoicesQuiz(
            course=mulitple_choice_quiz_form.course.data,
            quiz_1=mulitple_choice_quiz_form.quiz_1.data,
            quiz_2=mulitple_choice_quiz_form.quiz_2.data,
            quiz_3=mulitple_choice_quiz_form.quiz_3.data,
            quiz_4=mulitple_choice_quiz_form.quiz_4.data,
            quiz_5=mulitple_choice_quiz_form.quiz_5.data,
            quiz_6=mulitple_choice_quiz_form.quiz_6.data,
            quiz_7=mulitple_choice_quiz_form.quiz_7.data,
            quiz_8=mulitple_choice_quiz_form.quiz_8.data,
            quiz_9=mulitple_choice_quiz_form.quiz_9.data,
            quiz_10=mulitple_choice_quiz_form.quiz_10.data
        )
        db.session.add(chapter_quiz)
        db.session.commit()
        flash('Chapter quiz has been added!', 'success')
        return redirect(url_for(
            'teacher.review_general_mulitiple_choices_quiz'))

    all_quizzes = ChapterQuiz.query.filter_by(
        course=teacher.teacher_course).all()
    all_multiple_quizzes = GeneralMultipleChoicesQuiz.query.filter_by(
        course=teacher.teacher_course).all()
    course_chapters = Chapter.query.filter_by(
        course=teacher.teacher_course).all()

    # Length
    all_chapters = len(Chapter.query.all())
    all_toc = len(TableOfContents.query.all())
    all_course_overview = len(WebDevelopmentOverview.query.all())
    all_chapter_quizzes = len(ChapterQuiz.query.all())
    all_general_multiple_choice_quizzes = len(
        GeneralMultipleChoicesQuiz.query.all())
    return render_template(
        'teacher/manage_course.html',
        title='Manage Your Course',
        teacher=teacher,

        # Course Overview
        course_overview_form=course_overview_form,
        all_course_overview=all_course_overview,

        # Table of Contents
        table_of_contents_form=table_of_contents_form,
        all_toc=all_toc,

        # Chapters
        chapter_form=chapter_form,
        course_chapters=course_chapters,
        all_chapters=all_chapters,

        # Chapter Quiz
        chapter_quiz_form=chapter_quiz_form,
        all_quizzes=all_quizzes,
        all_chapter_quizzes=all_chapter_quizzes,

        # Multiple Choice Quiz
        mulitple_choice_quiz_form=mulitple_choice_quiz_form,
        all_multiple_quizzes=all_multiple_quizzes,
        all_general_multiple_choice_quizzes=all_general_multiple_choice_quizzes
        )

# ==========================================
# MANAGE BLOG POSTS
# ==========================================


@bp.route('/dashboard/manage-blog', methods=['GET', 'POST'])
@login_required
def dashboard_manage_blog():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name).first()
    # ----------------
    # Blogs: anonymous user
    # ----------------

    blog_articles_form = BlogArticlesForm()
    if blog_articles_form.validate_on_submit():
        blog_articles = BlogArticles(
            article_image=blog_articles_form.article_image.data,
            article_name=blog_articles_form.article_name.data,
            body=blog_articles_form.body.data,
            link=blog_articles_form.link.data
        )

        # Handling file upload
        uploaded_file = blog_articles_form.article_image.data
        filename = secure_filename(uploaded_file.filename)
        if not os.path.exists(current_app.config['UPLOAD_PATH']):
            os.makedirs(current_app.config['UPLOAD_PATH'])
        blog_image_path = os.path.join(
            current_app.config['UPLOAD_PATH'],
            filename
            )
        print('Img path:', blog_image_path)
        uploaded_file.save(blog_image_path)
        blog_articles.article_image = blog_image_path
        print('Db path: ', blog_articles.article_image)

        blog_image_path_list = blog_articles.article_image.split('/')[1:]
        print('Img path list: ', blog_image_path_list)
        new_blog_image_path = '/'.join(blog_image_path_list)
        print('New img path: ', new_blog_image_path)
        blog_articles.article_image = new_blog_image_path
        print(blog_articles.article_image)

        db.session.add(blog_articles)
        db.session.commit()
        flash('You have addeded a new blog article')
        return redirect(url_for('teacher.dashboard_manage_blog'))
    all_blog_articles = len(BlogArticles.query.all())
    return render_template(
        'teacher/manage_blog.html',
        title='Manage Blog',
        teacher=teacher,
        all_blog_articles=all_blog_articles,
        blog_articles_form=blog_articles_form,
        )


@bp.route('/blog/articles/review')
@login_required
def review_blog_articles():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    blogs = BlogArticles.query.order_by(
        BlogArticles.timestamp.desc()
        ).paginate(
            page,
            current_app.config['POSTS_PER_PAGE'],
            False
            )
    next_url = url_for(
        'teacher.review_blog_articles',
        page=blogs.next_num,
        _anchor="blog") \
        if blogs.has_next else None
    prev_url = url_for(
        'teacher.review_blog_articles',
        page=blogs.prev_num,
        _anchor="blog") \
        if blogs.has_prev else None
    all_blogs = len(BlogArticles.query.all())
    return render_template(
        'teacher/review_blog_article.html',
        title='Review Blog Article',
        blogs=blogs.items,
        next_url=next_url,
        prev_url=prev_url,
        all_blogs=all_blogs,
        teacher=teacher
    )


@bp.route('/blog/articles/<blog_article_id>/allow')
def allow_blog_article(blog_article_id):
    blog_article = BlogArticles.query.filter_by(
        id=blog_article_id
    ).first()
    blog_article.allowed_status = True
    db.session.commit()
    flash(f'Blog article {blog_article_id} has been authorized')
    return redirect(url_for('teacher.review_blog_articles'))

# ==========================================
# END OF MANAGE BLOG POSTS
# ==========================================


@bp.route('/dashboard/manage-events', methods=['GET', 'POST'])
@login_required
def dashboard_manage_events():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name).first()
    event_form = EventsForm()
    if event_form.validate_on_submit():
        event = Events(
            title=event_form.event_title.data,
            body=event_form.event_body.data,
            date=event_form.event_date.data,
            time=event_form.event_time.data,
            location=event_form.event_location.data,
            link=event_form.event_link.data
            )

        # Handling file upload
        uploaded_file = event_form.event_image.data
        filename = secure_filename(uploaded_file.filename)
        if not os.path.exists(current_app.config['UPLOAD_PATH']):
            os.makedirs(current_app.config['UPLOAD_PATH'])
        event_image_path = os.path.join(
            current_app.config['UPLOAD_PATH'],
            filename
            )
        print('Img path:', event_image_path)
        uploaded_file.save(event_image_path)
        event.event_image = event_image_path
        print('Db path: ', event.event_image)

        event_image_path_list = event.event_image.split('/')[1:]
        print('Img path list: ', event_image_path_list)
        new_event_image_path = '/'.join(event_image_path_list)
        print('New img path: ', new_event_image_path)
        event.event_image = new_event_image_path
        print(event.event_image)

        db.session.add(event)
        db.session.commit()
        flash('Your event has been updated. Take action now!')
        return redirect(url_for(
            'teacher.dashboard_manage_events',
            _anchor='events')
            )
    page = request.args.get('page', 1, type=int)
    events = Events.query.order_by(
        Events.timestamp.desc()
        ).paginate(
            page,
            current_app.config['POSTS_PER_PAGE'],
            False
            )
    next_url = url_for(
        'admin.dashboard_manage_events',
        page=events.next_num,
        _anchor="events") \
        if events.has_next else None
    prev_url = url_for(
        'admin.dashboard_manage_events',
        page=events.prev_num,
        _anchor="events") \
        if events.has_prev else None
    all_events = len(Events.query.all())

    return render_template(
        'teacher/manage_events.html',
        title='Manage Events',
        teacher=teacher,
        events=events.items,
        next_url=next_url,
        prev_url=prev_url,
        all_events=all_events,
        event_form=event_form
        )


@bp.route('/events/<event_id>/delete')
def delete_event(event_id):
    event = Events.query.filter_by(
        id=event_id
        ).first()
    db.session.delete(event)
    db.session.commit()
    flash(f'Event {event_id} has been deleted!')
    return redirect(url_for(
        'admin.dashboard_manage_events',
        _anchor='events')
        )


@bp.route('/event/<event_id>/allow', methods=['GET', 'POST'])
def allow_event(event_id):
    event = Events.query.filter_by(
        id=event_id
        ).first()
    event.allowed_status = True
    db.session.commit()
    flash(f'Event {event_id} has been authorized!')
    return redirect(url_for(
        'teacher.dashboard_manage_events',
        _anchor="events")
        )

# Profile route


@bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    form = EditProfileForm(current_user.teacher_email)
    if form.validate_on_submit():
        current_user.teacher_email = form.email.data
        current_user.teacher_about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for(
            'teacher.dashboard_account'
            )
        )
    elif request.method == 'GET':
        form.email.data = current_user.teacher_email
        form.about_me.data = current_user.teacher_about_me
    return render_template(
        'teacher/edit_profile_teacher.html',
        teacher=teacher,
        form=form,
        title='Edit Profile Teacher'
        )


@bp.route('/profile/<teacher_full_name>')
@login_required
def profile_teacher(teacher_full_name):
    teacher = Teacher.query.filter_by(
        teacher_full_name=teacher_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    comments = teacher.comments.order_by(
        TeacherCommunityComment.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'teacher.profile_teacher', teacher_full_name=teacher_full_name,
        _anchor="teacher-comments",
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'teacher.profile_teacher', teacher_full_name=teacher_full_name,
        _anchor="teacher-comments",
        page=comments.prev_num) \
        if comments.has_prev else None
    form = EmptyForm()
    return render_template(
        'teacher/profile_teacher.html',
        teacher=teacher,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,
        form=form,
        title='Teacher Profile'
        )

# Profile Popup


@bp.route('/profile/<teacher_full_name>/popup/')
@login_required
def teacher_profile_popup(teacher_full_name):
    teacher = Teacher.query.filter_by(
        teacher_full_name=teacher_full_name
        ).first_or_404()
    form = EmptyForm()
    return render_template(
        'teacher/profile_teacher_popup.html',
        teacher=teacher,
        title='Teacher Profile',
        form=form
        )


# Send private messages route

@bp.route('/send-messages/<recipient>', methods=['GET', 'POST'])
@login_required
def send_messages(recipient):
    teacher = Teacher.query.filter_by(
        teacher_full_name=recipient
        ).first()
    form = PrivateMessageForm()
    if form.validate_on_submit():
        private_message = TeacherMessage(
            author=current_user,
            recipient=teacher,
            body=form.message.data
            )
        db.session.add(private_message)
        teacher.add_notification(
            'unread_message_count', teacher.new_messages()
            )
        db.session.commit()
        flash('Your message has been sent!')
        return redirect(url_for(
            'teacher.send_messages',
            recipient=recipient)
            )
    return render_template(
        'teacher/private_messages/send_private_messages.html',
        teacher=teacher,
        title='Send Private Messages',
        form=form
        )

# View private messages route


@bp.route('/messages')
@login_required
def view_messages():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
            TeacherMessage.timestamp.desc()).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'teacher.view_messages',
        page=messages.next_num,
        _anchor="messages") \
        if messages.has_next else None
    prev_url = url_for(
        'teacher.view_messages',
        page=messages.prev_num,
        _anchor="messages") \
        if messages.has_prev else None
    return render_template(
        'teacher/private_messages/view_private_messages.html',
        messages=messages.items,
        title='View Private Messages',
        next_url=next_url,
        prev_url=prev_url,
        teacher=teacher
        )

# Teacher notificatons route


@bp.route('/notifications')
@login_required
def teacher_notifications():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    since = request.args.get('since', 0.0, type=float)
    notifications = teacher.notifications.filter(
        TeacherNotifications.timestamp > since).order_by(
            TeacherNotifications.timestamp.asc())
    return jsonify([{
        'teacher_full_name': n.teacher_full_name,
        'data': n.get_data(),
        'timestamp': n.timestamp
        } for n in notifications])


@bp.route('/profile/student/<student_full_name>')
@login_required
def profile_student(student_full_name):
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    student = Student.query.filter_by(
        student_full_name=student_full_name
        ).first()

    # Dsiplaying the chapter
    course_chapters = Chapter.query.filter_by(allowed_status=True).all()

    # Objectives and Quiz charts
    chapter1_objectives_results = list(chapter1_objectives(
        student_full_name=student_full_name))
    chapter2_objectives_results = list(chapter2_objectives(
        student_full_name=student_full_name))
    chapter3_objectives_results = list(chapter3_objectives(
        student_full_name=student_full_name))
    chapter1_total_score_results = list(chapter1_total_score(
        student_full_name=student_full_name))
    chapter1_total_score_labels = list(chapter1_total_score(
        student_full_name=student_full_name))
    chapter2_total_score_results = list(chapter2_total_score(
        student_full_name=student_full_name))
    chapter2_total_score_labels = list(chapter2_total_score(
        student_full_name=student_full_name))
    chapter3_total_score_results = list(chapter3_total_score(
        student_full_name=student_full_name))
    chapter3_total_score_labels = list(chapter3_total_score(
        student_full_name=student_full_name))
    print('Teacher Obj Results: ', chapter1_total_score_results)
    chapter1_obj_attempts_chart_labels = chapter1_objectives_results[1]
    chapter1_obj_attempts_chart_data = chapter1_objectives_results[2]
    obj_attempts_chart_labels_chapter2 = chapter2_objectives_results[1]
    obj_attempts_chart_data_chapter2 = chapter2_objectives_results[2]
    obj_attempts_chart_labels_chapter3 = chapter3_objectives_results[1]
    obj_attempts_chart_data_chapter3 = chapter3_objectives_results[2]
    int_total_score_list_chapter1 = chapter1_total_score_results[0]
    quiz_attempts_chart_labels_chapter1 = chapter1_total_score_labels[1]
    int_total_score_list_chapter2 = chapter2_total_score_results[0]
    quiz_attempts_chart_labels_chapter2 = chapter2_total_score_labels[1]
    int_total_score_list_chapter3 = chapter3_total_score_results[0]
    quiz_attempts_chart_labels_chapter3 = chapter3_total_score_labels[1]
    # End of charts
    
    page = request.args.get('page', 1, type=int)
    comments = student.comments.order_by(
        CommunityComment.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'teacher.profile_student', student_full_name=student_full_name,
        _anchor="student-comments",
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'teacher.profile_student', student_full_name=student_full_name,
        _anchor="student-comments",
        page=comments.prev_num) \
        if comments.has_prev else None
    form = EmptyForm()
    all_comments = len(student.comments.all())
    return render_template(
        'teacher/profile_student.html',
        teacher=teacher,
        student=student,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,
        form=form,
        title='Student Profile',
        all_comments=all_comments,
        course_chapters=course_chapters,
        chapter1_obj_attempts_chart_labels=chapter1_obj_attempts_chart_labels,
        chapter1_obj_attempts_chart_data=chapter1_obj_attempts_chart_data,
        obj_attempts_chart_labels_chapter2=obj_attempts_chart_labels_chapter2,
        obj_attempts_chart_data_chapter2=obj_attempts_chart_data_chapter2,
        obj_attempts_chart_labels_chapter3=obj_attempts_chart_labels_chapter3,
        obj_attempts_chart_data_chapter3=obj_attempts_chart_data_chapter3,
        int_total_score_list_chapter1=int_total_score_list_chapter1,
        quiz_attempts_chart_labels_chapter1=quiz_attempts_chart_labels_chapter1,
        int_total_score_list_chapter2=int_total_score_list_chapter2,
        quiz_attempts_chart_labels_chapter2=quiz_attempts_chart_labels_chapter2,
        int_total_score_list_chapter3=int_total_score_list_chapter3,
        quiz_attempts_chart_labels_chapter3=quiz_attempts_chart_labels_chapter3
        )


@bp.route('/profile/student/<student_full_name>/popup/')
@login_required
def student_profile_popup(student_full_name):
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    student = Student.query.filter_by(
        student_full_name=student_full_name
        ).first()
    return render_template(
        'teacher/profile_student_popup.html',
        student=student,
        teacher=teacher,
        title='Student Profile'
        )

# End of profile route

# Followership routes


@bp.route('/follow/<teacher_full_name>', methods=['POST'])
@login_required
def follow_teacher(teacher_full_name):
    teacher = Teacher.query.filter_by(
        teacher_full_name=teacher_full_name
        ).first()
    form = EmptyForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(
            teacher_full_name=teacher_full_name
            ).first()
        if teacher is None:
            flash(f'User {teacher_full_name} not found')
            return redirect(url_for('teacher.dashboard_explore_teachers'))
        if teacher == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for(
                'teacher.profile_teacher',
                teacher_full_name=teacher_full_name
                )
            )
        current_user.follow(teacher)
        db.session.commit()
        flash(f'You are following {teacher.teacher_full_name}!')
        return redirect(url_for(
            'teacher.profile_teacher',
            teacher_full_name=teacher_full_name
            )
        )
    else:
        return redirect(url_for('teacher.dashboard_explore_teachers'))


@bp.route('/unfollow/<teacher_full_name>', methods=['POST'])
@login_required
def unfollow_teacher(teacher_full_name):
    teacher = Teacher.query.filter_by(
        teacher_full_name=teacher_full_name
        ).first()
    form = EmptyForm()
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(
            teacher_full_name=teacher_full_name
            ).first()
        if teacher is None:
            flash(f'User {teacher_full_name} not found')
            return redirect(url_for('teacher.dashboard_explore_teachers'))
        if teacher == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for(
                'teacher.profile_teacher',
                teacher_full_name=teacher_full_name
                )
            )
        current_user.unfollow(teacher)
        db.session.commit()
        flash(f'You are not following {teacher.teacher_full_name}!')
        return redirect(url_for(
            'teacher.profile_teacher',
            teacher_full_name=teacher_full_name
            )
        )
    else:
        return redirect(url_for('teacher.dashboard_explore_teachers'))

# End of followership routes

# ========================================
# COURSE MANAGEMENT ROUTES
# ========================================

# Overview route


@bp.route('/course/overview/review')
@login_required
def review_course_overview():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    course_overview = WebDevelopmentOverview.query.filter_by(
        title=teacher.teacher_course
    ).order_by(
        WebDevelopmentOverview.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    course_overview_next_url = url_for(
        'teacher.review_course_overview',
        page=course_overview.next_num) \
        if course_overview.has_next else None
    course_overview_prev_url = url_for(
        'teacher.review_course_overview',
        page=course_overview.prev_num) \
        if course_overview.has_prev else None

    # Table of contents
    course_toc = TableOfContents.query.filter_by(
        title=teacher.teacher_course).order_by(
        TableOfContents.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)

    return render_template(
        'teacher/course/flask/reviews/flask_overview.html',
        teacher=teacher,
        title='Review Course Overview',
        course_overview=course_overview.items,
        course_overview_next_url=course_overview_next_url,
        course_overview_prev_url=course_overview_prev_url,
        course_toc=course_toc.items
        )


@bp.route('/course/overview/<course_title>/allow')
def allow_course_overview(course_title):
    course = WebDevelopmentOverview.query.filter_by(
        title=course_title
        ).first()
    course.allowed_status = True
    db.session.commit()
    flash('Course overview has been allowed.')
    return redirect(url_for(
        'teacher.review_course_overview'
        )
    )


@bp.route('/course/overview/<course_title>/delete')
def delete_course_overview(course_title):
    course = WebDevelopmentOverview.query.filter_by(
        title=course_title
        ).first()
    db.session.delete(course)
    db.session.commit()
    flash('Course overview has been deleted.')
    return redirect(url_for(
        'teacher.review_course_overview'
        )
    )


# Table of contents route


@bp.route('/course/toc/review')
@login_required
def review_table_of_contents():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    course_toc = TableOfContents.query.filter_by(
        title=teacher.teacher_course
    ).order_by(
        TableOfContents.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    course_toc_next_url = url_for(
                    'teacher.review_table_of_contents',
                    page=course_toc.next_num) \
        if course_toc.has_next else None
    course_toc_prev_url = url_for(
        'teacher.review_table_of_contents',
        page=course_toc.prev_num) \
        if course_toc.has_prev else None
    all_toc = len(TableOfContents.query.all())
    return render_template(
        'teacher/course/flask/reviews/flask_toc.html',
        teacher=teacher,
        title='Review Table of Contents',
        course_toc=course_toc.items,
        course_toc_next_url=course_toc_next_url,
        course_toc_prev_url=course_toc_prev_url,
        all_toc=all_toc
        )


@bp.route('/course/toc/<chapter>/allow')
def allow_table_of_contents(chapter):
    toc = TableOfContents.query.filter_by(
        chapter=chapter
        ).first()
    toc.allowed_status = True
    db.session.commit()
    flash(f'{chapter} in table of contents has been allowed.')
    return redirect(url_for(
        'teacher.review_table_of_contents'
        )
    )


@bp.route('/course/toc/<chapter>/delete')
def delete_table_of_contents(chapter):
    toc = TableOfContents.query.filter_by(
        chapter=chapter
        ).first()
    db.session.delete(toc)
    db.session.commit()
    flash(f'{chapter} in table of contents has been deleted.')
    return redirect(url_for(
        'teacher.review_table_of_contents'
        )
    )

# Chapters


@bp.route('/course/chapters/review')
@login_required
def review_chapters():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    page = request.args.get('page', 1, type=int)

    # Chapters
    course_chapters = Chapter.query.filter_by(
        course=teacher.teacher_course
    ).order_by(
        Chapter.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    course_chapters_next_url = url_for(
        'teacher.review_chapters',
        page=course_chapters.next_num) \
        if course_chapters.has_next else None
    course_chapters_prev_url = url_for(
        'teacher.review_chapters',
        page=course_chapters.prev_num) \
        if course_chapters.has_prev else None
    all_chapters = len(Chapter.query.all())
    # Table of contents
    toc_chapters = TableOfContents.query.filter_by(
        title=teacher.teacher_course).order_by(
            TableOfContents.timestamp.asc()).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)

    return render_template(
        'teacher/course/flask/reviews/flask_chapters.html',
        teacher=teacher,
        title='Review Chapters',
        all_chapters=all_chapters,

        # Chapters
        course_chapters=course_chapters.items,
        course_chapters_next_url=course_chapters_next_url,
        course_chapters_prev_url=course_chapters_prev_url,

        # Table of contents
        toc_chapters=toc_chapters.items
        )


@bp.route('/course/chapters/<chapter>/allow')
def allow_chapters(chapter):
    chapter = Chapter.query.filter_by(
        chapter=chapter
        ).first()
    chapter.allowed_status = True
    db.session.commit()
    flash('Chapter has been allowed.')
    return redirect(url_for(
        'teacher.review_chapters'
        )
    )


@bp.route('/course/chapters/<chapter>/delete')
def delete_chapters(chapter):
    chapter = Chapter.query.filter_by(
        chapter=chapter
        ).first()
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter has been deleted.')
    return redirect(url_for(
        'teacher.review_chapters'
        )
    )

# ========================================
# END OF COURSE MANAGEMENT ROUTES
# ========================================


# ========================================
# COMMENTS MANAGEMENT ROUTES
# ========================================

# Flask Chapter 1

@bp.route('/flask/chapter-1/comments/review')
@login_required
def review_flask_chapter_1_comments():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    flask_chapter_1_comments = WebDevChapter1Comment.query.order_by(
        WebDevChapter1Comment.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    flask_chapter_1_comments_next_url = url_for(
        'teacher.review_flask_chapter_1_comments',
        page=flask_chapter_1_comments.next_num) \
        if flask_chapter_1_comments.has_next else None
    flask_chapter_1_comments_prev_url = url_for(
        'teacher.review_flask_chapter_1_comments',
        page=flask_chapter_1_comments.prev_num) \
        if flask_chapter_1_comments.has_prev else None
    all_flask_chapter_1_comments = len(WebDevChapter1Comment.query.all())
    return render_template(
        'teacher/course/flask/reviews/flask_chapter_1_comments.html',
        teacher=teacher,
        title='Review Flask Chapter 1 Comments',
        flask_chapter_1_comments=flask_chapter_1_comments.items,
        flask_chapter_1_comments_next_url=flask_chapter_1_comments_next_url,
        flask_chapter_1_comments_prev_url=flask_chapter_1_comments_prev_url,
        all_flask_chapter_1_comments=all_flask_chapter_1_comments
        )


@bp.route('/flask/chapter-1/comments/<int:id>/allow')
def allow_flask_chapter_1_comments(id):
    student = Student.query.filter_by(
        id=id).first()
    comment = WebDevChapter1Comment.query.get_or_404(id)
    comment.allowed_status = True
    db.session.commit()
    send_live_flask_chapter_1_comment_email(student)
    flash(f'Flask chapter 1 comment {id} has been allowed.')
    return redirect(url_for(
        'teacher.review_flask_chapter_1_comments'
        )
    )


@bp.route('/flask/chapter-1/comments/<int:id>/delete')
def delete_flask_chapter_1_comments(id):
    comment = WebDevChapter1Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash(f'Flask chapter 1 comment {id} has been deleted.')
    return redirect(url_for(
        'teacher.review_flask_chapter_1_comments'
        )
    )


# Flask Chapter 2

@bp.route('/flask/chapter-2/comments/review')
@login_required
def review_flask_chapter_2_comments():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    comments = WebDevChapter2Comment.query.order_by(
        WebDevChapter2Comment.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'teacher.review_flask_chapter_2_comments',
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'teacher.review_flask_chapter_2_comments',
        page=comments.prev_num) \
        if comments.has_prev else None
    all_comments = len(WebDevChapter2Comment.query.all())
    return render_template(
        'teacher/course/flask/reviews/flask_chapter_2_comments.html',
        teacher=teacher,
        title='Review Flask Chapter 2 Comments',
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,
        all_comments=all_comments
        )


@bp.route('/flask/chapter-2/comments/<int:id>/allow')
def allow_flask_chapter_2_comments(id):
    student = Student.query.filter_by(
        id=id).first()
    comment = WebDevChapter2Comment.query.get_or_404(id)
    comment.allowed_status = True
    db.session.commit()
    send_live_flask_chapter_2_comment_email(student)
    flash(f'Flask chapter 2 comment {id} has been allowed.')
    return redirect(url_for(
        'teacher.review_flask_chapter_2_comments'
        )
    )


@bp.route('/flask/chapter-2/comments/<int:id>/delete')
def delete_flask_chapter_2_comments(id):
    comment = WebDevChapter2Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash(f'Flask chapter 3 comment {id} has been deleted.')
    return redirect(url_for(
        'teacher.review_flask_chapter_2_comments'
        )
    )


# Flask Chapter 3

@bp.route('/flask/chapter-3/comments/review')
@login_required
def review_flask_chapter_3_comments():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    comments = WebDevChapter3Comment.query.order_by(
        WebDevChapter3Comment.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'teacher.review_flask_chapter_3_comments',
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'teacher.review_flask_chapter_3_comments',
        page=comments.prev_num) \
        if comments.has_prev else None
    all_comments = len(WebDevChapter3Comment.query.all())
    return render_template(
        'teacher/course/flask/reviews/flask_chapter_3_comments.html',
        teacher=teacher,
        title='Review Flask Chapter 3 Comments',
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,
        all_comments=all_comments
        )


@bp.route('/flask/chapter-3/comments/<int:id>/allow')
def allow_flask_chapter_3_comments(id):
    student = Student.query.filter_by(
        id=id).first()
    comment = WebDevChapter3Comment.query.get_or_404(id)
    comment.allowed_status = True
    db.session.commit()
    send_live_flask_chapter_3_comment_email(student)
    flash(f'Flask chapter 3 comment {id} has been allowed.')
    return redirect(url_for(
        'teacher.review_flask_chapter_3_comments'
        )
    )


@bp.route('/flask/chapter-3/comments/<int:id>/delete')
def delete_flask_chapter_3_comments(id):
    comment = WebDevChapter3Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash(f'Flask chapter 3 comment {id} has been deleted.')
    return redirect(url_for(
        'teacher.review_flask_chapter_3_comments'
        )
    )


# Flask chapter quiz


@bp.route('/flask/quiz/review')
@login_required
def review_chapter_quiz():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    flask_quiz = ChapterQuiz.query.order_by(
        ChapterQuiz.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    flask_quiz_next_url = url_for(
        'teacher.review_chapter_quiz',
        page=flask_quiz.next_num) \
        if flask_quiz.has_next else None
    flask_quiz_prev_url = url_for(
        'teacher.review_chapter_quiz',
        page=flask_quiz.prev_num) \
        if flask_quiz.has_prev else None
    all_flask_quiz = len(ChapterQuiz.query.all())
    return render_template(
        'teacher/course/flask/reviews/flask_quiz.html',
        teacher=teacher,
        title='Review Chapter Quiz',
        flask_quiz=flask_quiz.items,
        flask_quiz_next_url=flask_quiz_next_url,
        flask_quiz_prev_url=flask_quiz_prev_url,
        all_flask_quiz=all_flask_quiz
        )


@bp.route('/flask/quiz/<int:id>/allow')
def allow_flask_quiz(id):
    quiz = ChapterQuiz.query.get_or_404(id)
    quiz.allowed_status = True
    db.session.commit()
    flash(f'Flask quiz {id} has been allowed.')
    return redirect(url_for(
        'teacher.review_chapter_quiz'
        )
    )


@bp.route('/flask/quiz/<int:id>/delete')
def delete_flask_quiz(id):
    quiz = ChapterQuiz.query.get_or_404(id)
    db.session.delete(quiz)
    db.session.commit()
    flash(f'Flask quiz {id} has been deleted.')
    return redirect(url_for(
        'teacher.review_chapter_quiz'
        )
    )

# ========================================
# END OF COMMENTS MANAGEMENT ROUTES
# ========================================

# ========================================
# REVIEW GENERAL MULTIPLE CHOICE QUESTIONS
# ========================================


@bp.route('/flask/general-mulitple-choices-quiz/review')
@login_required
def review_general_mulitiple_choices_quiz():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    flask_quiz = GeneralMultipleChoicesQuiz.query.order_by(
        GeneralMultipleChoicesQuiz.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'teacher.review_general_mulitiple_choices_quiz',
        page=flask_quiz.next_num) \
        if flask_quiz.has_next else None
    prev_url = url_for(
        'teacher.review_general_mulitiple_choices_quiz',
        page=flask_quiz.prev_num) \
        if flask_quiz.has_prev else None
    all_flask_quiz = len(GeneralMultipleChoicesQuiz.query.all())
    return render_template(
        'teacher/course/flask/reviews/general_multiple_choices_quiz.html',
        teacher=teacher,
        title='Review General Multiple Choices Quizzes',
        flask_quiz=flask_quiz.items,
        next_url=next_url,
        prev_url=prev_url,
        all_flask_quiz=all_flask_quiz
        )


@bp.route('/flask/general-mulitple-choices-quiz/<int:id>/allow')
def allow_review_general_mulitiple_choices_quiz(id):
    quiz = GeneralMultipleChoicesQuiz.query.get_or_404(id)
    quiz.allowed_status = True
    db.session.commit()
    flash(f'General flask quiz {id} has been allowed.')
    return redirect(url_for(
        'teacher.review_general_mulitiple_choices_quiz'
        )
    )


@bp.route('/flask/general-mulitple-choices-quiz/<int:id>/delete')
def delete_review_general_mulitiple_choices_quiz(id):
    quiz = GeneralMultipleChoicesQuiz.query.get_or_404(id)
    db.session.delete(quiz)
    db.session.commit()
    flash(f'General flask quiz {id} has been deleted.')
    return redirect(url_for(
        'teacher.review_general_mulitiple_choices_quiz'
        )
    )

# ===============================================
# END OF REVIEW GENERAL MULTIPLE CHOICE QUESTIONS
# ===============================================
