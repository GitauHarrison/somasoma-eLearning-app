from app import db
from datetime import datetime
from app.teacher import bp
from flask_login import login_required, current_user
from flask import render_template, flash, request, redirect, url_for,\
    current_app
from app.models import Teacher, TeacherCommunityComment, Student,\
    CommunityComment, WebDevelopmentOverview,TableOfContents
from app.teacher.forms import EditProfileForm, CommentForm, EmptyForm,\
    WebDevelopmentOverviewForm, TableOfContentsForm


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.teacher_last_seen = datetime.utcnow()
        db.session.commit()


# Dashboard route


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

    return render_template(
        'teacher/dashboard_teacher.html',
        teacher=teacher,

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
        all_students=all_students,

        # Students community comments
        student_comments=student_comments.items,
        student_next_url=student_next_url,
        student_prev_url=student_prev_url,

        # Manage Course Overview
        course_overview_form=course_overview_form,

        # Manage Course Table of Contents
        table_of_contents_form=table_of_contents_form
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
        allowed_status=True).order_by(
        TableOfContents.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    course_toc_next_url = url_for(
        'teacher.review_course_overview',
        page=course_toc.next_num) \
        if course_toc.has_next else None
    course_toc_prev_url = url_for(
        'teacher.review_course_overview',
        page=course_toc.prev_num) \
        if course_toc.has_prev else None

    return render_template(
        'teacher/course/flask/reviews/flask_overview.html',
        teacher=teacher,
        title='Review Course Overview',
        course_overview=course_overview.items,
        course_overview_next_url=course_overview_next_url,
        course_overview_prev_url=course_overview_prev_url,
        course_toc=course_toc.items,
        course_toc_next_url=course_toc_next_url,
        course_toc_prev_url=course_toc_prev_url
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
    return render_template(
        'teacher/course/flask/reviews/flask_toc.html',
        teacher=teacher,
        title='Review Table of Contents',
        course_toc=course_toc.items,
        course_toc_next_url=course_toc_next_url,
        course_toc_prev_url=course_toc_prev_url
        )


@bp.route('/course/toc/<chapter>/allow')
def allow_table_of_contents(chapter):
    toc = TableOfContents.query.filter_by(
        chapter=chapter
        ).first()
    toc.allowed_status = True
    db.session.commit()
    flash('Table of contents has been allowed.')
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
    flash('Table of contents has been deleted.')
    return redirect(url_for(
        'teacher.review_table_of_contents'
        )
    )

# ========================================
# COURSE MANAGEMENT ROUTES
# ========================================
