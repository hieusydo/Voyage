# Import flask dependencies
from flask import Blueprint, request, render_template, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash

from application import db
from application.mod_auth.forms import LoginForm, SignupForm
from application.mod_auth.colorTheme import ColorForm, ColorTheme
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
    # print(user.password, ' ', form.password.data, ' ', check_password_hash(user.password, form.password.data))
    if user and check_password_hash(user.password, form.password.data):
        session['user_id'] = user.id
        session['username'] = user.name
        print("right!")
        return redirect(url_for('auth.home'))

    return redirect(url_for('auth.signin'))

@mod_auth.route('/register/')
def register():
    return render_template("auth/register.html")

@mod_auth.route('/register_account/', methods=['GET', 'POST'])
def register_account():
    form = SignupForm(request.form)

    #Check duplicate users
    user_to_check = User.query.filter_by(email=form.email.data).first()
    if user_to_check:
        print("Duplicate Email")
        return redirect(url_for("auth.register"))

    #Insert into db
    user_to_add = User(form.name.data, form.email.data, generate_password_hash(form.password.data))
    db.session.add(user_to_add)
    db.session.commit()
    print("Resgister Successful!")
    
    return redirect(url_for("auth.signin"))

@mod_auth.route('/home/', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.signin'))

    # Theme change
    form = ColorForm(request.form)
    if form.validate_on_submit():
        #Get user, there's only one user
        user = User.query.filter_by(id=session['user_id']).all()[0]
        colorTheme = ColorTheme(form)
        user.theme = colorTheme.themeString        
        db.session.commit()
        return redirect(url_for('map.display'))

    return render_template("auth/home.html", form = form)

@mod_auth.route('/logout/')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('auth.signin'))

@mod_auth.route('/color/', methods=['GET', 'POST'])
def color():
    if 'user_id' not in session:
        return redirect(url_for('auth.signin'))

    form = ColorForm(request.form)

    if form.validate_on_submit():
        #Get user, there's only one user
        user = User.query.filter_by(id=session['user_id']).all()[0]
        colorTheme = ColorTheme(form)
        user.theme = colorTheme.themeString
        
        db.session.commit()

        return redirect(url_for('map.display'))

    return render_template("auth/color.html", form = form)
