import webapp2
from eblahg import landing, rss, search, pictures, article, render, sync


app = webapp2.WSGIApplication([
        ('/', landing.main),
        ('/rss', rss.main),
        ('/posts/(.+)', article.main),
        ('/search', search.term),
        ('/pics/(.*)', pictures.single),
        ('/p/(.*)', sync.draft),
        ('/.+', render.not_found),
    ])

sync_agent = webapp2.WSGIApplication([
        ('/settings', sync.main),
        ('/sync/(.+)', sync.handshake),
        ('/.+', render.not_found),
    ])
