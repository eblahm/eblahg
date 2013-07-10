import fix_path
fix_path.fix()
import config
import urllib
import json
import re
from datetime import datetime
import webapp2
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import taskqueue
from google.appengine.api import memcache
from google.appengine.api import urlfetch
import oauth
import logging
from eblahg import models, render
from eblahg.utility import dropbox_api


class main(webapp2.RequestHandler):
    def get(self):
        render.page(self, '/templates/base.html', values={'dumb_content': 'sync here'})

class handshake(webapp2.RequestHandler):
    def get(self, mode="login"):
        callback = self.request.host_url + '/sync/initialize'
        try:
            dropbox = dropbox_api(callback)
            minimum_dbox_info = True
        except:
            minimum_dbox_info = False
        if minimum_dbox_info:
            if mode == 'login':
                redirect_url = dropbox.client.get_authorization_url()
                self.redirect(redirect_url)
            if mode == 'initialize':
                request_token = self.request.get("oauth_token")
                request_secret = self.request.get("oauth_token_secret")
                data = dropbox.client.get_user_info(request_token,
                                                    auth_verifier=request_secret)
                saved_settings = config.settings.get_by_key_name('SETTINGS')
                if saved_settings is None:
                    saved_settings = config.settings(key_name='SETTINGS')
                saved_settings.dropbox_usr_secret = data['secret']
                saved_settings.dropbox_usr_token = data['token']
                saved_settings.put()
                # restart dropbox client with access token and secret
                dropbox = dropbox_api()
                # create the default file structure
                paths = ['/published', '/pics', 'sidebar_pics']
                for p in paths:
                    params = {'root': 'sandbox', 'path': p}
                    api_request = dropbox.create_folder(params)
                self.redirect('/sync')
        else:
            self.redirect('/sync')

