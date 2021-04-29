from app import db, login, bcrypt, app
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime
import jwt
from time import time


class Parent(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64),
                           index=True,
                           unique=True,
                           nullable=False
                           )
    last_name = db.Column(db.String(64),
                          index=True,
                          unique=True,
                          nullable=False
                          )
    username = db.Column(db.String(64),
                         index=True,
                         unique=True,
                         nullable=False
                         )
    email = db.Column(db.String(120),
                      index=True,
                      unique=True,
                      nullable=False
                      )
    verification_phone = db.Column(db.String(16))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(300))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.username} {self.email} {self.verification_phone}'

    # User login
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # User profile
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    # 2fa
    def two_factor_enabled(self):
        return self.verification_phone is not None

    # Email support
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,
                            app.config['SECRET_KEY'],
                            algorithms=['HS256']
                            )['reset_password']
        except:
            return
        return Parent.query.get(id)


class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64),
                           index=True,
                           unique=True,
                           nullable=False
                           )
    last_name = db.Column(db.String(64),
                          index=True,
                          unique=True,
                          nullable=False
                          )
    username = db.Column(db.String(64),
                         index=True,
                         unique=True,
                         nullable=False
                         )
    email = db.Column(db.String(120),
                      index=True,
                      unique=True,
                      nullable=False
                      )
    verification_phone = db.Column(db.String(16))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(300))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('StudentComment',
                               backref='author',
                               lazy='dynamic'
                               )

    def __repr__(self):
        return f'{self.username} {self.email} {self.verification_phone}'

    # User login
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # User profile
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    # 2fa
    def two_factor_enabled(self):
        return self.verification_phone is not None

    # email support
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,
                            app.config['SECRET_KEY'],
                            algorithms=['HS256']
                            )['reset_password']
        except:
            return
        return Student.query.get(id)


class Teacher(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64),
                           index=True,
                           unique=True,
                           nullable=False
                           )
    last_name = db.Column(db.String(64),
                          index=True,
                          unique=True,
                          nullable=False
                          )
    username = db.Column(db.String(64),
                         index=True,
                         unique=True,
                         nullable=False
                         )
    email = db.Column(db.String(120),
                      index=True,
                      unique=True,
                      nullable=False
                      )
    verification_phone = db.Column(db.String(16))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(300))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.username} {self.email} {self.verification_phone}'

    # User login
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # User profile
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    # 2fa
    def two_factor_enabled(self):
        return self.verification_phone is not None

    # Email support
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,
                            app.config['SECRET_KEY'],
                            algorithms=['HS256']
                            )['reset_password']
        except:
            return
        return Teacher.query.get(id)


class StudentComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return f'Student comment: {self.body}'


@login.user_loader
def teacher_load_user(id):
    return Teacher.query.get(int(id))


@login.user_loader
def parent_load_user(id):
    return Parent.query.get(int(id))


@login.user_loader
def student_load_user(id):
    return Student.query.get(int(id))
