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
from eblahg.utility import dropbox_api, dropox_info, upload_pic


def sync_datastore():
    dropbox = dropbox_api()
    pics_meta = dropbox.request_meta('/pics')

    if 'error' in pics_meta:
        assert False
    else:
        dstore = {}
        for p in models.pics.all():
            dstore[p.path] = p.rev

        for remote in pics_meta['contents']:
            dstore_rev = dstore.get(remote['path'], "")
            if dstore_rev != remote['rev']:
                upload_pic(remote['path'], remote['rev'])
                if dstore_rev != "":
                    dstore.pop(remote['path'])

        for deleted in dstore:
            rec = models.pics.get_by_key_name(deleted)
            rec.delete()
    return True

html_template = '/templates/main/dropbox.html'

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
            render.page(self, html_template, values=v)
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
                    v.update({'error': True})
                    render.page(self, html_template, values=v)
            else:
                # scenario 4 -> user is authorized
                content = pics_meta
                render.page(self, html_template, values=v)
    def post(self):
        v = {}
        di = dropox_info.get_by_key_name('DROPBOX_SECRETS')
        di.app_key = self.request.get('app_key')
        di.app_secret = self.request.get('app_secret')
        di.save()
        v.update({'app_key': di.app_key, 'app_secret': di.app_secret})
        sync_datastore()
        v.update({'sync': True})
        render.page(self, html_template, values=v)
        # except:
        #     v.update({'error': True})
        #     render.page(self, html_template, values=v)





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
            sync_datastore()
            self.redirect('/dropbox')



