# Voyage - A Visual Travel Journal

## Todo
MVP: 
- [ ] Login
- [ ] Add a landmark
- [ ] View landmarks
- [ ] Overlay over the map: by city, state, country, etc.

More: 
- [ ] Register
- [ ] Photo collage - db needs to support storing images
- [ ] Recommendation system
- [ ] Theme management

## Instructions
1. Instal `pip` 
1. Install `virtualenv`
1. `cd Voyage` and then `virtualenv env` to create a new virtual environment
1. Install all dependencies
   ```
   env/bin/pip install flask
   env/bin/pip install flask-sqlalchemy
   env/bin/pip install flask-wtf
   ```
1. `env/bin/python run.py` to run the app locally

## References
- https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications
- http://flask.pocoo.org/docs/0.12/design/
- https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example