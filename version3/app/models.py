from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5


@login.user_loader
def load_student(id):
    return Student.query.get(int(id))


# @login.user_loader
# def load_parent(id):
#     return Parent.query.get(int(id))


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

    def set_password(self, student_password):
        self.student_password_hash = generate_password_hash(student_password)

    def check_password(self, student_password):
        return check_password_hash(self.student_password_hash, student_password)

    # Two-factor authentication
    def two_factor_student_enabled(self):
        return self.student_phone is not None

    # Client avatar

    def avatar_student(self, size):
        digest = md5(self.student_email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Parent(UserMixin, db.Model):
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True)
    parent_full_name = db.Column(db.String(64), index=True, unique=True)
    parent_email = db.Column(db.String(120), index=True, unique=True)
    parent_phone = db.Column(db.String(120), index=True, unique=True)
    parent_occupation = db.Column(db.String(120), index=True)
    parent_residence = db.Column(db.String(120), index=True)
    parent_password_hash = db.Column(db.String(128))

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
