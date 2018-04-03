# Import flask and template operators
from flask import Flask, render_template, redirect, url_for

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__, static_folder="static", template_folder="templates")

# Configurations
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_map.map_controllers import mod_map as map_module
from app.mod_landmark.lm_controllers import mod_landmark as lm_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(map_module)
app.register_blueprint(lm_module)
# app.register_blueprint(xyz_module)
# ..

@app.route("/")
def index():
    return redirect(url_for('auth.signin'))

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()