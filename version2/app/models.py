from flask.globals import session
from app import db, login, bcrypt
from flask_login import UserMixin, current_user
from hashlib import md5
import jwt
from time import time
from datetime import datetime
from flask import current_app


class Client(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_full_name = db.Column(db.String(64),
                                 index=True,
                                 unique=True,
                                 nullable=False
                                 )
    parent_email = db.Column(db.String(120),
                             index=True,
                             unique=True,
                             nullable=False
                             )
    verification_phone = db.Column(db.String(16))
    student_full_name = db.Column(db.String(64),
                                  index=True,
                                  unique=True,
                                  nullable=False
                                  )
    student_email = db.Column(db.String(120),
                              index=True,
                              unique=True,
                              nullable=False
                              )
    student_username = db.Column(db.String(64),
                                 index=True,
                                 unique=True,
                                 nullable=False
                                 )
    student_course = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(300))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('ClientComment', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'{self.student_username} {self.student_email} {self.verification_phone}'

    # Client login
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # Client profile
    def avatar(self, size):
        digest = md5(self.student_email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    # 2fa
    def two_factor_enabled(self):
        return self.verification_phone is not None

    # Email support
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,
                            current_app.config['SECRET_KEY'],
                            algorithms=['HS256']
                            )['reset_password']
        except:
            return
        return Client.query.get(id)


class ClientComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    def __repr__(self):
        return f'Post: {self.id} {self.body}'


class Teacher(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_full_name = db.Column(db.String(64),
                                  index=True,
                                  unique=True,
                                  nullable=False
                                  )
    teacher_email = db.Column(db.String(120),
                              index=True,
                              unique=True,
                              nullable=False
                              )
    teacher_username = db.Column(db.String(64),
                                 index=True,
                                 unique=True,
                                 nullable=False
                                 )
    verification_phone = db.Column(db.String(16))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(300))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('TeacherComment', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'{self.teacher_username} {self.teacher_email} {self.verification_phone}'

    # Teacher login
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # Teacher profile
    def avatar(self, size):
        digest = md5(self.teacher_email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    # 2fa
    def two_factor_enabled(self):
        return self.verification_phone is not None

    # Email support
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,
                            current_app.config['SECRET_KEY'],
                            algorithms=['HS256']
                            )['reset_password']
        except:
            return
        return Teacher.query.get(id)


class TeacherComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __repr__(self):
        return f'Post: {self.id} {self.body}'


@login.user_loader
def load_client(id):
    return Client.query.get(int(id))


# @login.user_loader
# def load_teacher(id):
#     return Teacher.query.get(int(id))


# @login.user_loader
# def load_user(id):
#     client = Client.query.get(id)
#     teacher = Teacher.query.get(id)
#     if current_user == client:
#         return Client.query.get(int(id))
#     elif current_user == teacher:
#         return Teacher.query.get(int(id))
#     else:
#         return None
