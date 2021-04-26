from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
    TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError,\
    Length
# from app.models import User
import phonenumbers


class ParentRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Parent Email',
                        validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'Valid email address'})
    verification_phone = StringField('Parent Phone Number',
                                     validators=[DataRequired()],
                                     render_kw={'placeholder': '+254722000000'})
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

    # def validate_username(self, username):
    #     parent = Parent.query.filter_by(username=username.data).first()
    #     if parent is not None:
    #         raise ValidationError('Please use a different username')

    # def validate_email(self, email):
    #     parent = Parent.query.filter_by(email=email.data).first()
    #     if parent is not None:
    #         raise ValidationError('Please use a different email address')


class StudentRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Student Email',
                        validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'Valid email address'})
    verification_phone = StringField('Student Phone Number',
                                     validators=[DataRequired()],
                                     render_kw={'placeholder': '+254722000000'})
    course = StringField('Select a Course', validators=[DataRequired()])
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

    # def validate_username(self, username):
    #     student = Student.query.filter_by(username=username.data).first()
    #     if student is not None:
    #         raise ValidationError('Please use a different username')

    # def validate_email(self, email):
    #     student = Student.query.filter_by(email=email.data).first()
    #     if student is not None:
    #         raise ValidationError('Please use a different email address')


class TeacherRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Teacher Email',
                        validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'Valid email address'})
    verification_phone = StringField('Student Phone Number',
                                     validators=[DataRequired()],
                                     render_kw={'placeholder': '+254722000000'})
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

    # def validate_username(self, username):
    #     teacher = Teacher.query.filter_by(username=username.data).first()
    #     if teacher is not None:
    #         raise ValidationError('Please use a different username')

    # def validate_email(self, email):
    #     teacher = Teacher.query.filter_by(email=email.data).first()
    #     if teacher is not None:
    #         raise ValidationError('Please use a different email address')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RquestPasswordResetForm(FlaskForm):
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


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=300)])
    submit = SubmitField('Update')
