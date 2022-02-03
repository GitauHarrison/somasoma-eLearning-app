from app.models import Student
from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, BooleanField, TextAreaField,\
    SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError

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
    objective_1 = BooleanField('You can install flask into your application',)
    objective_2 = BooleanField('You can create a simple flask application structure',)
    objective_3 = BooleanField('You can start the flask server',)
    objective_4 = BooleanField('You can display some text on your browser',)
    objective_5 = BooleanField('You can exit your flask server',)
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
        render_kw={"placeholder": "Markdown enabled"}
        )
    submit = SubmitField('Submit')


# Quiz 1


class Chapter1Quiz1OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('pip3 flask', 'pip3 flask'),
            ('install flask', 'install flask'),
            ('pip3 install flask', 'pip3 install flask'),
            ('python3 -m flask', 'python3 -m flask'),
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


class Chapter2Quiz1OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('To display content', 'To display content'),
            ('It has no purpose', 'It has no purpose'),
            ('To query a database', 'To query a database'),
            ('To style page content', 'To style page content'),
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


class Chapter3Quiz1OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('To make a page look beautiful', 'To make a page look beautiful'),
            ('It has no purpose', 'It has no purpose'),
            ('It makes it easier to work with flask', 'It makes it easier to work with flask'),
            ('To collect user data', 'To collect user data'),
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


# Quiz 2


class Chapter1Quiz2OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('Flask', 'Flask'),
            ('Java', 'Java'),
            ('Python', 'Python'),
            ('HTML', 'HTML')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


class Chapter2Quiz2OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('Flask', 'Flask'),
            ('Java', 'Java'),
            ('Python', 'Python'),
            ('HTML', 'HTML')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


class Chapter3Quiz2OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('Flask', 'Flask'),
            ('Flask-wtf', 'Flask-wtf'),
            ('SECRET_KEY', 'SECRET_KEY'),
            ('Flask-bootstrap', 'Flask-bootstrap')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


# Quiz 3


class Chapter1Quiz3OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('Small capacity', 'Small in capacity'),
            ('Incapable of doing much', 'Incapable of doing much'),
            ('A living organism', 'A living organism'),
            ('Keeping the core simple but extensible', 'Keeping the core simple but extensible')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


class Chapter2Quiz3OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('Flask', 'Flask'),
            ('Click', 'Click'),
            ('Python', 'Python'),
            ('Jinja', 'Jinja')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


class Chapter3Quiz3OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('StringField', 'StringField'),
            ('ValidationError', 'ValidationError'),
            ('PasswordField', 'PasswordField'),
            ('FlaskForm', 'FlaskForm')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')

# Quiz 4


class Chapter1Quiz4OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('By clicking the run button', 'By clicking the run button'),
            ('Using the command flask run', 'Using the command flask run'),
            ('Praying to God', 'Praying to God'),
            ('Typing the word "python" in the terminal', 'Typing the word "python" in the terminal')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


class Chapter2Quiz4OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('Flask', 'Flask'),
            ('View functions', 'View functions'),
            ('Database', 'Database'),
            ('Python', 'Database')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


class Chapter3Quiz4OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('routes.py', 'routes.py'),
            ('index.html', 'index.html'),
            ('.env', '.env'),
            ('forms.py', 'forms.py')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


# Quiz 5


class Chapter1Quiz5OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('Flask', 'Flask'),
            ('View functions', 'View functions'),
            ('Database', 'Database'),
            ('Python', 'Database')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


class Chapter2Quiz5OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('Flask', 'Flask'),
            ('Click', 'Click'),
            ('Python', 'Python'),
            ('CSS', 'CSS')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')


class Chapter3Quiz5OptionsForm(FlaskForm):
    answer = SelectField(
        'Choose an answer',
        choices=[
            ('Jinja', 'Jinja'),
            ('Flask bootsrap', 'Flask bootsrap'),
            ('SECRET_KEY', 'SECRET_KEY'),
            ('Python-dotenv', 'Python-dotenv')
            ],
        validators=[DataRequired()]
        )
    submit = SubmitField('Submit')

# ========================================
# END OF QUIZZES FORM
# ========================================
