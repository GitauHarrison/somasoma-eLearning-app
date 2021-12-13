from app.models import Client
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


# ========================================
# Login form
# ========================================


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Valid Email Address"}
                        )
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# ========================================
# Client Registration Form
# ========================================

class ParentRegistrationForm(FlaskForm):
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

    submit = SubmitField('Register')

    def validate_parent_full_name(self, parent_full_name):
        parent = Client.query.filter_by(parent_full_name=parent_full_name.data).first()
        if parent:
            raise ValidationError('Name already taken. Please choose a different one.')

    def validate_parent_email(self, parent_email):
        parent = Client.query.filter_by(parent_email=parent_email.data).first()
        if parent:
            raise ValidationError('Name already taken. Please choose a different one.')


class StudentRegistrationForm(FlaskForm):
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
                                                         EqualTo('parent_password')
                                                         ]
                                             )
    submit = SubmitField('Register')

    def validate_student_full_name(self, student_full_name):
        student = Client.query.filter_by(student_full_name=student_full_name.data).first()
        if student:
            raise ValidationError('Name already taken. Please choose a different one.')

    def validate_student_email(self, student_email):
        student = Client.query.filter_by(student_email=student_email.data).first()
        if student:
            raise ValidationError('Name already taken. Please choose a different one.')

# ========================================
# End of client registration form
# ========================================

# ========================================
# Password reset form
# ========================================


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

# ========================================
# End of password reset form
# ========================================
