from flask import Flask, render_template, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

# EB looks for an 'application' callable by default.
application = Flask(__name__)

application.config.from_object('config')


# Define the database object 
db = SQLAlchemy(application)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()


# Import a module / component using its blueprint handler variable
from application.mod_auth.controllers import mod_auth as auth_module
from application.mod_map.map_controllers import mod_map as map_module
from application.mod_landmark.lm_controllers import mod_landmark as lm_module

# Register blueprints
application.register_blueprint(auth_module)
application.register_blueprint(map_module)
application.register_blueprint(lm_module)


@application.route("/")
def index():
    return redirect(url_for('auth.signin'))

# HTTP error handling
@application.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
