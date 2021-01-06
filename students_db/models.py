from students_db import db
from flask_login import UserMixin
from students_db import login


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone = db.Column(db.String(30))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(80), nullable=False, unique=True)

    def __repr__(self):
        return f"User: {self.username}"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
