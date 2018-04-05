# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm 
from wtforms import TextField, PasswordField 
from wtforms.validators import Required, Email

# Define the login form (WTForms)
class LoginForm(FlaskForm):
    email    = TextField('Email Address', [Email(),
                Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                Required(message='Must provide a password')])