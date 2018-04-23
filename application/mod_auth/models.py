from application import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'auth_user'

    # User Name
    name    = db.Column(db.String(128),  nullable=False)

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    password = db.Column(db.String(192),  nullable=False)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    # Map Theme
    theme    = db.Column(db.String(5000), nullable = True)

    landmarks = db.relationship("Landmark", backref="user", lazy=True)

    # New instance instantiation procedure
    def __init__(self, name, email, password):

        self.name     = name
        self.email    = email
        self.password = password
        self.role     = 1
        self.status   = 1
        self.theme = "[{'stylers': [{'color': '#ebe3cd'}], 'elementType': 'geometry'}, {'stylers': [{'color': '#523735'}], 'elementType': 'labels.text.fill'}, {'stylers': [{'color': '#f5f1e6'}], 'elementType': 'labels.text.stroke'}, {'featureType': 'administrative', 'elementType': 'geometry.stroke', 'stylers': [{'color': '#c9b2a6'}]}, {'featureType': 'administrative.land_parcel', 'elementType': 'geometry.stroke', 'stylers': [{'color': '#dcd2be'}]}, {'featureType': 'administrative.land_parcel', 'elementType': 'labels.text.fill', 'stylers': [{'color': '#ae9e90'}]}, {'featureType': 'landscape.natural', 'elementType': 'geometry', 'stylers': [{'color': '#dfd2ae'}]}, {'featureType': 'poi', 'elementType': 'geometry', 'stylers': [{'color': '#dfd2ae'}]}, {'featureType': 'poi', 'elementType': 'labels.text.fill', 'stylers': [{'color': '#93817c'}]}, {'featureType': 'poi.park', 'elementType': 'geometry.fill', 'stylers': [{'color': '#a5b076'}]}, {'featureType': 'poi.park', 'elementType': 'labels.text.fill', 'stylers': [{'color': '#447530'}]}, {'featureType': 'road', 'stylers': [{'visibility': 'off'}]}, {'featureType': 'road', 'elementType': 'geometry', 'stylers': [{'color': '#f5f1e6'}]}, {'featureType': 'road.arterial', 'elementType': 'geometry', 'stylers': [{'color': '#fdfcf8'}]}, {'featureType': 'road.highway', 'elementType': 'geometry', 'stylers': [{'color': '#f8c967'}]}, {'featureType': 'road.highway', 'elementType': 'geometry.stroke', 'stylers': [{'color': '#e9bc62'}]}, {'featureType': 'road.highway.controlled_access', 'elementType': 'geometry', 'stylers': [{'color': '#e98d58'}]}, {'featureType': 'road.highway.controlled_access', 'elementType': 'geometry.stroke', 'stylers': [{'color': '#db8555'}]}, {'featureType': 'road.local', 'elementType': 'labels.text.fill', 'stylers': [{'color': '#806b63'}]}, {'featureType': 'transit.line', 'elementType': 'geometry', 'stylers': [{'color': '#dfd2ae'}]}, {'featureType': 'transit.line', 'elementType': 'labels.text.fill', 'stylers': [{'color': '#8f7d77'}]}, {'featureType': 'transit.line', 'elementType': 'labels.text.stroke', 'stylers': [{'color': '#ebe3cd'}]}, {'featureType': 'transit.station', 'elementType': 'geometry', 'stylers': [{'color': '#dfd2ae'}]}, {'featureType': 'water', 'elementType': 'geometry.fill', 'stylers': [{'color': '#b9d3c2'}]}, {'featureType': 'water', 'elementType': 'labels.text.fill', 'stylers': [{'color': '#92998d'}]}]"

    def __repr__(self):
        return '<User %r>' % (self.name)  

# Many to One relationship with User
class Landmark(Base):
    __tablename__ = 'landmark'

    lmPlaceID = db.Column(db.String(128),  nullable=False)
    usrID = db.Column(db.Integer, db.ForeignKey("auth_user.id"), nullable=False)
    lmName = db.Column(db.String(128),  nullable=False)
    lmLat = db.Column(db.Float, nullable=False)
    lmLng = db.Column(db.Float, nullable=False)
    photoFileURL = db.Column(db.String(128),  nullable=False)
    lmRating = db.Column(db.SmallInteger, nullable=False)
    lmComments = db.Column(db.String(192),  nullable=False)

    def __init__(self, pid, uid, name, lat, lng, url, rating, comments):
        self.lmPlaceID = pid
        self.usrID = uid
        self.lmName = name
        self.lmLat = lat
        self.lmLng = lng
        self.photoFileURL = url
        self.lmRating = rating
        self.lmComments = comments

    def __repr__(self):
        return '<Landmark %r>' % (self.lmName)  
