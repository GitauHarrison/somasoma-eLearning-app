from app import db


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    verification_phone = db.Column(db.String(16))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'{self.username} {self.email} {self.verification_phone}'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    verification_phone = db.Column(db.String(16))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'{self.username} {self.email} {self.verification_phone}'


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    verification_phone = db.Column(db.String(16))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'{self.username} {self.email} {self.verification_phone}'
