from flask import flash, redirect, url_for
from app import db
from app.admin import bp
from app.models import Client, Teacher


@bp.route('/profile/client/<username>/delete-account')
def delete_client_account(username):
    client = Client.query.filter_by(student_username=username).first_or_404()
    db.session.delete(client)
    db.session.commit()
    flash(f'Your client account {client.student_username} was successfully deleted')
    return redirect(url_for('main.home'))


@bp.route('/profile/teacher/<username>/delete-account')
def delete_teacher_account(username):
    teacher = Teacher.query.filter_by(teacher_username=username).first_or_404()
    db.session.delete(teacher)
    db.session.commit()
    flash(f'Your client account {teacher.teacher_username} was successfully deleted')
    return redirect(url_for('main.home'))
