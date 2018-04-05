# Import flask and template operators
from flask import Flask, render_template, redirect, url_for

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Make cross-origin AJAX possible
from flask_cors import CORS

# Define the WSGI application object
application = Flask(__name__, static_folder="static", template_folder="templates")
CORS(application)

# Configurations
application.config.from_object('config')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['TEMPLATES_AUTO_RELOAD'] = True

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(application)

# Sample HTTP error handling
@application.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_map.map_controllers import mod_map as map_module
from app.mod_landmark.lm_controllers import mod_landmark as lm_module

# Register blueprint(s)
application.register_blueprint(auth_module)
application.register_blueprint(map_module)
application.register_blueprint(lm_module)
# application.register_blueprint(xyz_module)
# ..

@application.route("/")
def index():
    return redirect(url_for('auth.signin'))

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()


if __name__ == "__main__":
    # application.debug = True
    application.run()