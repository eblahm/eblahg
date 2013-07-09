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

settings = {
    'blog_title': "Eblahg",
    'author': 'Matt Halbe',
    'email': 'matthew.c.halbe@gmail.com',
    'google_analytics': 'XXX',
    'randomized_sidebar': True,
}
