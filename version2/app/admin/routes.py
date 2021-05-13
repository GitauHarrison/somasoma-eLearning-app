from flask import flash, redirect, url_for
from app import db
from app.admin import bp
from app.models import Client


@bp.route('/profile/client/<username>/delete-account')
def delete_client_account(username):
    client = Client.query.filter_by(username=username).first_or_404()
    db.session.delete(client)
    db.session.commit()
    flash(f'Your client account {client.username} was successfully deleted')
    return redirect(url_for('main.home'))
