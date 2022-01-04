from app import db
from datetime import datetime
from app.teacher import bp
from flask_login import login_required, current_user
from flask import render_template, flash, request, redirect, url_for,\
    current_app
from app.models import Teacher, TeacherCommunityComment, Student,\
    CommunityComment, WebDevelopmentOverview, TableOfContents, Chapter,\
    WebDevChapter1Comment, ChapterObjectives, ChapterQuiz
from app.teacher.forms import EditProfileForm, CommentForm, EmptyForm,\
    WebDevelopmentOverviewForm, TableOfContentsForm, ChapterForm,\
    ChapterObjectivesForm, ChapterQuizForm
from app.teacher.email import send_live_flask_chapter_1_comment_email


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
def dashboard_all_students():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name).first()
    students = Student.query.filter_by(
        student_course=teacher.teacher_course).order_by(
        Student.student_last_seen.desc()).all()
    all_students = len(students)
    return render_template(
        'teacher/all_students.html',
        title='All Students',
        teacher=teacher,
        students=students,
        all_students=all_students
        )


@bp.route('/dashboard/explore-teachers')
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


@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_teacher():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    page = request.args.get('page', 1, type=int)

    # List all students
    students = Student.query.filter_by(
        student_course=teacher.teacher_course).order_by(
        Student.student_last_seen.desc()).all()
    all_students = len(students)

    # Explore teacher community comments
    comments = TeacherCommunityComment.query.order_by(
        TeacherCommunityComment.timestamp.desc()
        ).paginate(
            page,
            current_app.config['POSTS_PER_PAGE'],
            False
            )
    next_url = url_for(
                    'teacher.dashboard_teacher',
                    page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'teacher.dashboard_teacher',
        page=comments.prev_num) \
        if comments.has_prev else None

    # Following: Teacher community comments
    my_comments = current_user.followed_comments().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    my_next_url = url_for(
                    'teacher.dashboard_teacher',
                    page=comments.next_num) \
        if comments.has_next else None
    my_prev_url = url_for(
        'teacher.dashboard_teacher',
        page=comments.prev_num) \
        if comments.has_prev else None

    # Form: Explore teacher community comments
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = TeacherCommunityComment(
            body=comment_form.comment.data,
            author=current_user
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('teacher.dashboard_teacher'))

    # Students community comments
    student_comments = CommunityComment.query.order_by(
        CommunityComment.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    student_next_url = url_for(
                    'teacher.dashboard_teacher',
                    page=comments.next_num) \
        if comments.has_next else None
    student_prev_url = url_for(
        'teacher.dashboard_teacher',
        page=comments.prev_num) \
        if comments.has_prev else None

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
            chapter_review_link=chapter_form.chapter_review_link.data,
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

    # Chapter objectives
    chapter_objectives_form = ChapterObjectivesForm()
    if chapter_objectives_form.validate_on_submit():
        chapter_objective = ChapterObjectives(
            course=chapter_objectives_form.course.data,
            chapter=chapter_objectives_form.chapter.data,
            review_objectives_link=chapter_objectives_form.review_objectives_link.data,
            objective_1=chapter_objectives_form.objective_1.data,
            objective_2=chapter_objectives_form.objective_2.data,
            objective_3=chapter_objectives_form.objective_3.data,
            objective_4=chapter_objectives_form.objective_4.data,
            objective_5=chapter_objectives_form.objective_5.data
        )
        db.session.add(chapter_objective)
        db.session.commit()
        flash('Chapter objectives have been added!', 'success')
        return redirect(url_for('teacher.review_flask_objectives'))
    all_objectives = ChapterObjectives.query.filter_by(
        course=teacher.teacher_course).all()

    # Chapter Quiz
    chapter_quiz_form = ChapterQuizForm()
    if chapter_quiz_form.validate_on_submit():
        chapter_quiz = ChapterQuiz(
            course=chapter_quiz_form.course.data,
            chapter=chapter_quiz_form.chapter.data,
            review_quiz_link=chapter_quiz_form.review_quiz_link.data,
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
    all_quizzes = ChapterQuiz.query.filter_by(
        course=teacher.teacher_course).all()

    # Length
    course_chapters = Chapter.query.filter_by(
        course=teacher.teacher_course).all()
    all_chapters = len(Chapter.query.all())
    all_toc = len(TableOfContents.query.all())
    all_course_overview = len(WebDevelopmentOverview.query.all())
    all_chapter_objectives = len(ChapterObjectives.query.all())
    all_chapter_quizzes = len(ChapterQuiz.query.all())

    return render_template(
        'teacher/dashboard_teacher.html',
        teacher=teacher,

        # Length
        all_chapters=all_chapters,
        all_toc=all_toc,
        all_course_overview=all_course_overview,
        all_chapter_objectives=all_chapter_objectives,
        all_students=all_students,
        all_chapter_quizzes=all_chapter_quizzes,

        # All comments
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,

        # Followed comments
        my_comments=my_comments.items,
        my_next_url=my_next_url,
        my_prev_url=my_prev_url,

        # Form: Explore teacher community comments
        comment_form=comment_form,

        # Students taking teacher's course
        students=students,

        # Students community comments
        student_comments=student_comments.items,
        student_next_url=student_next_url,
        student_prev_url=student_prev_url,

        # Manage Course Overview
        course_overview_form=course_overview_form,

        # Manage Course Table of Contents
        table_of_contents_form=table_of_contents_form,

        # Chapters
        chapter_form=chapter_form,
        course_chapters=course_chapters,

        # Chapter objectives
        chapter_objectives_form=chapter_objectives_form,
        all_objectives=all_objectives,

        # Chapter Quiz
        chapter_quiz_form=chapter_quiz_form,
        all_quizzes=all_quizzes
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
        return redirect(url_for('teacher.dashboard_teacher'))
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
        'teacher.dashboard_teacher', teacher_full_name=teacher_full_name,
        _anchor="teacher-comments",
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'teacher.dashboard_teacher', teacher_full_name=teacher_full_name,
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


@bp.route('/profile/student/<student_full_name>')
@login_required
def profile_student(student_full_name):
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    student = Student.query.filter_by(
        student_full_name=student_full_name
        ).first()
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
        all_comments=all_comments
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
            return redirect(url_for('teacher.dashboard_teacher'))
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
        return redirect(url_for('teacher.dashboard_teacher'))


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
            return redirect(url_for('teacher.dashboard_teacher'))
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
        return redirect(url_for('teacher.dashboard_teacher'))

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
                    'teacher.dashboard_teacher',
                    page=course_overview.next_num) \
        if course_overview.has_next else None
    course_overview_prev_url = url_for(
        'teacher.dashboard_teacher',
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
# COURSE MANAGEMENT ROUTES
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


# Flask chapter objectives

@bp.route('/flask/objectives/review')
@login_required
def review_flask_objectives():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    flask_objectives = ChapterObjectives.query.order_by(
        ChapterObjectives.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    flask_objectives_next_url = url_for(
        'teacher.review_flask_objectives',
        page=flask_objectives.next_num) \
        if flask_objectives.has_next else None
    flask_objectives_prev_url = url_for(
        'teacher.review_flask_objectives',
        page=flask_objectives.prev_num) \
        if flask_objectives.has_prev else None
    objectives = ChapterObjectives.query.filter_by(
        course=teacher.teacher_course).all()
    all_flask_objectives = len(ChapterObjectives.query.all())
    return render_template(
        'teacher/course/flask/reviews/flask_objectives.html',
        teacher=teacher,
        title='Review Chapter Objectives',
        flask_objectives=flask_objectives.items,
        flask_objectives_next_url=flask_objectives_next_url,
        flask_objectives_prev_url=flask_objectives_prev_url,
        all_flask_objectives=all_flask_objectives,
        objectives=objectives
        )


@bp.route('/flask/objectives/<int:id>/allow')
def allow_flask_objectives(id):
    objective = ChapterObjectives.query.get_or_404(id)
    objective.allowed_status = True
    db.session.commit()
    flash(f'Flask objective {id} has been allowed.')
    return redirect(url_for(
        'teacher.review_flask_objectives'
        )
    )


@bp.route('/flask/objectives/<int:id>/delete')
def delete_flask_objectives(id):
    objective = ChapterObjectives.query.get_or_404(id)
    db.session.delete(objective)
    db.session.commit()
    flash(f'Flask objective {id} has been deleted.')
    return redirect(url_for(
        'teacher.review_flask_objectives'
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
