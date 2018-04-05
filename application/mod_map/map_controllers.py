# Import flask dependencies
from flask import Blueprint, request, render_template, redirect, url_for

# Import the database object from the main app module
from application import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_map = Blueprint('map', __name__, url_prefix='/map')


@mod_map.route('/display/')
def display():
    return render_template("map/view.html")


    