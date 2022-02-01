from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5
from flask import current_app
import jwt
from time import time
from markdown import markdown
import bleach
import json


# @login.user_loader
# def load_student(id):
#     return Student.query.get(int(id))


@login.user_loader
def load_teacher(id):
    return Teacher.query.get(int(id))

# @login.user_loader
# def load_admin(id):
#     return Admin.query.get(int(id))


# @login.user_loader
# def load_parent(id):
#     return Parent.query.get(int(id))


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('student.id'))
)

teacher_followers = db.Table(
    'teacher_followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('teacher.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('teacher.id'))
)

# ========================================
# ADMIN MODELS
# ========================================


class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    admin_full_name = db.Column(db.String(64), index=True, unique=True)
    admin_email = db.Column(db.String(64), unique=True, index=True)
    admin_phone = db.Column(db.String(64), unique=True, index=True)
    admin_last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    admin_about_me = db.Column(db.String(140))
    admin_password_hash = db.Column(db.String(128))

    courses = db.relationship(
        'Courses',
        backref='author',
        lazy='dynamic'
        )
    flask_student_stories = db.relationship(
        'FlaskStudentStories',
        backref='author',
        lazy='dynamic'
        )

    def __repr__(self):
        return f'Admin: {self.admin_full_name}'

    def set_password(self, password):
        self.admin_password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.admin_password_hash, password)

    def avatar_admin(self, size):
        digest = md5(self.admin_email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    # Two-factor authentication

    def two_factor_admin_enabled(self):
        return self.admin_phone is not None

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Admin.query.get(id)

# ========================================
# END OF ADMIN MODELS
# ========================================

# ========================================
# STUDENT MODELS
# ========================================


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

    messages_sent = db.relationship(
        'StudentMessage',
        foreign_keys='StudentMessage.sender_id',
        backref='author',
        lazy='dynamic'
        )
    messages_received = db.relationship(
        'StudentMessage',
        foreign_keys='StudentMessage.recipient_id',
        backref='recipient',
        lazy='dynamic'
        )
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship(
        'StudentNotification',
        backref='student',
        lazy='dynamic'
        )

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
    webdev_chapter1_quiz_1_options = db.relationship(
        'WebDevChapter1Quiz1Options',
        backref='author',
        lazy='dynamic'
        )
    webdev_chapter1_quiz_2_options = db.relationship(
        'WebDevChapter1Quiz2Options',
        backref='author',
        lazy='dynamic'
        )
    webdev_chapter1_quiz_3_options = db.relationship(
        'WebDevChapter1Quiz3Options',
        backref='author',
        lazy='dynamic'
        )
    webdev_chapter1_quiz_4_options = db.relationship(
        'WebDevChapter1Quiz4Options',
        backref='author',
        lazy='dynamic'
        )

    def __repr__(self):
        return f'Student {self.student_full_name}'

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return StudentMessage.query.filter_by(recipient=self).filter(
            StudentMessage.timestamp > last_read_time).count()

    def add_notification(self, student_full_name, data):
        self.notifications.filter_by(
            student_full_name=student_full_name).delete()
        n = StudentNotification(
            student_full_name=student_full_name,
            payload_json=json.dumps(data),
            student=self
            )
        db.session.add(n)
        return n

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
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Student.query.get(id)


class StudentMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'Message {self.body}'


class StudentNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_full_name = db.Column(db.String(128), index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))


class CommunityComment(db.Model):
    __tablename__ = 'community_comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return f'Community Comment: {self.body}'

    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br', 'li'
                        ]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(
    CommunityComment.body,
    'set',
    CommunityComment.on_changed_body
    )


# ========================================
# END OF STUDENT MODELS
# ========================================

# ========================================
# PARENT MODELS
# ========================================


class Parent(UserMixin, db.Model):
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True)
    parent_full_name = db.Column(db.String(64), index=True)
    parent_email = db.Column(db.String(120), index=True)
    parent_phone = db.Column(db.String(120), index=True)
    parent_occupation = db.Column(db.String(120), index=True)
    parent_residence = db.Column(db.String(120), index=True)
    parent_last_seen = db.Column(db.DateTime, default=datetime.utcnow)
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

    # Password reset
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Parent.query.get(id)

# ========================================
# END OF PARENT MODELS
# ========================================

# ========================================
# TEACHER MODELS
# ========================================


class Teacher(UserMixin, db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    teacher_full_name = db.Column(db.String(64), index=True, unique=True)
    teacher_email = db.Column(db.String(120), index=True, unique=True)
    teacher_phone = db.Column(db.String(120), index=True, unique=True)
    teacher_residence = db.Column(db.String(120), index=True)
    teacher_course = db.Column(db.String(120), index=True)
    teacher_about_me = db.Column(db.String(140))
    teacher_last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    teacher_password_hash = db.Column(db.String(128))

    comments = db.relationship(
        'TeacherCommunityComment',
        backref='author',
        lazy='dynamic'
        )
    course_overview = db.relationship(
        'WebDevelopmentOverview',
        backref='author',
        lazy='dynamic'
        )
    table_of_contentes = db.relationship(
        'TableOfContents',
        backref='author',
        lazy='dynamic'
        )
    chapter = db.relationship(
        'Chapter',
        backref='author',
        lazy='dynamic'
        )
    chapter_quizzes = db.relationship(
        'ChapterQuiz',
        backref='author',
        lazy='dynamic'
        )
    blog_articles = db.relationship(
        'BlogArticles',
        backref='author',
        lazy='dynamic'
    )
    events = db.relationship(
        'Events',
        backref='author',
        lazy='dynamic'
        )
    messages_sent = db.relationship(
        'TeacherMessage',
        foreign_keys='TeacherMessage.sender_id',
        backref='author',
        lazy='dynamic'
        )
    messages_received = db.relationship(
        'TeacherMessage',
        foreign_keys='TeacherMessage.recipient_id',
        backref='recipient',
        lazy='dynamic'
        )
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship(
        'TeacherNotifications',
        backref='teacher',
        lazy='dynamic'
        )

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return TeacherMessage.query.filter_by(recipient=self).filter(
            TeacherMessage.timestamp > last_read_time).count()

    def add_notification(self, teacher_full_name, data):
        self.notifications.filter_by(
            teacher_full_name=teacher_full_name).delete()
        n = TeacherNotifications(
            teacher_full_name=teacher_full_name,
            payload_json=json.dumps(data),
            teacher=self
            )
        db.session.add(n)
        return n

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

    # Password reset
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Teacher.query.get(id)

    teacher_followed = db.relationship(
        'Teacher',
        secondary=teacher_followers,
        primaryjoin=(teacher_followers.c.follower_id == id),
        secondaryjoin=(teacher_followers.c.followed_id == id),
        backref=db.backref(
            'teacher_followers',
            lazy='dynamic'
            ), lazy='dynamic')

    def follow(self, teacher):
        if not self.is_following(teacher):
            self.teacher_followed.append(teacher)

    def unfollow(self, teacher):
        if self.is_following(teacher):
            self.teacher_followed.remove(teacher)

    def is_following(self, teacher):
        return self.teacher_followed.filter(
            teacher_followers.c.followed_id == teacher.id).count() > 0

    def followed_comments(self):
        teacher_followed = TeacherCommunityComment.query.join(
            teacher_followers,
            (teacher_followers.c.followed_id == TeacherCommunityComment.teacher_id)
            ).filter(teacher_followers.c.follower_id == self.id)
        own = TeacherCommunityComment.query.filter_by(teacher_id=self.id)
        return teacher_followed.union(own).order_by(
            TeacherCommunityComment.timestamp.desc()
            )


class TeacherMessage(db.Model):
    __tablename__ = 'teacher_message'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    body = db.Column(db.String(140))
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'Message {self.body}'

    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br', 'li'
                        ]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(
    TeacherMessage.body,
    'set',
    TeacherMessage.on_changed_body
    )


class TeacherNotifications(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    teacher_full_name = db.Column(db.String(128), index=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))


class TeacherCommunityComment(db.Model):
    __tablename__ = 'teacher community comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __repr__(self):
        return f'Teacher Comment: {self.body}'

    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br', 'li'
                        ]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(
    TeacherCommunityComment.body,
    'set',
    TeacherCommunityComment.on_changed_body
    )


class WebDevelopmentOverview(db.Model):
    __tablename__ = 'web development overview'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    overview = db.Column(db.String(140))
    overview_html = db.Column(db.Text)
    youtube_link = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    allowed_status = db.Column(db.Boolean, default=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __repr__(self):
        return f'Web Development Overview: {self.title}'

    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br', 'li'
                        ]
        target.overview_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(
    WebDevelopmentOverview.overview,
    'set',
    WebDevelopmentOverview.on_changed_body
    )


class TableOfContents(db.Model):
    __tablename__ = 'table of contents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    chapter = db.Column(db.String(140))
    link = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    allowed_status = db.Column(db.Boolean, default=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __repr__(self):
        return f'Table of Contents: {self.chapter}'


class Chapter(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(140))
    chapter = db.Column(db.String(64), index=True)
    chapter_link = db.Column(db.String(140))
    chapter_review_link = db.Column(db.String(140))
    overview = db.Column(db.String(140))
    overview_html = db.Column(db.Text)
    accomplish = db.Column(db.String(140))
    youtube_link = db.Column(db.String(140))
    conclusion = db.Column(db.String(140))
    objective_1 = db.Column(db.String(140))
    objective_2 = db.Column(db.String(140))
    objective_3 = db.Column(db.String(140))
    objective_4 = db.Column(db.String(140))
    objective_5 = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    allowed_status = db.Column(db.Boolean, default=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __repr__(self):
        return f'Chapter: {self.chapter}'

    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br', 'li'
                        ]
        target.overview_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(Chapter.overview, 'set', Chapter.on_changed_body)


class ChapterQuiz(db.Model):
    __tablename__ = 'chapter quiz'
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(140))
    chapter = db.Column(db.String(64), index=True)
    review_quiz_link = db.Column(db.String(140))
    quiz_1 = db.Column(db.String(140))
    quiz_2 = db.Column(db.String(140))
    quiz_3 = db.Column(db.String(140))
    quiz_4 = db.Column(db.String(140))
    quiz_5 = db.Column(db.String(140))
    allowed_status = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __repr__(self):
        return f'Chapter Quiz: {self.chapter}'


class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_image = db.Column(db.String(300))
    title = db.Column(db.String(64), index=True)
    body = db.Column(db.String(300))
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    date = db.Column(db.String(300))
    time = db.Column(db.String(300))
    location = db.Column(db.String(300))
    link = db.Column(db.String(300))
    allowed_status = db.Column(db.Boolean, default=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __repr__(self):
        return f'Event: {self.title}'

    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br', 'li'
                        ]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(
    Events.body, 'set', Events.on_changed_body)


# ========================================
# END OF TEACHER MODELS
# ========================================

# ========================================
# ANONYMOUS MODELS
# ========================================


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    comment = db.Column(db.String(140))
    comment_html = db.Column(db.Text)

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

    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br', 'li'
                        ]
        target.comment_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(User.comment, 'set', User.on_changed_body)


class BlogArticles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_image = db.Column(db.String(140))
    article_name = db.Column(db.String(140))
    body = db.Column(db.String(300))
    body_html = db.Column(db.Text)
    link = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    allowed_status = db.Column(db.Boolean, default=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __repr__(self):
        return f'Article: {self.article_name}'

    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br', 'li'
                        ]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(BlogArticles.body, 'set', BlogArticles.on_changed_body)


class Courses(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    course_image = db.Column(db.String(300))
    title = db.Column(db.String(64), index=True)
    body = db.Column(db.String(300))
    body_html = db.Column(db.Text)
    overview = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    next_class_date = db.Column(db.String(300))
    link = db.Column(db.String(300))
    allowed_status = db.Column(db.Boolean, default=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return f'Course: {self.title}'

    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br', 'li'
                        ]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(Courses.body, 'set', Courses.on_changed_body)  


class FlaskStudentStories(db.Model):
    __tablename__ = 'flask student stories'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    student_image = db.Column(db.String(300))
    email = db.Column(db.String(64), unique=True)
    body = db.Column(db.String(300))
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    allowed_status = db.Column(db.Boolean, default=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return f'Flask Story: {self.body}'

    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br', 'li'
                        ]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(FlaskStudentStories.body,
                'set',
                FlaskStudentStories.on_changed_body
                )


class AnonymousTemplateInheritanceComment(db.Model):
    __tablename__ = 'template inheritance comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Template Inheritance Comment: {self.body}'

    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br', 'li'
                        ]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(AnonymousTemplateInheritanceComment.body,
                'set',
                AnonymousTemplateInheritanceComment.on_changed_body
                )

# ========================================
# ANONYMOUS MODELS
# ========================================

# ========================================
# WEB DEVELOPMENT MODELS
# ========================================


class WebDevChapter1Comment(db.Model):
    __tablename__ = 'chapter1_comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    body_html = db.Column(db.Text)
    allowed_status = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return f'Chapter 1 Comment: {self.body}'

    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'br', 'li'
                        ]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


db.event.listen(WebDevChapter1Comment.body,
                'set',
                WebDevChapter1Comment.on_changed_body
                )


class WebDevChapter1Objectives(db.Model):
    __tablename__ = 'web_dev_chapter1_objectives'
    id = db.Column(db.Integer, primary_key=True)

    # Objectives
    objective_1 = db.Column(db.Boolean, default=False)
    objective_2 = db.Column(db.Boolean, default=False)
    objective_3 = db.Column(db.Boolean, default=False)
    objective_4 = db.Column(db.Boolean, default=False)
    objective_5 = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return f'Objectives: {self.objective_1}, {self.objective_2},\
            {self.objective_3}, {self.objective_4}, {self.objective_5}\n\n'


class WebDevChapter1Quiz(db.Model):
    __tablename__ = 'web_dev_chapter1_quiz'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return f'Quiz: {self.title}'


class WebDevChapter1Quiz1Options(db.Model):
    __tablename__ = 'web_dev_chapter_1_quiz_1_options'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return f'Quiz 1 Options: {self.answer}'


class WebDevChapter1Quiz2Options(db.Model):
    __tablename__ = 'web_dev_chapter_1_quiz_2_options'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return f'Quiz 2 Options: {self.answer}'


class WebDevChapter1Quiz3Options(db.Model):
    __tablename__ = 'web_dev_chapter_1_quiz_3_options'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return f'Quiz 3 Options: {self.answer}'


class WebDevChapter1Quiz4Options(db.Model):
    __tablename__ = 'web_dev_chapter_1_quiz_4_options'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return f'Quiz 4 Options: {self.answer}'

# ========================================
# END OF WEB DEVELOPMENT MODELS
# ========================================
