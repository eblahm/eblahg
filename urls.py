import webapp2
from eblahg import landing, rss, search, pictures, article, render, sync


app = webapp2.WSGIApplication([
        ('/', landing.main),
        ('/rss', rss.main),
        ('/tag/([-\w]+)', search.tag),
        ('/posts/(.+)', article.main),
        ('/search', search.term),
        ('/pics/(.*)', pictures.single),
        ('/p/(.*)', sync.draft),
        ('/.+', render.not_found),
    ], debug=True)

sync_agent = webapp2.WSGIApplication([
        ('/sync/(.+)', sync.handshake),
        ('/dropbox', sync.main),
        ('/.+', render.not_found),
    ], debug=True)