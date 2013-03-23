import webapp2
from eblahg import landing, rss, search, pictures, helper, article


app = webapp2.WSGIApplication([('/', landing.main),
                               ('/rss', rss.main),
                               ('/tag/([-\w]+)', search.tag),
                               ('/posts/(.+)', article.main),
                               ('/search', search.term),
                               ('/pic/sbar', pictures.sbar),
                               ('/pic', pictures.single),
                               ('/pics/(.+)', pictures.all),
                               ('/(.+)', article.main),
                               ],
                                debug=True)


