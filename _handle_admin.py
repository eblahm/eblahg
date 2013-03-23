import webapp2
from eblahm import admin

def http_error (h):
    h.response.out.write("404")

app = webapp2.WSGIApplication([('/admin/config', admin.config_handler),
                               ('/admin/console', admin.console),
                               ('/admin/console/(.+)', admin.console),
                               ('/admin/edit', admin.edit),
                               ('/admin/sync', admin.sync),
                               ('/admin', admin.console),
                               ('/.*', http_error),
                               ],debug=True)