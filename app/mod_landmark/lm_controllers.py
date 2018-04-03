# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_landmark = Blueprint('landmark', __name__, url_prefix='/landmark')


@mod_landmark.route('/add/')
def add():
    return render_template("landmark/add.html")

    