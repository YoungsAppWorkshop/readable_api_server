# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

# Define the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'readable.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

# Secret key for signing cookies
SECRET_KEY = "YOUR_SECRET_KEY_HERE"
