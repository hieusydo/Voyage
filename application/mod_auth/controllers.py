# Import flask dependencies
from flask import Blueprint, request, render_template, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
# from application import db

# Import module forms
from application.mod_auth.forms import LoginForm

# Import module models (i.e. User)
from application.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@mod_auth.route('/signin/')
def signin():
    return render_template("auth/signin.html")

@mod_auth.route('/verify/', methods=['GET', 'POST'])
def verify():
    form = LoginForm(request.form)

    # if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and check_password_hash(user.password, form.password.data):
        session['user_id'] = user.id
        print("right!")
        return redirect(url_for('auth.home'))

    return redirect(url_for('auth.signin'))

@mod_auth.route('/home/')
def home():
    return render_template("auth/home.html")

@mod_auth.route('/logout/')
def logout():
    return redirect(url_for('auth.signin'))
