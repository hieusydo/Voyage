import os

DEBUG = bool(os.environ.get('V_DEBUG'))

# Define the database - we are working with Postgresql
SQLALCHEMY_DATABASE_URI = "postgresql://" + os.environ.get('RDS_USERNAME') + ":" + os.environ.get('RDS_PASSWORD')\
                            + "@" + os.environ.get('RDS_HOSTNAME') + ":" + os.environ.get('RDS_PORT') + "/"\
                            + os.environ.get('RDS_DB_NAME')
# # # print(SQLALCHEMY_DATABASE_URI)
# # DATABASE_CONNECT_OPTIONS = {}

SQLALCHEMY_TRACK_MODIFICATIONS = False
TEMPLATES_AUTO_RELOAD = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = os.environ.get('CSRF_SESSION_KEY')

# Secret key for signing cookies
SECRET_KEY = os.environ.get('SECRET_KEY')