from students_db import app, db
from flask import render_template, request, redirect
from students_db.models import Student


@app.route('/')
def home():

    return render_template('index.html')

@app.route('/show', methods=['GET', 'POST'])
def show():

    if request.method == 'POST':

        students = ''
        student = Student(name=request.form.get('fullname'), email=request.form.get('email'), phone=request.form.get('phone'))
        db.session.add(student)
        db.session.commit()
  
    students = Student.query.all()
    return render_template('table.html', students=students)

@app.route("/delete/<int:id>", methods=["POST", "GET"])
def delete(id):
    student = Student.query.get(id)
    try:
        db.session.delete(student)
        db.session.commit()
        return redirect("/show")
    except:
        print("Something went wrong")
        return redirect("/show")

@app.route("/checkbox", methods=["GET", "POST"])
def handle_checkbox():
    if request.method == "POST":
        students = request.form.getlist('checkbox')
        for s in students:
            s = Student.query.get(s)
            db.session.delete(s)
            db.session.commit()
        return redirect('/show')
    return redirect('/')