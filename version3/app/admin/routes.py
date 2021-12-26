from app import db
from app.admin import bp
from flask import render_template, redirect, url_for, flash, request,\
    current_app
from app.admin.forms import EditProfileForm
from app.models import CommunityComment, Admin
from flask_login import current_user, login_required
from datetime import datetime


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.student_last_seen = datetime.utcnow()
        db.session.commit()


# Dashboard

@bp.route('/dashboard')
@login_required
def dashboard_admin():
    admin = Admin.query.filter_by(
        admin_full_name=current_user.admin_full_name
        ).first()
    return render_template(
        'admin/dashboard_admin.html',
        admin=admin
        )


# Profile routes


@bp.route('/profile/<admin_full_name>')
@login_required
def profile_admin(admin_full_name):
    admin = Admin.query.filter_by(
        admin_full_name=admin_full_name
        ).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = admin.comments.order_by(
        CommunityComment.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'admin.dashboard_admin', admin_full_name=admin_full_name,
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'admin.dashboard_admin', admin_full_name=admin_full_name,
        page=comments.prev_num) \
        if comments.has_prev else None
    return render_template(
        'admin/profile_admin.html',
        title='Profile',
        admin=admin,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url
    )

# Edit profile routes


@bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile_admin():
    admin = Admin.query.filter_by(
        admin_full_name=current_user.admin_full_name
        ).first()
    form = EditProfileForm(current_user.admin_email)
    if form.validate_on_submit():
        current_user.admin_email = form.email.data
        current_user.admin_about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('admin.dashboard_admin'))
    elif request.method == 'GET':
        form.email.data = current_user.admin_email
        form.about_me.data = current_user.admin_about_me
    return render_template(
        'admin/edit_profile_admin.html',
        title='Edit Profile',
        form=form,
        admin=admin
    )
