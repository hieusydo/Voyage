# Voyage - A Visual Travel Journal


## Demo

App is live on AWS! http://voyage.fkqpxtepmm.us-west-2.elasticbeanstalk.com (at least until my credits run out...)

Screenshots:

![view-map](demo/view-map.png)

![collage-req](demo/collage-req.png)

![collage-res](demo/collage-res.png)

And more in the `demo/` folder!


## Todo

MVP: 
- [x] Login (`mod_auth`): Used Flask session to validate each view when the user log in/out
- [x] Register
- [x] (Basic) Add a landmark (`mod_landmark`): Used [Google Geocode](https://developers.google.com/maps/documentation/geocoding/intro) to parse the landmark name entered by the user to a coordinate. 
- [x] (Basic) View landmarks & render on map (`mod_map`): All users' landmarks are queried from the database (see `viewMap.js`) and drawn on the map as a simple red marker. Ref: [Custom style for map](https://developers.google.com/maps/documentation/javascript/styling) and [custom markers](https://developers.google.com/maps/documentation/javascript/custom-markers)

More: 
- [x] Red marker should be clickable and info about its ratings and photos should be displayed. 
https://developers.google.com/maps/documentation/javascript/examples/place-details
- [x] Picture needs to be stored in database. Right now the only thing stored is the filename
- [x] Theme management
- [x] Photo collage generator



## Installation instructions

**Note: The project is created using Python 2.x**

1. Instal `pip` 
1. Install `virtualenv`
1. Clone the repo. Create your own branch to work on. 
1. `cd Voyage` and then `virtualenv your-env` to create your new virtual environment, and activate it.
1. Install all dependencies: `(your-env)$ pip install -r requirements.txt`
1. To run the app locally: `(your-env)$ python application.py` 

**You must set your environment variables in order to connect to the database**


## How the app flows

- Example flow of mod_auth: 
   - import the **controllers** in main `__init__.py` 
   - controllers import **models** (interacting with DB) and **forms** (dependent module)


## Databases

- Install [Postgresql](https://www.postgresql.org/)


## Deployment on AWS

- [x] Flask app deployed on AWS Elasticbeanstalk 
- [x] PostgreSQL database deployed on AWS RDS 


## Materials on Flask
- http://flask.pocoo.org/docs/0.12/
- https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications

