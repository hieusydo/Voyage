import os

from flask import Flask, render_template, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

import os

# EB looks for an 'application' callable by default.
application = Flask(__name__)

application.config.from_object('config')


# Define the database object 
db = SQLAlchemy(application)


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

# Cache buster for templates - Ref: http://flask.pocoo.org/snippets/40/
# Force viewMap.js to reload from source for ez debuggin'
if bool(os.environ.get('V_DEBUG')):
    @application.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    def dated_url_for(endpoint, **values):
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename:
                file_path = os.path.join(application.root_path,
                                         endpoint, filename)
                values['q'] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)


# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

# Initialize boto3 config/credentials
# Make a function to avoid polluting global namespace
def initBotoConfig():
    if not os.path.exists('.aws'):
        os.makedirs('.aws')

    # Create default config file if it doesn't exist
    if not os.path.isfile('.aws/config'):
        configfile = open('.aws/config', 'w+')
        configfile.write("[default]\noutput = json\nregion = us-east-1")
        configfile.close()
    
    if not os.path.isfile('.aws/credentials'):
        credentialfile = open('.aws/credentials', 'w+')
        credentialfile.write("[default]\naws_access_key_id = " + os.environ.get('AWS_ACCESS_KEY_ID') + "\n")
        credentialfile.write("aws_secret_access_key = " + os.environ.get('AWS_SECRET_ACCESS_KEY'))
        credentialfile.close()
    
    # Set required environment variables
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '.aws/credentials'
    os.environ['AWS_CONFIG_FILE'] = '.aws/config'

initBotoConfig()