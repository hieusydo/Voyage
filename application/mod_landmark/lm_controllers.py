from flask import Blueprint, request, render_template, session, redirect, url_for
from flask.json import jsonify
from werkzeug import secure_filename
import urllib2, json

from application import db
from application.mod_landmark.lm_forms import AddLmForm
from application.mod_auth.models import Landmark

mod_landmark = Blueprint('landmark', __name__, url_prefix='/landmark')

@mod_landmark.route('/getAll/', methods=['GET'])
def getAll():
    if 'user_id' not in session:
        return redirect(url_for('auth.signin'))

    uid = session['user_id']
    landmarks = Landmark.query.filter_by(usrID=uid).all()
    print(landmarks)
    
    # Extract and reformat each landmark info
    allLms = []
    for l in landmarks:
        allLms.append((l.lmName, l.lmLat, l.lmLng, l.photoFileName, l.lmRating, l.lmComments))

    return jsonify({'landmarks': allLms})

@mod_landmark.route('/add/', methods=['GET', 'POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('auth.signin'))    
    
    form = AddLmForm()

    if form.validate_on_submit():
        # Store photo
        filename = secure_filename(form.photoFile.data.filename)
        
        # TODO: actually save the photo
        # form.photoFile.data.save('./../uploads/' + filename)

        # Simple parsing
        lmParseName = "+".join(form.lmName.data.split(" "))

        # Geocode the landmark! Call to Google Map API 
        geocodeURL = "https://maps.googleapis.com/maps/api/geocode/json?address="+\
                        lmParseName + "&key=AIzaSyDFHbK7fyCZ6ltg9VcHSOhtxKNdYeEQi9w"
        req = urllib2.Request(geocodeURL)
        res = urllib2.urlopen(req)
        data = json.load(res) # data is a dict 

        # Extract lattitude and longitude
        lat = 0
        lng = 0
        try:
            lat = data["results"][0]["geometry"]["location"]["lat"]
            lng = data["results"][0]["geometry"]["location"]["lng"]
            # print(form.lmName.data, lat, lng)
        except:
            # TODO: Handle when user-entered landmark can't be geocoded
            # print(data)
            print("Error reading json obj") 

        # Insert into db
        usrID = session['user_id']
        landmark = Landmark(usrID, form.lmName.data, lat, lng, filename, form.lmRating.data, form.lmComments.data)
        db.session.add(landmark)
        db.session.commit()

        # print(usrID, form.lmName.data, filename, form.lmRating.data, form.lmComments.data)

        return redirect(url_for('map.display'))

    return render_template("landmark/add.html", form=form)

    
