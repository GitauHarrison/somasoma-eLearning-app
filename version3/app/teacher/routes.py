from app import db
from datetime import datetime
from app.teacher import bp
from flask_login import login_required, current_user
from flask import render_template, flash, request, redirect, url_for,\
    current_app
from app.models import Teacher, TeacherCommunityComment
from app.teacher.forms import EditProfileForm, CommentForm, EmptyForm


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

    # My teacher community comments
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
    return render_template(
        'teacher/dashboard_teacher.html',
        teacher=teacher,
        comments=comments.items,
        my_comments=my_comments.items,
        next_url=next_url,
        prev_url=prev_url,
        my_next_url=my_next_url,
        my_prev_url=my_prev_url,
        comment_form=comment_form
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
