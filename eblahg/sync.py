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
from eblahg.utility import dropbox_api, dropox_info


class main(webapp2.RequestHandler):
    def get(self):
        v = {}
        db_info = dropox_info.get_by_key_name('DROPBOX_SECRETS')
        if db_info == None:
            # scenario 1 -> new user
            di = dropox_info(
                key_name='DROPBOX_SECRETS',
                app_key='oakhf7vqc9cqy6d',
                app_secret='gqod403qntsb51g'
            ) # initialize
            di.put() # initialize
            render.page(self, '/templates/main/dropbox.html', values=v)
        else:
            v.update({'app_key': db_info.app_key, 'app_secret': db_info.app_secret})
            DB = dropbox_api()
            pics_meta = DB.request_meta('/pics')
            if 'error' in pics_meta:
                if self.request.get('attempt') != '2':
                    # scenario 2 -> first attempt at oauth after inputing app key and secret
                    # redirect to handshake
                    self.redirect('/sync/login')
                else:
                    # scenario 3 -> oauth handshake fail
                    v.update({'wrong_key': True})
                    render.page(self, '/templates/main/dropbox.html', values=v)
            else:
                # scenario 4 -> user is authorized
                content = pics_meta
                render.page(self, '/templates/main/dropbox.html', values=v)
    def post(self):
        di = dropox_info.get_by_key_name('DROPBOX_SECRETS')
        di.app_key = self.request.get('app_key')
        di.app_secret = self.request.get('app_secret')
        di.save()
        self.redirect('/sync/login')

def sync_datastore():
    dropbox = dropbox_api()


class handshake(webapp2.RequestHandler):
    def get(self, mode="login"):
        if mode == 'login':
            callback = self.request.host_url + '/sync/initialize'
            dropbox = dropbox_api(callback)
            redirect_url = dropbox.client.get_authorization_url()
            self.redirect(redirect_url)
        if mode == 'initialize':
            request_token = self.request.get("oauth_token")
            request_secret = self.request.get("oauth_token_secret")
            dropbox = dropbox_api()
            data = dropbox.client.get_user_info(request_token, auth_verifier=request_secret)
            DB_info = dropox_info.get_by_key_name('DROPBOX_SECRETS')
            DB_info.usr_secret = data['secret']
            DB_info.usr_token = data['token']
            DB_info.put()

            # restart dropbox client with access token and secret
            dropbox = dropbox_api()
            # create the default file structure
            paths = ['/pics']
            for p in paths:
                params = {'root': 'sandbox', 'path': p}
                api_request = dropbox.create_folder(params)
            self.redirect('/dropbox?attempt=2')


