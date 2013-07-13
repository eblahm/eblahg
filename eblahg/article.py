import webapp2
import render
import models


class main(webapp2.RequestHandler):
    def get(self, slug):
        this_article = models.Article.all().filter('slug =', slug).get()
        if this_article <> None:
            render.page(self, '/templates/main/article.html', {'article': this_article,
                                                               'title': this_article.title})
        else:
            render.not_found(self)
