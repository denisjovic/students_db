from students_db import app
from students_db import db
from flask import render_template, request, redirect, url_for, session, flash, Markup
from students_db.models import Student, User
from students_db.forms import RegisterForm, AddStudent, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user


@app.route('/')
@app.route('/show')
@login_required
def dashboard():
    students = User.query.all()
    return render_template('table.html', students=students)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddStudent()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        student = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            department=form.department.data,
            password_hash=hashed_password
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added to the database!', category='info')
        return redirect(url_for('dashboard'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            print(f"There was an error with adding students: {err_msg}")
    return render_template('add.html', form=form)


@app.route("/delete/<int:id>", methods=["POST", "GET"])
@login_required
def delete(id):
    student = User.query.get(id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash(f'Student {student.name} has been deleted!', category='info')
        return redirect(url_for('dashboard'))
    except Exception as e:
        print(e)
        flash("Something went wrong")
        return redirect(url_for('dashboard'))


@app.route("/checkbox", methods=["GET", "POST"])
@login_required
def handle_checkbox():
    if request.method == "POST":
        students = request.form.getlist('checkbox')
        for student in students:
            del_student = User.query.get(student)
            db.session.delete(del_student)
            db.session.commit()
            flash(f"Student {del_student.name} has been deleted!", category="info")
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    message = Markup(
        'User already exists! Would you like to <a href="/login">log in </a> instead?')
    if request.method == 'POST' and form.validate():
        if User.query.filter_by(email=form.email.data).first():
            flash(message, category='info')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = User(name=form.name.data,
                        email=form.email.data,
                        phone=form.phone.data,
                        department=form.department.data,
                        password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created!', category='info')
        login_user(new_user)
        return redirect(url_for('dashboard'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    message = Markup(
        'Account does not exist, do you want to <a href="/register">create</a> one instead?')
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash(message, category='info')
            return redirect(url_for('login'))
        if check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('dashboard')
            flash('Logged in!', category='info')
            return redirect(url_for('dashboard'))

        flash('Username or password incorrect', category='danger')
        return redirect(url_for('login'))

    if form.errors != {}:
        for err in form.errors.values():
            flash(err, category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You\'re logged out!', category='info')
    return redirect(url_for('login'))


@app.route('/profile/<int:id>', methods=["GET", "POST"])
def profile(id):
    user_to_update = User.query.get(id)
    form = AddStudent(obj=user_to_update)
    if request.method == 'POST':
        form.populate_obj(user_to_update)
        db.session.commit()
        flash('User data updated!', category='success')
        return redirect(url_for('dashboard'))
    return render_template('profile.html', profile=user_to_update, form=form)

