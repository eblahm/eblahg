import os
from google.appengine.api import memcache
from google.appengine.ext import db

APP_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
APP_URL = 'http://eblahm.appspot.com'

# input data to datastore using the form @ /admin/config

class settings(db.Model):
    blog_title = db.StringProperty()
    author = db.StringProperty()
    email = db.StringProperty()
    url = db.StringProperty()
    google_analytics = db.StringProperty()
    dropbox_app_key = db.StringProperty()
    dropbox_app_secret = db.StringProperty()
    dropbox_usr_token = db.StringProperty()
    dropbox_usr_secret = db.StringProperty()