from students_db import db
from flask_login import UserMixin
from students_db import login


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone = db.Column(db.String(30))

    def __repr__(self):
        return f"Student: {self.name}"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(80), nullable=False, unique=True)
    department = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(30))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"User: {self.name}"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
