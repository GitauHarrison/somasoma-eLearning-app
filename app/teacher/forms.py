from app.models import Teacher
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_wtf.file import FileField, FileAllowed

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

# Private messages form


class PrivateMessageForm(FlaskForm):
    message = PageDownField(
        'Message',
        validators=[DataRequired(), Length(min=0, max=140)],
        render_kw={"placeholder": "Message: Markdown supported"}
        )
    submit = SubmitField('Send')

# Comment form


class CommentForm(FlaskForm):
    comment = PageDownField(
        'Comment',
        validators=[DataRequired()],
        render_kw={"placeholder": "Markdown enabled"}
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
    body = PageDownField(
        'Course Overview',
        validators=[DataRequired()],
        render_kw={"placeholder": "Markdown enabled"}
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
        render_kw={"placeholder": "web-development/chapter-1"}
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
    chapter_link = StringField(
        'Live Chapter Link',
        validators=[DataRequired()],
        render_kw={"placeholder": "chapter-1"}
        )
    comment_moderation_link = StringField(
        'Comment Moderation Link',
        validators=[DataRequired()],
        render_kw={"placeholder": "flask/chapter-1/comments/review"}
        )
    overview = PageDownField(
        'Chapter Overview',
        validators=[DataRequired()],
        render_kw={"placeholder": "Markdown enabled"}
        )
    accomplish = TextAreaField(
        'What You Will Accomplish',
        validators=[DataRequired()]
        )
    youtube_link = StringField(
        'YouTube Link',
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Embed Code: YwBxwB8u9uY"
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


class ChapterQuizForm(FlaskForm):
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
    quiz_1 = StringField(
        'Quiz 1',
        validators=[DataRequired()],
        render_kw={"placeholder": "What is HTML in full"}
        )
    quiz_2 = StringField(
        'Quiz 2',
        validators=[DataRequired()],
        render_kw={"placeholder": "What is CSS in full"}
        )
    quiz_3 = StringField(
        'Quiz 3',
        validators=[DataRequired()],
        render_kw={"placeholder": "What is Python in full"}
        )
    quiz_4 = StringField(
        'Quiz 4',
        validators=[DataRequired()],
        render_kw={"placeholder": "What is Flask in full"}
        )
    quiz_5 = StringField(
        'Quiz 5',
        validators=[DataRequired()],
        render_kw={"placeholder": "What is SQL in full"}
        )
    submit = SubmitField('Post')


class BlogArticlesForm(FlaskForm):
    article_image = FileField(
        'Blog Image',
        validators=[DataRequired(), FileAllowed(['jpg', 'png', 'svg'])],
        )
    article_name = StringField(
        'Article Name',
        validators=[DataRequired()]
    )
    body = PageDownField(
        'Body',
        validators=[DataRequired()],
        render_kw={"placeholder": "Markdown enabled"}
        )
    link = StringField(
        'Article Link',
        validators=[DataRequired()]
    )
    submit = SubmitField('Update')


class EventsForm(FlaskForm):
    event_image = FileField(
        'Event Image',
        validators=[DataRequired(), FileAllowed(['jpg', 'png'])],
        )
    event_title = StringField(
        'Title',
        validators=[DataRequired(), Length(min=2, max=100)]
        )
    event_body = PageDownField(
        'Body',
        validators=[DataRequired()],
        render_kw={"placeholder": "Markdown enabled"}
        )
    event_date = StringField(
        'Event Date',
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={'placeholder': 'December 26, 2021'}
        )
    event_time = StringField(
        'Event Time',
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={'placeholder': '10:00 AM - 12:00 PM'}
        )
    event_location = StringField(
        'Event Location',
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={'placeholder': 'Online'}
        )
    event_link = StringField(
        'Link',
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={'placeholder': 'https://www.meet.google.com'}
        )
    submit = SubmitField('Update')
