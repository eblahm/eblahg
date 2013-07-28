import os
from google.appengine.ext import db
from eblahg.utility import seed_data
from eblahg.models import Article


APP_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

social_links = {
    # 'facebook': "http://www.facebook.com/mchalbe",
    'linkedin': "http://www.linkedin.com/pub/matthew-halbe/2b/a37/911/",
    # 'youtube': "http://www.youtube.com/mchalbe",
    'twitter_handle': "_yonant",
    'adn_handle': "eblah",
    # 'kippt': "https://kippt.com/mchalbe",
    # 'gplus': 'https://plus.google.com/116164959143674684741/',
    'github': "https://github.com/eblahm",
    'email': 'matthew.c.halbe@gmail.com',
}

settings = {
    'blog_title': "Eblahm",
    'author': 'Matt Halbe',
    'google_analytics': 'UA-11111111-1',
    'randomized_sidebar': True,
}
