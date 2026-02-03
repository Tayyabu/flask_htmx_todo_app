from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length,Email





class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2)])
    email = EmailField("Email",validators=[DataRequired(), Length(min=2),Email("Email Required")])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password")
 

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Length(min=2)])
    password = PasswordField("Password", validators=[DataRequired(), ])



class TodoForm(FlaskForm):
     title = StringField("Title",validators=[DataRequired(), Length(min=2)])
     content = TextAreaField("Content",validators=[DataRequired(), Length(min=2)])
      