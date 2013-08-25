import webapp2
import models
import render
import pictures


class main(webapp2.RequestHandler):
    def get(self, qtype="blog", tagslug = None):
        v = {}
        v = pictures.random_pic_update(v)

        if qtype == 'blog':
            v['title'] = 'Home'
            q = models.Article.all().order('-pub_date')
            q = q.filter('collection =', 'blog')

        elif qtype.lower() == 'tag' and tagslug != None:
            v['title'] = 'tag search'
            tag = models.Tag.get_by_key_name(tagslug)
            if tag == None:
                tagkey = None
                v['tag'] = tagslug
            else:
                tagkey = tag.key()
                v['tag'] = tag.name

            q = models.Article.all().filter('tags =', tagkey)

        v['Tag'] = models.Tag

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