# Import flask dependencies
from flask import Blueprint, request, render_template, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash

from application.mod_auth.forms import LoginForm
from application.mod_auth.models import User

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
    if 'user_id' not in session:
        return redirect(url_for('auth.signin'))

    return render_template("auth/home.html")

@mod_auth.route('/logout/')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.signin'))
