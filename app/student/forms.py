from app.models import Student
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
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


class Chapter1WebDevelopmentForm(FlaskForm):
    objective_1 = BooleanField('1. Understand the concept of web development',)
    objective_2 = BooleanField('2. Understand the concept of web development',)
    objective_3 = BooleanField('3. Understand the concept of web development',)
    objective_4 = BooleanField('4. Understand the concept of web development',)
    objective_5 = BooleanField('5. Understand the concept of web development',)
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


class Chapter1QuizOptionsForm(FlaskForm):
    option_1 = BooleanField('Option 1')
    option_2 = BooleanField('Option 2')
    option_3 = BooleanField('Option 3')
    option_4 = BooleanField('Option 4')
    submit = SubmitField('Submit')

# ========================================
# END OF QUIZZES FORM
# ========================================
