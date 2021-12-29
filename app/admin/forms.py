from app.models import Admin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_wtf.file import FileField, FileAllowed


class EditProfileForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Valid Email Address"}
                        )
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_admin_email(self, email):
        if email.data != self.original_email:
            admin = Admin.query.filter_by(admin_email=self.email.data).first()
            if admin is not None:
                raise ValidationError('Please use a different email.')


class CoursesForm(FlaskForm):
    course_image = FileField(
        'Courses Image',
        validators=[DataRequired(), FileAllowed(['jpg', 'png'])],
        )
    title = StringField(
        'Title',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    body = TextAreaField(
        'Body',
        validators=[DataRequired()]
        )
    overview = TextAreaField(
        'Overview',
        validators=[DataRequired()]
    )
    next_class_date = StringField(
        'Next Class Date',
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={'placeholder': 'December 26, 2021'}
        )
    link = StringField(
        'Link',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    submit = SubmitField('Update')


class BlogArticlesForm(FlaskForm):
    article_image = FileField(
        'Blog Image',
        validators=[DataRequired(), FileAllowed(['jpg', 'png', 'svg'])],
        )
    article_name = StringField(
        'Article Name',
        validators=[DataRequired()]
    )
    body = TextAreaField(
        'Body',
        validators=[DataRequired()]
        )
    link = StringField(
        'Article Link',
        validators=[DataRequired()]
    )
    submit = SubmitField('Update')
