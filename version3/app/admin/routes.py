from app import db
from app.admin import bp
from flask import render_template, redirect, url_for, flash, request,\
    current_app
from app.admin.forms import EditProfileForm
from app.auth.forms import TeacherRegistrationForm
from app.models import CommunityComment, Admin, Student, Teacher, Parent, User
from flask_login import current_user, login_required
from datetime import datetime


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.admin_last_seen = datetime.utcnow()
        db.session.commit()


# Dashboard

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_admin():
    admin = Admin.query.filter_by(
        admin_full_name=current_user.admin_full_name
        ).first()
    students = Student.query.order_by(Student.student_last_seen.desc()).all()
    teachers = Teacher.query.order_by(Teacher.teacher_last_seen.desc()).all()
    parents = Parent.query.order_by(Parent.parent_last_seen.desc()).all()
    all_students = len(Student.query.all())
    all_teachers = len(Teacher.query.all())
    all_parents = len(Parent.query.all())

    # Teacher Registration
    teacher_form = TeacherRegistrationForm()
    if teacher_form.validate_on_submit():
        teacher = Teacher(
            teacher_full_name=teacher_form.teacher_full_name.data,
            teacher_email=teacher_form.teacher_email.data,
            teacher_phone=teacher_form.teacher_phone.data,
            teacher_residence=teacher_form.teacher_residence.data,
            teacher_course=teacher_form.teacher_course.data
        )
        teacher.set_password(teacher_form.teacher_password.data)
        db.session.add(teacher)
        db.session.commit()
        flash('Teacher successfully registered')
        return redirect(url_for('admin.dashboard_admin'))
    # End of teacher registration

    return render_template(
        'admin/dashboard_admin.html',
        admin=admin,
        students=students,
        teachers=teachers,
        parents=parents,
        all_students=all_students,
        all_teachers=all_teachers,
        all_parents=all_parents,
        teacher_form=teacher_form
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


# Delete account routes


@bp.route('/student/<student_id>/delete-account')
def delete_account_student(student_id):
    student = Student.query.filter_by(
        id=student_id
        ).first()
    db.session.delete(student)
    db.session.commit()
    flash(f'Student {student_id} account has been deleted!')
    return redirect(url_for('admin.dashboard_admin'))


@bp.route('/teacher/<teacher_id>/delete-account')
def delete_account_teacher(teacher_id):
    teacher = Teacher.query.filter_by(
        id=teacher_id
        ).first()
    db.session.delete(teacher)
    db.session.commit()
    flash(f'Teacher {teacher_id} account has been deleted!')
    return redirect(url_for('admin.dashboard_admin'))


@bp.route('/parent/<parent_id>/delete-account')
def delete_account_parent(parent_id):
    parent = Parent.query.filter_by(
        id=parent_id
        ).first()
    db.session.delete(parent)
    db.session.commit()
    flash(f'Parent {parent_id} account has been deleted!')
    return redirect(url_for('admin.dashboard_admin'))
