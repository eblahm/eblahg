import fix_path
fix_path.fix()
from datetime import datetime

import webapp2
from google.appengine.ext import db
from google.appengine.api import taskqueue
from google.appengine.api import memcache
import oauth

from eblahg import models, render
from eblahg.utility import dropbox_api, dropox_info, upload_pic
from externals.pytz.gae import pytz


def sync_datastore():
    dropbox = dropbox_api()
    pics_meta = dropbox.request_meta('/pics')
    dstore = {}
    for p in models.pics.all():
        dstore[p.key().name()] = p.rev

    for remote in pics_meta.get('contents', []):
        dstore_rev = dstore.get(remote['path'], "")
        if dstore_rev != remote['rev']:
            taskqueue.add(url='/sync/upload',
                params={
                    'path': remote['path'],
                    'rev': remote['rev'],
                })
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
            # -> new user
            di = dropox_info(
                key_name='DROPBOX_SECRETS',
            ) # initialize
            di.put() # initialize
        else:
            # -> returning user
            v.update({'app_key': db_info.app_key, 'app_secret': db_info.app_secret})
        render.page(self, html_template, values=v)

    def post(self):
        v = {}
        di = dropox_info.get_by_key_name('DROPBOX_SECRETS')
        di.app_key = self.request.get('app_key')
        di.app_secret = self.request.get('app_secret')
        di.save()
        try:
            DB = dropbox_api()
        except:
            v['error'] = True
            render.page(self, html_template, values=v)

        if not v.get('error', False):
            meta = DB.request_meta('/pics')
            if 'error' in meta:
                # -> attempt oauth
                # redirect to handshake
                self.redirect('/sync/login')
            else:
                # -> user is authorized
                v.update({'app_key': di.app_key, 'app_secret': di.app_secret})
                sync_datastore()
                now = datetime.now().replace(tzinfo=pytz.utc)
                message = 'synced @ %s' % (now.astimezone(pytz.timezone('America/New_York')).strftime('%I:%M:%S%p %Z'))
                v['sync'] =  message
                render.page(self, html_template, values=v)






class handshake(webapp2.RequestHandler):
    def get(self, mode="login"):
        v = {}
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
            self.redirect('/dropbox')
    def post(self, mode):
        if mode == 'upload':
            path = self.request.get('path')
            rev = self.request.get('rev')
            upload_pic(path, rev)

