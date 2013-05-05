import fix_path
fix_path.fix()
import config
import urllib2
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
import config
from eblahg import models, tools, render





class dropbox_api():
    def __init__(self, callback_url='http://localhost:8080/admin/console/verify'):
        settings = config.settings.get_by_key_name('SETTINGS', read_policy=db.STRONG_CONSISTENCY)
        application_key = str(settings.dropbox_app_key)
        application_secret = str(settings.dropbox_app_secret)
        self.user_token = str(settings.dropbox_usr_token)
        self.user_secret = str(settings.dropbox_usr_secret)
        self.callback_url = callback_url
        self.client = oauth.DropboxClient(application_key, application_secret, callback_url)

    def request_file(self, path):
        api_url = 'https://api-content.dropbox.com/1/files/sandbox' + urllib.quote(path)
        api_request = self.client.make_request(url=api_url, token=self.user_token, secret=self.user_secret)
        return api_request.content

    def request_meta(self, path):
        api_url = 'https://api.dropbox.com/1/metadata/sandbox' + urllib.quote(path)
        api_request = self.client.make_request(url=api_url, token=self.user_token, secret=self.user_secret)
        return json.loads(api_request.content)
    def upload_file(self, path, params, head):
        api_url = 'https://api-content.dropbox.com/1/files/sandbox' + urllib.quote(path)
        api_request = self.client.make_request(api_url, self.user_token, self.user_secret, additional_params=params, protected=False, method=urlfetch.POST, headers=head)
        return api_request.content


def mb_limit(pic):
    MB = 1000000.0
    if len(pic) > MB:
        degrade = int((MB/len(pic)) * 100)
        this_pic = images.Image(pic)
        this_pic.im_feeling_lucky()
        return this_pic.execute_transforms(output_encoding=images.JPEG, quality=degrade)
    else:
        return pic


def upload_pic(path, rev, collection='main', blog_post_key=None):
    dropbox = dropbox_api()
    this_pic = dropbox.request_file(path)
    this_pic = mb_limit(this_pic)
    new_picture = models.pics(
        key_name=path,
        title = path.replace('/pics/',"").replace('.jpg', "").replace('sidebar/',""),
        pic = db.Blob(this_pic),
        parent = blog_post_key,
        collection = collection)
    new_picture.rev = rev
    new_picture.put()
    return new_picture

def upload(path, this_rev, last_updated=datetime(1947, 11, 11, 11)):
    dropbox = dropbox_api()
    text = dropbox.request_file(path)
    header = {'title':None, 'date':None, 'pics':None, 'tags':"", 'slug':""}

    for meta_item in header:
        my_regex = r'%s:(.+)\n' % (meta_item)
        re_search = re.search(my_regex, text)
        if re_search <> None:
            header[meta_item] = re_search.group(1).strip()
        flush_regex = r'%s:.+\n' % (meta_item)
        text = re.sub(flush_regex, "", text)
    if header['date'] == None:
        header['date'] = datetime.now()
    else:
        header['date'] = datetime.strptime(header['date'].upper(), '%m-%d-%Y %I:%M%p')
    if header['title'] == None:
        header['title'] = re.search('posts/(.*?)\..+$', path).group(1)

    new_post = models.articles(
        key_name = str(path),
        title = header['title'].decode('utf-8', 'ignore'),
        pub_date = header['date'],
        body = text.decode('utf-8', 'ignore'),
        tags = [tag.strip() for tag in header['tags'].split(",") if tag.strip() <> ""],
        last_updated = last_updated,
        rev = this_rev,
        )
    new_post.put()

    if header['pics'] <> None:
        existing_pic = models.pics.all().ancestor(new_post).get()
        if existing_pic <> None:
            existing_pic.delete()
        for pic_name in header['pics'].split(","):
            simple_name = pic_name.strip().replace('"', "")
            path = '/pics/' + simple_name + '.jpg'
            upload_pic(path, None, 'main', new_post.key())

    return "good"


class console(webapp2.RequestHandler):
    def get(self, mode="all"):
        # Get your app key and secret from the Dropbox developer website
        dropbox = dropbox_api()

        if mode == "login":
            redirect_url = dropbox.client.get_authorization_url()
            self.redirect(redirect_url)

        if mode == 'verify':
            request_token = self.request.get("oauth_token")
            request_secret = self.request.get("oauth_token_secret")
            data = dropbox.client.get_user_info(request_token, auth_verifier=request_secret)
            saved_settings = config.settings.get_by_key_name('SETTINGS', read_policy=db.STRONG_CONSISTENCY)
            if saved_settings == None:
                saved_settings = config.settings(key_name='SETTINGS')
            saved_settings.dropbox_usr_secret = data['secret']
            saved_settings.dropbox_usr_token = data['token']
            saved_settings.put()
            self.redirect('/admin/console')
           # head = {}
           # params = {}

           # h = {}
           # h['Content-Type'] = 'text/plain'
           # h['Content-Transfer-Encoding'] = 'utf-8'
           # h['Content-disposition'] = 'attachment; filename="foo.md"'

           # params = {'file': (h, urllib2.urlopen('https://dl.dropbox.com/u/10718699/Hello%20World.md').read())}

           # api_request = dropbox.upload_file('/posts', params, head)
           # self.response.out.write(api_request)


        if mode == "all":
            v = {}
            data = dropbox.request_meta('/posts')

            drafts = []
            published = []
            try:
                folder_contents = data['contents']
                auth = True
            except:
                auth = False

            if auth == False:
                incoming_url = self.request.url
                re_url = '/admin/console/login?callback=' + urllib.quote(incoming_url) + urllib.quote("?initialize=yes")
                self.redirect(re_url)
            else:
                for a in folder_contents:
                    rec = models.articles.get_by_key_name(str(a['path']))

                    class article:
                        title = a['path'].replace('/posts/', "").replace('.md', "")
                        last_updated = datetime.strptime(a['modified'], "%a, %d %b %Y %H:%M:%S +0000")
                        tags = ""
                        path = urllib.quote(a['path'])
                        rev = a['rev']
                        if rec <> None:
                            pub_date = rec.pub_date
                        if rec == None:
                            status = 'Draft'
                        elif rec.rev == rev:
                            status = 'Published'
                        else:
                            status = 'Unpublished Changes'

                    if article.status in ['Draft', 'Unpublished Changes']:
                        drafts.append(article)
                    else:
                        published.append(article)

                v['articles'] = sorted(drafts, key=lambda article: article.last_updated, reverse=True) + sorted(published, key=lambda article: article.pub_date, reverse=True)

                render.page(self, '/templates/admin/console.html', values=v)



class edit(webapp2.RequestHandler):
    def get(self, mode=""):
        self.response.out.write('editor')


class config_handler(webapp2.RequestHandler):
    def get(self):
        v = {}
        render.page(self, '/templates/admin/config.html', v)
    def post(self):
        settings_dict = self.request.POST
        saved_settings = config.settings.get_by_key_name('SETTINGS', read_policy=db.STRONG_CONSISTENCY)
        if saved_settings == None:
            saved_settings = config.settings(key_name='SETTINGS')
        for s in settings_dict:
            setattr(saved_settings, s, str(settings_dict[s]))
        saved_settings.put()
        self.response.out.write('saved!')


class sync(webapp2.RequestHandler):
    def get(self):
        dropbox = dropbox_api()

        # Two folders from dropbox will be syced with datastore
        # this dict object enables abstraction for the syching mechanism later on
        sync_folders = {}
        sync_folders['articles'] = {'path':'/posts',
                                      'content_type':'text',
                                      'query': models.articles.all(),
                                      'model': models.articles}
        sync_folders['sidebar'] = {'path':'/pics/sidebar',
                                        'content_type':'pic',
                                        'query': models.pics.all().filter('collection =', 'sidebar').run(limit=2000),
                                        'model': models.pics}
        master_count = 0
        master_delete_count = 0
        for sync_folder in sync_folders:
            data = sync_folders[sync_folder]

            # query datastore
            # use memcached data by default to minimize datastore query calls
            version_control_object = tools.get_memcached_data(sync_folder, data['query'])

            # call dropbox api for info regarding folder contents
            folder_meta = dropbox.request_meta(data['path'])
            upload_count = 0
            for a in folder_meta['contents']:
                try:
                    dstore_rev = version_control_object[str(a['path'])]
                except:
                    dstore_rev = None
                dropbox_rev = a['rev']
                # compare current drobox for each item versus the currently in datastore
                # "rev" is the version control number, new 'rev' == new edit
                # conflict indicates new edits
                if dstore_rev <> dropbox_rev:
                    # queue item to be reuploaded to datastore
                    # the reupload process will overwrite obsolete data
                    taskqueue.add(url='/admin/sync', params={'path': str(a['path']), 'rev':a['rev'], 'modified':a['modified'], 'content_type':data['content_type'] })
                    upload_count += 1

                # remove checked items from memcache
                # once loop is complete only deleted or renamed files will remain
                if dstore_rev <> None:
                    version_control_object.pop(a['path'])

            # delete all items in datastore that no longer appear in dropbox
            deleted_count = 0
            for dead_file in version_control_object:
                dead_db_record = data['model'].get_by_key_name(dead_file)
                dead_db_record.delete()
                deleted_count += 1

            # delete obsolete cached data
            if upload_count > 0 or deleted_count > 0:
                memcache.delete(sync_folder)
                serialized_version_name = sync_folder + "_serialized"
                memcache.delete(serialized_version_name)
            # memcache will automatically be reset next go-round
            master_count += upload_count
            master_delete_count += deleted_count

        status_message = "added or updated: %i --- deleted: %i" % (master_count, master_delete_count)
        logging.info(status_message)
        render.page(self, '/templates/base.html', values={'dumb_content': status_message})


    def post(self):
        path = self.request.get('path')
        content_type = self.request.get('content_type')
        rev = self.request.get('rev')
        if content_type == 'text':
            modified = datetime.strptime(self.request.get('modified'), "%a, %d %b %Y %H:%M:%S +0000")
            if path <> "":
                upload(path, rev, modified)
        elif content_type == 'pic':
            upload_pic(path, rev, 'sidebar')
        self.response.out.write('good')

