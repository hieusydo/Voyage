from flask import Blueprint, request, render_template, redirect, url_for

from application import db

mod_map = Blueprint('map', __name__, url_prefix='/map')

@mod_map.route('/display/')
def display():
    return render_template("map/view.html")


    