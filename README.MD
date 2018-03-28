# Voyage - A Visual Travel Journal

## Todo

MVP: 
- [x] Login
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
1. Install all dependencies: `env/bin/pip install -r requirements.txt`
1. `env/bin/python run.py` to run the app locally


## Databases

- Install [Postgresql](https://www.postgresql.org/)


## Flask Blueprints

- Flow of mod_auth: 
   - import the **controllers** in main `__init__.py` 
   - controllers import **models** (interacting with DB) and **forms** (dependent module)



## References

- https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications
- http://flask.pocoo.org/docs/0.12/design/
- https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example