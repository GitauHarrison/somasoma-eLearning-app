from app import db
from datetime import datetime
from app.teacher import bp
from flask_login import login_required, current_user
from flask import render_template
from app.models import Teacher


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
