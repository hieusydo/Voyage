from flask import Blueprint, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField

from application.mod_collage.photoManip import generateCollage
from application.mod_auth.models import Landmark

mod_collage = Blueprint('collage', __name__, url_prefix='/collage')

# Represents the collage form
class AddColForm(FlaskForm):
    landmark1 = SelectField("Landmark 1")
    landmark2 = SelectField("Landmark 2")

    # Allows setting the 'choices' field after creation
    def setChoices(self, landmarks):
        self.landmark1.choices = landmarks
        self.landmark2.choices = landmarks

@mod_collage.route('/get/', methods=['GET', 'POST'])
def picTest():
    if 'user_id' not in session:
        return redirect(url_for('auth.signin'))

    # Get landmarks by id
    uid = session['user_id']
    landmarks = Landmark.query.filter_by(usrID=uid).all()
    landmarks.sort(key=lambda x: x.lmName)

    print "picTest", landmarks

    # Create a list of value,display tuples from the landmarks
    choices = []
    for i in landmarks:
        choices.append((i.photoFileURL, i.lmName))

    # Create and set the form choices
    form = AddColForm()
    form.setChoices(choices)

    if form.validate_on_submit():
        print "picTest about to generateCollage..."
        url = generateCollage(form.landmark1.data, form.landmark2.data)
        print "picTest done generateCollage"
        return render_template('collage/result.html', image_url=url)


    return render_template('collage/request.html', form=form)