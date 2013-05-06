import webapp2
from eblahg import admin


def http_error(h):
    h.response.out.write("404")


app = webapp2.WSGIApplication([('/config', admin.config_handler),
                               ('/admin/sync', admin.sync),
                               ('/admin/(.+)', admin.console),
                               ('/admin/', admin.console),
                               ('/admin', admin.console),
                               ('/.*', http_error),
                               ], debug=True)
