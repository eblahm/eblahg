import webapp2
import models
import render
import pictures
__author__ = 'Matt'

class main(webapp2.RequestHandler):
    def get(self):
        v = {}
        v = pictures.random_pic_update(v)
        v['title'] = 'Home'
        v['results'] = models.articles.all().order('-pub_date')
        render.page(self, '/templates/main/landing.html', v)