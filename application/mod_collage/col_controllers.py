from flask import Blueprint, render_template

mod_collage = Blueprint('collage', __name__, url_prefix='/collage')

@mod_collage.route('/get/')
def picTest():
    return render_template('collage/test.html')