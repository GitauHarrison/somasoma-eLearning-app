from app import db
from flask import render_template
from app.errors import bp


@bp.errorhandler(404)
def page_not_found(e):
    return render_template(
        'errors/404.html',
        title='Page Not found'
        ), 404


@bp.errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    return render_template(
        'errors/500.html',
        title='Unexpected Error'
        ), 500
