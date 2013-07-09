import webapp2
import render
import models


class main(webapp2.RequestHandler):
    def get(self, slug):
        this_article = models.articles.all().filter('slug =', slug).get()
        if this_article <> None:
            this_pic = models.pics.all().ancestor(this_article).get()
            render.page(self, '/templates/main/article.html', {'article': this_article,
                                                               'picture': this_pic,
                                                               'title': this_article.title})
        else:
            render.not_found(self)
