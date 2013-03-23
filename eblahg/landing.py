import webapp2
import models
import render
import random
import tools
import urllib
from google.appengine.api import search
from google.appengine.ext import db
from google.appengine.api import memcache
__author__ = 'Matt'

class main(webapp2.RequestHandler):
    def get(self):
        v = {}
        v['title'] = 'Home'
        folder_serialized = tools.get_memcached_data('sidebar', models.pics.all().filter('collection =', 'sidebar').run(limit=2000), format='serialized')
        limit = len(folder_serialized) - 1
        if limit >= 1:
            ran_num = random.randint(0, limit)
            random_pic = db.get(folder_serialized[ran_num])
        else:
            random_pic = models.pics.all().filter('collection =', 'sidebar').get()
        try:
            v['random_picture_key'] = str(random_pic.key())
            v['random_picture_path'] = urllib.quote(random_pic.key().name())
        except:
            pass
        v['results'] = models.articles.all().order('-pub_date')
        render.page(self, '/templates/main/landing.html', v)