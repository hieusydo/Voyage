from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

from werkzeug import secure_filename

from app import db

from app.mod_landmark.lm_forms import AddLmForm

from app.mod_auth.models import Landmark

mod_landmark = Blueprint('landmark', __name__, url_prefix='/landmark')

@mod_landmark.route('/add/', methods=['GET', 'POST'])
def add():
    form = AddLmForm()

    if form.validate_on_submit():
        # Store photo
        filename = secure_filename(form.photoFile.data.filename)
        # form.photoFile.data.save('./../uploads/' + filename)

        # Insert into db
        usrID = session['user_id']
        landmark = Landmark(usrID, form.lmName.data, filename, form.lmRating.data, form.lmComments.data)
        db.session.add(landmark)
        db.session.commit()

        print(usrID, form.lmName.data, filename, form.lmRating.data, form.lmComments.data)

        return redirect(url_for('auth.home'))

    return render_template("landmark/add.html", form=form)

    
