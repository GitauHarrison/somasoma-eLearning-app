from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    parent_full_name = db.Column(db.String(64), index=True)
    parent_email = db.Column(db.String(120), index=True)
    parent_phone = db.Column(db.String(120), index=True)
    parent_occupation = db.Column(db.String(120), index=True)
    parent_residence = db.Column(db.String(120), index=True)
    parent_password_hash = db.Column(db.String(128))

    student_full_name = db.Column(db.String(64), index=True)
    student_email = db.Column(db.String(120), index=True)
    student_phone = db.Column(db.String(120), index=True)
    student_school = db.Column(db.String(120), index=True)
    student_age = db.Column(db.Integer, index=True)
    student_password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'Client: {self.parent_full_name} - {self.student_full_name}'

    def set_parent_password(self, parent_password):
        self.parent_password_hash = generate_password_hash(parent_password)

    def check_parent_password(self, parent_password):
        return check_password_hash(self.parent_password_hash, parent_password)

    def set_student_password(self, student_password):
        self.student_password_hash = generate_password_hash(student_password)

    def check_student_password(self, student_password):
        return check_password_hash(self.student_password_hash, student_password)


@login.user_loader
def load_user(id):
    return Client.query.get(int(id))
