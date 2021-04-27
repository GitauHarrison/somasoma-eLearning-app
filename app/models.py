from app import db, login, bcrypt
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime


class Parent(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    verification_phone = db.Column(db.String(16))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(300))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.username} {self.email} {self.verification_phone}'

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def two_factor_enabled(self):
        return self.verification_phone is not None


class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    verification_phone = db.Column(db.String(16))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(300))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.username} {self.email} {self.verification_phone}'

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def two_factor_enabled(self):
        return self.verification_phone is not None


class Teacher(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    verification_phone = db.Column(db.String(16))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(300))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.username} {self.email} {self.verification_phone}'

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def two_factor_enabled(self):
        return self.verification_phone is not None


@login.user_loader
def teacher_load_user(id):
    return Teacher.query.get(int(id))


@login.user_loader
def parent_load_user(id):
    return Parent.query.get(int(id))


@login.user_loader
def student_load_user(id):
    return Student.query.get(int(id))
