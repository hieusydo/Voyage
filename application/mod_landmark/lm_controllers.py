from flask import Blueprint, request, render_template, session, redirect, url_for
from flask.json import jsonify
from werkzeug import secure_filename, generate_password_hash
import urllib2, json, boto3, os

from application import db
from application.mod_landmark.lm_forms import AddLmForm
from application.mod_auth.models import Landmark, User
from application.mod_auth.colorTheme import ColorTheme

mod_landmark = Blueprint('landmark', __name__, url_prefix='/landmark')

# Allowed file extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS and \
           len(filename) <= 128

@mod_landmark.route('/getAll/', methods=['GET'])
def getAll():
    if 'user_id' not in session:
        return redirect(url_for('auth.signin'))

    uid = session['user_id']
    landmarks = Landmark.query.filter_by(usrID=uid).all()
    print(landmarks)

    user = User.query.filter_by(id=session['user_id']).all()[0]

    if (user.theme == ''):
        theme = eval(ColorTheme().themeString)
    else:
        theme = eval(user.theme)
    
    # Extract and reformat each landmark info
    allLms = []
    for l in landmarks:
        #allLms.append((l.lmPlaceID, l.lmName, l.lmLat, l.lmLng, l.photoFileURL, l.lmRating, l.lmComments))
        allLms.append({"place_id": l.lmPlaceID, "name": l.lmName,
                       "date_created": l.date_created,
                       "lat": l.lmLat, "lng": l.lmLng,
                       "photo_url": l.photoFileURL, "rating": l.lmRating,
                       "comment": l.lmComments})

    return jsonify({'landmarks': allLms, 'theme': theme})

@mod_landmark.route('/add/', methods=['GET', 'POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('auth.signin'))
    
    form = AddLmForm()

    if form.validate_on_submit():

        if len(form.lmName.data) > 128 or len(form.lmComments.data) > 192: 
            return

        # Store photo
        photo = form.photoFile.data
        # Filename is userid_landmarkname_filename
        photo.filename = '{}_{}_{}'.format(str(session['user_id']), form.lmName.data, photo.filename)
        if photo and allowed_file(photo.filename):
            # Hash filename to prevent "easy" access to photos
            photo.filename = generate_password_hash(photo.filename).split('$')[-1] + '.png'
            try:
                s3 = boto3.client('s3')
                s3.upload_fileobj(photo, os.environ.get('AWS_S3_BUCKET'), photo.filename, ExtraArgs={
                    "ContentType": photo.content_type
                })
            except Exception as e:
                print e

        # Simple parsing
        lmParseName = "+".join(form.lmName.data.split(" "))

        # Geocode the landmark! Call to Google Map API 
        geocodeURL = "https://maps.googleapis.com/maps/api/geocode/json?address="+\
                        lmParseName + "&key=AIzaSyDFHbK7fyCZ6ltg9VcHSOhtxKNdYeEQi9w"
        req = urllib2.Request(geocodeURL)
        res = urllib2.urlopen(req)
        data = json.load(res) # data is a dict

        # Possible problem with directly extracting place_id?
        placeID = data["results"][0]["place_id"]

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
        fileURL = 'https://{}.s3.amazonaws.com/{}'.format(os.environ.get('AWS_S3_BUCKET'), photo.filename)
        landmark = Landmark(placeID, usrID, form.lmName.data, lat, lng, fileURL, form.lmRating.data, form.lmComments.data)
        db.session.add(landmark)
        db.session.commit()

        # print(usrID, form.lmName.data, filename, form.lmRating.data, form.lmComments.data)

        return redirect(url_for('map.display'))

    return render_template("landmark/add.html", form=form)

    
