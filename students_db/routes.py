from students_db import app
from students_db import db
from flask import render_template, request, redirect, url_for, session, flash
from flask_session import Session
from students_db.models import Student, User
from students_db.forms import RegisterForm, AddStudent, LoginForm
from students_db.helpers import login_required
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
@app.route('/show')
# @login_required
def dashboard():
    students = Student.query.all()
    return render_template('table.html', students=students)


@app.route('/add', methods=['GET', 'POST'])
# @login_required
def add():
    form = AddStudent()
    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added to the database!')
        return redirect(url_for('dashboard'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            print(f"There was an error with adding students: {err_msg}")
    return render_template('add.html', form=form)


@app.route("/delete/<int:id>", methods=["POST", "GET"])
# @login_required
def delete(id):
    student = Student.query.get(id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted!')
        return redirect(url_for('dashboard'))
    except Exception as e:
        print("Something went wrong", e)
        return redirect(url_for('dashboard'))


@app.route("/checkbox", methods=["GET", "POST"])
# @login_required
def handle_checkbox():
    if request.method == "POST":
        students = request.form.getlist('checkbox')
        for s in students:
            s = Student.query.get(s)
            db.session.delete(s)
            db.session.commit()
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('User created!')
            return redirect(url_for('dashboard'))
        flash('User creation failed.')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                flash('You\'re logged in!')
                return redirect(url_for('dashboard'))
        flash('Login failed')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))
