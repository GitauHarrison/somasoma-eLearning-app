from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import Parent, Student, Teacher


# ------------
# User Profile
# ------------

class ParentEditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=300)])
    submit = SubmitField('Update')

    def __init__(self, original_username, *args, **kwargs):
        super(ParentEditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            parent = Parent.query.filter_by(username=self.username.data).first()
            if parent is not None:
                raise ValidationError('Please use a different username.')


class StudentEditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=300)])
    submit = SubmitField('Update')

    def __init__(self, original_username, *args, **kwargs):
        super(StudentEditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            student = Student.query.filter_by(username=self.username.data).first()
            if student is not None:
                raise ValidationError('Please use a different username.')


class TeacherEditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=300)])
    submit = SubmitField('Update')

    def __init__(self, original_username, *args, **kwargs):
        super(TeacherEditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            teacher = Teacher.query.filter_by(username=self.username.data).first()
            if teacher is not None:
                raise ValidationError('Please use a different username.')


# ------------------------
# Comments Form
# ------------------------


class CommentForm(FlaskForm):
    body = TextAreaField('Your Comment', validators=[DataRequired()])
    submit = SubmitField('Post')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
