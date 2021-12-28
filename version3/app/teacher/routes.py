from app import db
from datetime import datetime
from app.teacher import bp
from flask_login import login_required, current_user
from flask import render_template, flash, request, redirect, url_for
from app.models import Teacher
from app.teacher.forms import EditProfileForm


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.teacher_last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/dashboard')
@login_required
def dashboard_teacher():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    return render_template(
        'teacher/dashboard_teacher.html',
        teacher=teacher
        )


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
