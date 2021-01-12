from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, DataRequired


class RegisterForm(FlaskForm):
    name = StringField(label='Full name', validators=[Length(min=3, max=15), DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    phone = StringField(label='Phone', validators=[Length(min=6, max=9), DataRequired()])
    department = StringField(label='Department', validators=[Length(min=2, max=30), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=3), DataRequired()])
    submit_data = SubmitField(label='Submit')


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit_data = SubmitField(label='Login')


class AddStudent(FlaskForm):
    name = StringField(label='Full name', validators=[Length(min=3, max=20), DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    phone = StringField(label='Phone', validators=[Length(min=6, max=9), DataRequired()])
    department = StringField(label='Department', validators=[Length(min=3, max=30), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=5), DataRequired()])
    submit_data = SubmitField(label='Add student')


class Filter(FlaskForm):
    search = StringField(label='Search...')
