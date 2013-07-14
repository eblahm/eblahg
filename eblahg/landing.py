import webapp2
import models
import render
import pictures


class main(webapp2.RequestHandler):
    def get(self):
        v = {}
        v['title'] = 'Home'
        v = pictures.random_pic_update(v)

        q = models.Article.all().order('-pub_date')
        if self.request.get('o') != "":
            offset = int(self.request.get('o'))
        else:
            offset = 0
        v['results'] = q.fetch(10, offset=offset)
        v['count'] = q.count(offset=offset, limit=10)
        v['offset'] = offset + 10

        if offset == 0:
            render.page(self, '/templates/main/landing.html', v)
        else:
            render.page(self, '/templates/main/article_links.html', v)