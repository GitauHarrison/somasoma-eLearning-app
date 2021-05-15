from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import Client


# ------------
# User Profile
# ------------

class ClientEditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=300)])
    submit = SubmitField('Update')

    def __init__(self, original_username, *args, **kwargs):
        super(ClientEditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            client = Client.query.filter_by(student_username=self.username.data).first()
            if client is not None:
                raise ValidationError('Please use a different username.')


# ------------------------
# Comments Form
# ------------------------


class CommentForm(FlaskForm):
    body = TextAreaField('Your Comment', validators=[DataRequired()])
    submit = SubmitField('Post')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
