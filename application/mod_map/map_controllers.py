from flask import Blueprint, request, render_template, session, redirect, url_for

from application import db

mod_map = Blueprint('map', __name__, url_prefix='/map')

@mod_map.route('/display/')
def display():
    if 'user_id' not in session:
        return redirect(url_for('auth.signin'))

    return render_template("map/view.html")


    