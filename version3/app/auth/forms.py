from app.models import Parent, Student, Teacher, Admin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,\
    SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo,\
    ValidationError
import phonenumbers


# Login form

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Valid Email Address"}
                        )
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# End of Login form

# Registration form


class AdminRegistrationForm(FlaskForm):
    admin_full_name = StringField(
        'Admin Full Name',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    admin_email = StringField(
        'Admin Email',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Valid Email Address"}
        )
    admin_phone = StringField(
        'Admin Phone Number',
        validators=[DataRequired()]
        )
    admin_password = PasswordField(
        'Admin Password',
        validators=[DataRequired()]
        )
    admin_confirm_password = PasswordField(
        'Admin Confirm Password',
        validators=[DataRequired(), EqualTo('admin_password')]
        )
    submit = SubmitField('Register')

    def validate_admin_full_name(self, admin_full_name):
        admin = Admin.query.filter_by(
            admin_full_name=admin_full_name.data
            ).first()
        if admin:
            raise ValidationError(
                'Name already taken. Please choose a different one.'
                )

    def validate_admin_email(self, admin_email):
        admin = Admin.query.filter_by(
            admin_email=admin_email.data
            ).first()
        if admin:
            raise ValidationError(
                'Name already taken. Please choose a different one.'
                )


class StudentRegistrationForm(FlaskForm):
    student_full_name = StringField(
        'Student Full Name',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    student_email = StringField(
        'Student Email',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Valid Email Address"}
        )
    student_phone = StringField(
        'Student Phone Number',
        validators=[DataRequired()])
    student_school = StringField(
        'Student School',
        validators=[DataRequired()]
        )
    student_age = StringField(
        'Student Age',
        validators=[DataRequired()]
        )
    student_course = SelectField(
        'Student Course',
        choices=[
            ('Flask Web Development', 'Flask Web Development'),
            ('Python DSA', 'Python DSA'),
            ('Data Science', 'Data Science'),
            ('Machine Learning', 'Machine Learning')
            ],
        validators=[DataRequired()]
        )
    student_password = PasswordField(
        'Student Password',
        validators=[DataRequired()]
        )
    student_confirm_password = PasswordField(
        'Student Confirm Password',
        validators=[DataRequired(), EqualTo('student_password')]
        )
    submit = SubmitField('Register')

    def validate_student_full_name(self, student_full_name):
        student = Student.query.filter_by(
            student_full_name=student_full_name.data
            ).first()
        if student:
            raise ValidationError(
                'Name already taken. Please choose a different one.'
                )

    def validate_student_email(self, student_email):
        student = Student.query.filter_by(
            student_email=student_email.data
            ).first()
        if student:
            raise ValidationError(
                'Name already taken. Please choose a different one.'
                )


class ParentRegistrationForm(FlaskForm):
    parent_full_name = StringField(
        'Parent Full Name',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    parent_email = StringField(
        'Parent Email',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Valid Email Address"}
        )
    parent_phone = StringField(
        'Parent Phone Number',
        validators=[DataRequired()])
    parent_occupation = StringField(
        'Parent Occupation',
        validators=[DataRequired()]
        )
    parent_residence = StringField(
        'Parent Residence',
        validators=[DataRequired()]
        )
    parent_password = PasswordField(
        'Parent Password',
        validators=[DataRequired()]
        )
    parent_confirm_password = PasswordField(
        'Parent Confirm Password',
        validators=[DataRequired(), EqualTo('parent_password')]
        )
    submit = SubmitField('Register')

    def validate_parent_full_name(self, parent_full_name):
        parent = Parent.query.filter_by(
            parent_full_name=parent_full_name.data
            ).first()
        if parent:
            raise ValidationError(
                'Name already taken. Please choose a different one.'
                )

    def validate_parent_email(self, parent_email):
        parent = Parent.query.filter_by(
            parent_email=parent_email.data
            ).first()
        if parent:
            raise ValidationError(
                'Name already taken. Please choose a different one.'
                )


class TeacherRegistrationForm(FlaskForm):
    teacher_full_name = StringField(
        'Teacher Full Name',
        validators=[DataRequired(), Length(min=2, max=20)]
        )
    teacher_email = StringField(
        'Teacher Email',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Valid Email Address"}
        )
    teacher_phone = StringField(
        'Teacher Phone Number',
        validators=[DataRequired()])
    teacher_residence = StringField(
        'Teacher Residence',
        validators=[DataRequired()]
        )
    teacher_course = SelectField(
        'Teaching Course',
        choices=[
            ('Flask Web Development', 'Flask Web Development'),
            ('Python DSA', 'Python DSA'),
            ('Data Science', 'Data Science'),
            ('Machine Learning', 'Machine Learning')
            ],
        validators=[DataRequired()]
        )
    teacher_password = PasswordField(
        'Teacher Password',
        validators=[DataRequired()]
        )
    teacher_confirm_password = PasswordField(
        'Teacher Confirm Password',
        validators=[DataRequired(), EqualTo('teacher_password')]
        )
    submit = SubmitField('Register')

    def validate_teacher_full_name(self, teacher_full_name):
        teacher = Teacher.query.filter_by(
            teacher_full_name=teacher_full_name.data
            ).first()
        if teacher:
            raise ValidationError(
                'Name already taken. Please choose a different one.'
                )

    def validate_teacher_email(self, teacher_email):
        teacher = Teacher.query.filter_by(
            teacher_email=teacher_email.data
            ).first()
        if teacher:
            raise ValidationError(
                'Name already taken. Please choose a different one.'
                )

# End of registration form

# Password reset form


class RequestPasswordResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={
                            "placeholder":
                            "Valid Email Address Used During Registration"
                            }
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

# End of password reset form


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
