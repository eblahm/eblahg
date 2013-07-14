import os
from google.appengine.ext import db


APP_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

social_links = {
    # 'facebook': "http://www.facebook.com/mchalbe",
    'linkedin': "http://www.linkedin.com/pub/matthew-halbe/2b/a37/911/",
    # 'youtube': "http://www.youtube.com/mchalbe",
    'twitter': "http://twitter.com/_yonant",
    'adn': "https://alpha.app.net/eblah",
    # 'kippt': "https://kippt.com/mchalbe",
    # 'gplus': 'https://plus.google.com/116164959143674684741/',
    'github': "https://github.com/eblahm"
}

settings = {
    'blog_title': "Eblahg",
    'author': 'Matt Halbe',
    'email': 'matthew.c.halbe@gmail.com',
    'google_analytics': 'XXX',
    'randomized_sidebar': True,
}
