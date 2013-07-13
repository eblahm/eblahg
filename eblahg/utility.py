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
from HTMLParser import HTMLParser
import re
import models

class dropox_info(db.Model):
    app_key = db.StringProperty()
    app_secret = db.StringProperty()
    usr_token = db.StringProperty()
    usr_secret = db.StringProperty()

class dropbox_api():
    def __init__(self, callback_url=''):
        DB = dropox_info.get_by_key_name('DROPBOX_SECRETS')
        application_key = str(DB.app_key)
        application_secret = str(DB.app_secret)
        self.user_token = str(DB.usr_token)
        self.user_secret = str(DB.usr_secret)
        self.callback_url = callback_url
        self.client = oauth.DropboxClient(application_key,
                                          application_secret,
                                          callback_url)

    def request_file(self, path):
        api_url = 'https://api-content.dropbox.com/1/files/sandbox'
        api_url += urllib.quote(path)
        api_request = self.client.make_request(url=api_url,
                                               token=self.user_token,
                                               secret=self.user_secret)
        return api_request.content

    def request_meta(self, path):
        api_url = 'https://api.dropbox.com/1/metadata/sandbox' + urllib.quote(path)
        api_request = self.client.make_request(url=api_url, token=self.user_token, secret=self.user_secret)
        return json.loads(api_request.content)

    def create_folder(self, params, head={}):
        api_url = 'https://api.dropbox.com/1/fileops/create_folder'
        api_request = self.client.make_request(url=api_url,
                                               token=self.user_token,
                                               secret=self.user_secret,
                                               protected=True,
                                               additional_params=params,
                                               method=urlfetch.POST,
                                               headers=head)
        return api_request.content

    def upload_file(self, path, head={}, file_contents="", params={}):
        api_url = 'https://api-content.dropbox.com/1/files_put/sandbox' + path
        api_request = self.client.make_async_request(url=api_url,
                                               token=self.user_token,
                                               secret=self.user_secret,
                                               protected=True,
                                               additional_params=params,
                                               method=urlfetch.PUT,
                                               headers=head,
                                               body=file_contents)
        return api_request.get_result().content


def upload_pic(path, rev):
    dropbox = dropbox_api()
    this_pic = dropbox.request_file(path)
    this_pic = mb_limit(this_pic)
    try:
        title = re.search(r'([^\/]*)\..{,3}$', path).group(1)
    except:
        try:
            title = re.search(r'[^\/]*$').group(0)
        except:
            title = path
    new_picture = models.pics(
        key_name=path,
        title = title,
        pic = db.Blob(this_pic),
        sidebar = True,
    )
    new_picture.rev = rev
    new_picture.put()
    return new_picture

def mb_limit(pic):
    MB = 1000000.0
    if len(pic) > MB:
        degrade = int((MB/len(pic)) * 100)
        this_pic = images.Image(pic)
        this_pic.im_feeling_lucky()
        return this_pic.execute_transforms(output_encoding=images.JPEG, quality=degrade)
    else:
        return pic

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()