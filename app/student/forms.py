from app.models import Student
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField,\
    SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError

# Comment form


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment',
                            validators=[DataRequired()]
                            )
    submit = SubmitField('Post')


# Follow form


class EmptyForm(FlaskForm):
    submit = SubmitField('Post')


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

    def validate__email(self, student_email):
        if student_email.data != self.original_email:
            student = Student.query.filter_by(
                student_email=self.email.data).first()
            if student is not None:
                raise ValidationError('Please use a different email.')


# ========================================
# OBJECTIVES FORM
# ========================================

# Web Development Objectives


class ChapterObjectivesForm(FlaskForm):
    objective_1 = BooleanField('Student can create a flask project structure',)
    objective_2 = BooleanField('Student can create a project\'s instance',)
    objective_3 = BooleanField('Student can create a flask entry point',)
    objective_4 = BooleanField('Student can display a welcome message',)
    objective_5 = BooleanField('Student can start a flask server',)
    submit = SubmitField('Submit')

# ========================================
# END OF OBJECTIVES FORM
# ========================================

# ========================================
# QUIZZES FORM
# ========================================


class QuizForm(FlaskForm):
    title = StringField('Question', validators=[DataRequired()])
    body = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Chapter1Quiz1OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('To display content in a webpage', 'To display content in a webpage'),
            ('To hack a browser', 'To hack a browser'),
            ('To style the contents of a webpage', 'To style the contents of a webpage'),
            ('To hack the server', 'To hack the server')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


class Chapter1Quiz2OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('To inspect a webpage', 'To inspect a webpage'),
            ('To hack an app', 'To hack an app'),
            ('To style the contents of a webpage', 'To style the contents of a webpage'),
            ('To query a database', 'To query a database')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


class Chapter1Quiz3OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('To create tables in a webpage', 'To create tables in a webpage'),
            ('To create a database', 'To create a database'),
            ('To create beautiful animations', 'To create beautiful animations'),
            ('To style a website', 'To style a website')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


class Chapter1Quiz4OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('To improve the security of an app', 'To improve the security of an app'),
            ('To query a database', 'To query a database'),
            ('To enhance the creation of an app', 'To enhance the creation of an app'),
            ('To display content in a webpage', 'To display content in a webpage')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


# ========================================
# END OF QUIZZES FORM
# ========================================
