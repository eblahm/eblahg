import fix_path
fix_path.fix()
import config
import oauth

import urllib
import json


class dropbox_api():
    def __init__(self, callback_url=''):
        settings = config.settings.get_by_key_name('SETTINGS')
        application_key = str(settings.dropbox_app_key)
        application_secret = str(settings.dropbox_app_secret)
        self.user_token = str(settings.dropbox_usr_token)
        self.user_secret = str(settings.dropbox_usr_secret)
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


class console(webapp2.RequestHandler):
    def get(self, mode="login"):
        # Get your app key and secret from the Dropbox developer website
        if 'localhost' in self.request.url or '127.0.0' in self.request.url:
            callback = self.request.url
            callback = callback.replace('/admin', '')
            callback = callback.replace('/login', '')
        else:
            callback = config.APP_URL
        callback += '/admin/initialize'
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
                self.redirect('/config?m=1')
        else:
            self.redirect('/config')

render.page(self, '/templates/base.html', values={'dumb_content': status_message})