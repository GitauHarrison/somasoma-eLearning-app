from app.models import Teacher
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError

# Profile form


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

    def validate_email(self, teacher_email):
        if teacher_email.data != self.original_email:
            teacher = Teacher.query.filter_by(
                teacher_email=self.email.data).first()
            if teacher is not None:
                raise ValidationError('Please use a different email.')

# Comment form


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment',
                            validators=[DataRequired()]
                            )
    submit = SubmitField('Post')


# Follow form


class EmptyForm(FlaskForm):
    submit = SubmitField('Post')

# Course overview form


class WebDevelopmentOverviewForm(FlaskForm):
    title = SelectField(
        'Course Title',
        choices=[
            ('Flask Web Development', 'Flask Web Development'),
            ('Python DSA', 'Python DSA'),
            ('Data Science', 'Data Science'),
            ('Machine Learning', 'Machine Learning')
            ],
        validators=[DataRequired()]
        )
    body = TextAreaField(
        'Course Overview',
        validators=[DataRequired()]
        )
    youtube_link = StringField(
        'Youtube Link',
        validators=[DataRequired()],
        render_kw={"placeholder": "Youtube Embed Link"}
        )
    submit = SubmitField('Post')


class TableOfContentsForm(FlaskForm):
    title = SelectField(
        'Course Title',
        choices=[
            ('Flask Web Development', 'Flask Web Development'),
            ('Python DSA', 'Python DSA'),
            ('Data Science', 'Data Science'),
            ('Machine Learning', 'Machine Learning')
            ],
        validators=[DataRequired()]
        )
    chapter = StringField(
        'Chapter',
        validators=[DataRequired()],
        render_kw={"placeholder": "Chapter 1: Introduction"}
        )
    link = StringField(
        'Chapter Link',
        validators=[DataRequired()],
        render_kw={"placeholder": "https://link/to/chapter"}
        )
    submit = SubmitField('Post')


class ChapterForm(FlaskForm):
    course = SelectField(
        'Course Title',
        choices=[
            ('Flask Web Development', 'Flask Web Development'),
            ('Python DSA', 'Python DSA'),
            ('Data Science', 'Data Science'),
            ('Machine Learning', 'Machine Learning')
            ],
        validators=[DataRequired()]
        )
    chapter = StringField(
        'Chapter Title',
        validators=[DataRequired()],
        render_kw={"placeholder": "Chapter 1: Introduction"}
        )
    overview = TextAreaField(
        'Chapter Overview',
        validators=[DataRequired()]
        )
    accomplish = TextAreaField(
        'What You Will Accomplish',
        validators=[DataRequired()]
        )
    youtube_link = StringField(
        'YouTube Link',
        validators=[DataRequired()],
        render_kw={
            "placeholder": "https://www.youtube.com"
            }
        )
    conclusion = TextAreaField(
        'Conclusion',
        validators=[DataRequired()]
        )
    objective_1 = StringField(
        'Objective 1',
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Student can create a flask project structure"
            }
        )
    objective_2 = StringField(
        'Objective 2',
        validators=[DataRequired()],
        render_kw={"placeholder": "Student can create project instance"}
        )
    objective_3 = StringField(
        'Objective 3',
        validators=[DataRequired()],
        render_kw={"placeholder": "Student can add a flask entry point"}
        )
    objective_4 = StringField(
        'Objective 4',
        validators=[DataRequired()],
        render_kw={"placeholder": "Student can display a welcome message"}
        )
    objective_5 = StringField(
        'Objective 5',
        validators=[DataRequired()],
        render_kw={"placeholder": "Student can start a flask server"}
        )
    submit = SubmitField('Post')
