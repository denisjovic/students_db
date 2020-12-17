import os
from flask import Flask, redirect, render_template, flash, url_for, request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "studentsdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = 'some random secret key'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone = db.Column(db.String(30))

# app = Flask(__name__)

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
    # flash('Student added to the database!')
    return render_template('table.html', students=students)

@app.route("/delete/<int:id>", methods=["POST", "GET"])
def delete(id):
    student = Student.query.get(id)
    try:
        db.session.delete(student)
        db.session.commit()
        # flash("Deleted!")
        return redirect("/show")
    except:
        # flash('Something went wrong, deleting failed.')
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



if __name__ == "__main__":
    app.run(debug=True)


# >>> from bookmanager import db
# >>> db.create_all()
# >>> exit()