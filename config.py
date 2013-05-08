import os
from google.appengine.ext import db


APP_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
APP_URL = 'http://eblahm.appspot.com'

social_links = {
    'facebook_url': "http://www.facebook.com/mchalbe",
    'linkedin_url': "http://www.linkedin.com/pub/matthew-halbe/2b/a37/911/",
    'youtube_url': "http://www.youtube.com/mchalbe",
    'twitter_url': "http://twitter.com/_yonant",
    'adn_url': "https://alpha.app.net/eblah",
    'kippt_url': "https://kippt.com/mchalbe",
    'gplus_url': 'https://plus.google.com/116164959143674684741/',
}


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
    randomized_sidebar = db.StringProperty(default='no',choices=['yes','no'])
