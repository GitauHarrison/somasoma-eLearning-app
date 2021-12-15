from app.models import Client
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,\
    TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,\
    ValidationError
import phonenumbers


# ========================================
# AUTHENTICATION FORMS
# ========================================


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Valid Email Address"}
                        )
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ClientRegistrationForm(FlaskForm):
    parent_full_name = StringField('Parent Full Name',
                                   validators=[DataRequired(),
                                               Length(min=2, max=20)
                                               ]
                                   )
    parent_email = StringField('Parent Email',
                               validators=[DataRequired(), Email()],
                               render_kw={"placeholder": "Valid Email Address"}
                               )
    parent_phone = StringField('Parent Phone Number',
                               validators=[DataRequired()]
                               )
    parent_occupation = StringField('Parent Occupation',
                                    validators=[DataRequired()]
                                    )
    parent_residence = StringField('Parent Residence',
                                   validators=[DataRequired()]
                                   )
    parent_password = PasswordField('Parent Password',
                                    validators=[DataRequired()])
    parent_confirm_password = PasswordField('Parent Confirm Password',
                                            validators=[DataRequired(),
                                                        EqualTo('parent_password')
                                                        ]
                                            )
    # Student
    student_full_name = StringField('Student Full Name',
                                    validators=[DataRequired(),
                                                Length(min=2, max=20)
                                                ]
                                    )
    student_email = StringField('Student Email',
                                validators=[DataRequired(), Email()],
                                render_kw={"placeholder": "Valid Email Address"}
                                )
    student_phone = StringField('Student Phone Number',
                                validators=[DataRequired()]
                                )
    student_school = StringField('Student School',
                                 validators=[DataRequired()]
                                 )
    student_age = StringField('Student Age',
                              validators=[DataRequired()]
                              )
    student_password = PasswordField('Student Password',
                                     validators=[DataRequired()])
    student_confirm_password = PasswordField('Student Confirm Password',
                                             validators=[DataRequired(),
                                                         EqualTo('student_password')
                                                         ]
                                             )

    submit = SubmitField('Register')

    def validate_parent_full_name(self, parent_full_name):
        parent = Client.query.filter_by(parent_full_name=parent_full_name.data).first()
        if parent:
            raise ValidationError('Name already taken. Please choose a different one.')

    def validate_parent_email(self, parent_email):
        parent = Client.query.filter_by(parent_email=parent_email.data).first()
        if parent:
            raise ValidationError('Name already taken. Please choose a different one.')

    def validate_student_full_name(self, student_full_name):
        student = Client.query.filter_by(student_full_name=student_full_name.data).first()
        if student:
            raise ValidationError('Name already taken. Please choose a different one.')

    def validate_student_email(self, student_email):
        student = Client.query.filter_by(student_email=student_email.data).first()
        if student:
            raise ValidationError('Name already taken. Please choose a different one.')


class RequestPasswordResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Valid Email Address Used During Registration"}
                        )
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()]
                             )
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')
                                                 ]
                                     )
    submit = SubmitField('Reset Password')


# Two-factor authentication


class Enable2faForm(FlaskForm):
    verification_phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Enalble 2fa')

    def validate_verification_number(self, verification_phone):
        try:
            p = phonenumbers.parse(verification_phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class Confirm2faForm(FlaskForm):
    token = StringField('Token')
    submit = SubmitField('Verify')


class Disable2faForm(FlaskForm):
    submit = SubmitField('Disable 2fa')

# End of two-factor authentication

# ========================================
# END OF AUTHENTICATION FORMS
# ========================================

# ========================================
# COMMENT FORM
# ========================================


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment',
                            validators=[DataRequired()]
                            )
    submit = SubmitField('Post')

# ========================================
# END OF COMMENT FORM
# ========================================

# ========================================
# PROFILE FORM
# ========================================


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

    def validate_student_email(self, email):
        if email.data != self.original_email:
            student = Client.query.filter_by(student_email=self.email.data).first()
            if student is not None:
                raise ValidationError('Please use a different email.')

# ========================================
# END OF PROFILE FORM
# ========================================

# ========================================
# COURSES FORM
# ========================================

# Web Development


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
# COURSES FORM
# ========================================
