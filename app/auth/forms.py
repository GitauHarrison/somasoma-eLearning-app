from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Client, Teacher
import phonenumbers


# ------------
# Registration
# ------------

class ClientRegistrationForm(FlaskForm):
    parent_full_name = StringField('Parent Full Name',
                                   validators=[DataRequired()],
                                   render_kw={'placeholder': 'Noni Mugi Gita'})
    parent_email = StringField('Parent Email',
                               validators=[DataRequired(), Email()],
                               render_kw={'placeholder': 'Valid email address'}
                               )
    verification_phone = StringField('Parent Phone Number',
                                     validators=[DataRequired()])
    student_full_name = StringField('Student Full Name',
                                    validators=[DataRequired()],
                                    render_kw={'placeholder': 'Noni Mugi Gita'}
                                    )
    student_email = StringField('Student Email',
                                validators=[DataRequired(), Email()],
                                render_kw={'placeholder': 'Valid email address'})
    student_username = StringField('Student Username',
                                   validators=[DataRequired()],
                                   render_kw={'placeholder': 'noni'})
    student_course = StringField('Choose A Course',
                                 validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register')

    def validate_verification_phone(self, verification_phone):
        try:
            p = phonenumbers.parse(verification_phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

    def validate_username(self, username):
        parent = Client.query.filter_by(username=username.data).first()
        if parent is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        parent = Client.query.filter_by(email=email.data).first()
        if parent is not None:
            raise ValidationError('Please use a different email address')


class TeacherRegistrationForm(FlaskForm):
    teacher_full_name = StringField('Teacher Full Name',
                                    validators=[DataRequired()],
                                    render_kw={'placeholder': 'Noni Mugi Gita'})
    teacher_email = StringField('Teacher Email',
                                validators=[DataRequired(), Email()],
                                render_kw={'placeholder': 'Valid email address'}
                                )
    verification_phone = StringField('Teacher Phone Number',
                                     validators=[DataRequired()])
    teacher_username = StringField('Teacher Username',
                                   validators=[DataRequired()],
                                   render_kw={'placeholder': 'noni'})
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register')

    def validate_verification_phone(self, verification_phone):
        try:
            p = phonenumbers.parse(verification_phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

    def validate_username(self, username):
        teacher = Teacher.query.filter_by(username=username.data).first()
        if teacher is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        teacher = Teacher.query.filter_by(email=email.data).first()
        if teacher is not None:
            raise ValidationError('Please use a different email address')


# -----
# Login
# -----

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


# -------------
# Email Support
# -------------

class RequestPasswordResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'Valid email address'})
    submit = SubmitField('Request')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Reset')


# ------------------------
# Two-factor authenticaion
# ------------------------

class Enable2faForm(FlaskForm):
    verification_phone = StringField('Phone Number',
                                     validators=[DataRequired()]
                                     )
    submit = SubmitField('Enable 2FA')

    def validate_verification_number(self, verification_phone):
        try:
            p = phonenumbers.parse(verification_phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class Confirm2faForm(FlaskForm):
    token = StringField('Token', validators=[DataRequired()])
    submit = SubmitField('Verify')


class Disable2faForm(FlaskForm):
    submit = SubmitField('Disable 2FA')
