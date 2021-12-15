from app import app, db
from flask import render_template


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        'errors/404.html',
        title='Page Not found'
        ), 404


@app.errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    return render_template(
        'errors/500.html',
        title='Unexpected Error'
        ), 500
