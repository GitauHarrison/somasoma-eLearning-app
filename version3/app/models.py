from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5
from flask import current_app
import jwt
from time import time


@login.user_loader
def load_student(id):
    return Student.query.get(int(id))


# @login.user_loader
# def load_parent(id):
#     return Parent.query.get(int(id))


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('student.id'))
)


class Student(UserMixin, db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    student_full_name = db.Column(db.String(64), index=True, unique=True)
    student_email = db.Column(db.String(120), index=True, unique=True)
    student_phone = db.Column(db.String(120), index=True, unique=True)
    student_school = db.Column(db.String(120), index=True)
    student_age = db.Column(db.Integer, index=True)
    student_course = db.Column(db.String(120), index=True)
    student_password_hash = db.Column(db.String(128))
    student_about_me = db.Column(db.String(140))
    student_last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))

    comments = db.relationship(
                               'CommunityComment',
                               backref='author',
                               lazy='dynamic'
                               )
    webdev_chapter1_comments = db.relationship(
                                        'WebDevChapter1Comment',
                                        backref='author',
                                        lazy='dynamic'
                                        )
    webdev_chapter1_objectives = db.relationship(
                                        'WebDevChapter1Objectives',
                                        backref='author',
                                        lazy='dynamic'
                                        )
    webdev_chapter1_quiz = db.relationship(
                                        'WebDevChapter1Quiz',
                                        backref='author',
                                        lazy='dynamic'
                                        )
    webdev_chapter1_quiz_options = db.relationship(
                                        'WebDevChapter1QuizOptions',
                                        backref='author',
                                        lazy='dynamic'
                                        )

    def __repr__(self):
        return f'Student {self.student_full_name}'

    def set_password(self, student_password):
        self.student_password_hash = generate_password_hash(student_password)

    def check_password(self, student_password):
        return check_password_hash(
            self.student_password_hash,
            student_password
            )

    # Two-factor authentication
    def two_factor_student_enabled(self):
        return self.student_phone is not None

    # Client avatar

    def avatar_student(self, size):
        digest = md5(self.student_email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    followed = db.relationship(
        'Student',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, student):
        if not self.is_following(student):
            self.followed.append(student)

    def unfollow(self, student):
        if self.is_following(student):
            self.followed.remove(student)

    def is_following(self, student):
        return self.followed.filter(
            followers.c.followed_id == student.id).count() > 0

    def followed_comments(self):
        followed = CommunityComment.query.join(
            followers,
            (followers.c.followed_id == CommunityComment.student_id)
            ).filter(followers.c.follower_id == self.id)
        own = CommunityComment.query.filter_by(student_id=self.id)
        return followed.union(own).order_by(CommunityComment.timestamp.desc())

    # Password reset

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Student.query.get(id)


class Parent(UserMixin, db.Model):
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True)
    parent_full_name = db.Column(db.String(64), index=True)
    parent_email = db.Column(db.String(120), index=True)
    parent_phone = db.Column(db.String(120), index=True)
    parent_occupation = db.Column(db.String(120), index=True)
    parent_residence = db.Column(db.String(120), index=True)
    parent_password_hash = db.Column(db.String(128))
    child = db.relationship('Student', backref='parent', lazy='dynamic')

    def __repr__(self):
        return f'Parent {self.parent_full_name}'

    def set_password(self, parent_password):
        self.parent_password_hash = generate_password_hash(parent_password)

    def check_password(self, parent_password):
        return check_password_hash(self.parent_password_hash, parent_password)

    # Two-factor authentication
    def two_factor_parent_enabled(self):
        return self.parent_phone is not None

    # Parent avatar
    def avatar_parent(self, size):
        digest = md5(self.parent_email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Teacher(UserMixin, db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    teacher_full_name = db.Column(db.String(64), index=True, unique=True)
    teacher_email = db.Column(db.String(120), index=True, unique=True)
    teacher_phone = db.Column(db.String(120), index=True, unique=True)
    teacher_residence = db.Column(db.String(120), index=True)
    teacher_course = db.Column(db.String(120), index=True)
    teacher_password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'Teacher {self.teacher_full_name}'

    def set_password(self, teacher_password):
        self.teacher_password_hash = generate_password_hash(teacher_password)

    def check_password(self, teacher_password):
        return check_password_hash(
            self.teacher_password_hash,
            teacher_password
            )

    # Two-factor authentication
    def two_factor_teacher_enabled(self):
        return self.teacher_phone is not None

    # Parent avatar
    def avatar_teacher(self, size):
        digest = md5(self.teacher_email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

# Anonymous User


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    comment = db.Column(db.String(140))

    comments = db.relationship(
        'AnonymousTemplateInheritanceComment',
        backref='author',
        lazy='dynamic'
        )

    def __repr__(self):
        return f'User {self.name}'

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class CommunityComment(db.Model):
    __tablename__ = 'community_comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return f'Community Comment: {self.body}'

# ============================================================
# WEB DEVELOPMENT
# ============================================================


class WebDevChapter1Comment(db.Model):
    __tablename__ = 'chapter1_comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return f'Chapter 1 Comment: {self.body}'


class WebDevChapter1Objectives(db.Model):
    __tablename__ = 'web_dev_chapter1_objectives'
    id = db.Column(db.Integer, primary_key=True)

    # Objectives
    objective_1 = db.Column(db.Boolean, default=False)
    objective_2 = db.Column(db.Boolean, default=False)
    objective_3 = db.Column(db.Boolean, default=False)
    objective_4 = db.Column(db.Boolean, default=False)
    objective_5 = db.Column(db.Boolean, default=False)
    objective_6 = db.Column(db.Boolean, default=False)
    objective_7 = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return f'Objectives: {self.objective_1} {self.objective_2} {self.objective_3} {self.objective_4} {self.objective_5} {self.objective_6} {self.objective_7}'


class WebDevChapter1Quiz(db.Model):
    __tablename__ = 'web_dev_chapter1_quiz'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))


class WebDevChapter1QuizOptions(db.Model):
    __tablename__ = 'web_dev_chapter1_quiz_options'
    id = db.Column(db.Integer, primary_key=True)
    option_1 = db.Column(db.Boolean, default=False)
    option_2 = db.Column(db.Boolean, default=False)
    option_3 = db.Column(db.Boolean, default=False)
    option_4 = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

# ============================================================
# END OF WEB DEVELOPMENT
# ============================================================


# ============================================================
# ANONYMOUS COURSE CONTENT
# ============================================================


class AnonymousTemplateInheritanceComment(db.Model):
    __tablename__ = 'template inheritance comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Template Inheritance Comment: {self.body}'

# ============================================================
# ANONYMOUS COURSE CONTENT
# ============================================================
