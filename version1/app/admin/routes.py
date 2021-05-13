from flask import flash, redirect, url_for
from app import db
from app.admin import bp
from app.models import Parent, Student, Teacher


@bp.route('/profile/parent/<username>/delete-account')
def delete_parent_account(username):
    parent = Parent.query.filter_by(username=username).first_or_404()
    db.session.delete(parent)
    db.session.commit()
    flash(f'Your parent account {parent.username} was successfully deleted')
    return redirect(url_for('main.home'))


@bp.route('/profile/student/<username>/delete-account')
def delete_student_account(username):
    student = Student.query.filter_by(username=username).first_or_404()
    db.session.delete(student)
    db.session.commit()
    flash(f'Your student account {student.username} was successfully deleted')
    return redirect(url_for('main.home'))


@bp.route('/profile/teacher/<username>/delete-account')
def delete_teacher_account(username):
    teacher = Teacher.query.filter_by(username=username).first_or_404()
    db.session.delete(teacher)
    db.session.commit()
    flash(f'Your teacher account {teacher.username} was successfully deleted')
    return redirect(url_for('main.home'))
