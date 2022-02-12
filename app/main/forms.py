from app.models import Student, FlaskStudentStories
from flask_wtf import FlaskForm, RecaptchaField
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_wtf.file import FileField, FileAllowed

# Comment form


class CommentForm(FlaskForm):
    comment = PageDownField(
        'Comment',
        validators=[DataRequired()],
        render_kw={"placeholder": "Markdown enabled"}
        )
    submit = SubmitField('Post')


# Anonymous Comment form


class AnonymousCommentForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Valid Email Address"})
    comment = PageDownField(
        'Comment',
        validators=[DataRequired()],
        render_kw={"placeholder": "Markdown enabled"})
    recaptcha = RecaptchaField()
    submit = SubmitField('Post')


# Follow form


class EmptyForm(FlaskForm):
    submit = SubmitField('Post')


# Profile form


class EditProfileForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Valid Email Address"})
    about_me = StringField(
        'About me',
        validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_student_email(self, email):
        if email.data != self.original_email:
            student = Student.query.filter_by(student_email=self.email.data).first()
            if student is not None:
                raise ValidationError('Please use a different email.')


# ========================================
# OBJECTIVES FORM
# ========================================

# Web Development Objectives


class Chapter1WebDevelopmentForm(FlaskForm):
    objective_1 = BooleanField('You can understand what HTML is used for in a web application')
    objective_2 = BooleanField('You can create an empty HTML page')
    objective_3 = BooleanField('You can add the general syntax of a HTML page')
    objective_4 = BooleanField('You can add the head section of a HTML page')
    objective_5 = BooleanField('You can add the body section of a HTML page')
    objective_6 = BooleanField('You can understand the basic tags used in HTML')
    objective_7 = BooleanField('You can add comments to a HTML page')
    submit = SubmitField('Submit')

# ========================================
# END OF OBJECTIVES FORM
# ========================================

# ========================================
# QUIZZES FORM
# ========================================


class QuizForm(FlaskForm):
    title = StringField('Question', validators=[DataRequired()])
    body = PageDownField(
        'Description',
        validators=[DataRequired()],
        render_kw={"placeholder": "Markdown enabled"})
    submit = SubmitField('Submit')


class Chapter1QuizOptionsForm(FlaskForm):
    option_1 = BooleanField('Option 1')
    option_2 = BooleanField('Option 2')
    option_3 = BooleanField('Option 3')
    option_4 = BooleanField('Option 4')
    submit = SubmitField('Submit')

# ========================================
# END OF QUIZZES FORM
# ========================================

# ========================================
# STUDENT STORIES FORM
# ========================================


class StudentStoriesForm(FlaskForm):
    student_image = FileField(
        'Student Image',
        validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    username = StringField(
        'Full Name',
        validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Valid Email Address"})
    body = PageDownField(
        'Your Story',
        validators=[DataRequired()],
        render_kw={"placeholder": "Markdown enabled"})
    recaptcha = RecaptchaField()
    submit = SubmitField('Update')

    def validate_email(self, email):
        student = FlaskStudentStories.query.filter_by(email=email.data).first()
        if student:
            raise ValidationError(
                'Email already taken. Please choose a different one.')

# ========================================
# END OF STUDENT STORIES FORM
# ========================================
