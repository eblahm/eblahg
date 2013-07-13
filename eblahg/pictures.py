import webapp2
import models
import random
import hashlib
import render
import urllib
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache
from utility import dropbox_api
import re



class single(webapp2.RequestHandler):
    def get(self, key):
        pic = models.Picture.get_by_key_name(key).pic

        height = self.request.get('h')
        width = self.request.get('w')
        if height != "" and width != "":
            sbar_height = int(float(height))
            sbar_width = int(float(width))
            try:
                img = images.Image(pic)
                img.resize(height=sbar_height)
                if sbar_width < img.width:
                    width_ratio = sbar_width/float(img.width)
                    side_offset = (1 - width_ratio)/2.0
                else:
                    side_offset = 0
                if img.height > sbar_height:
                    height_ratio = sbar_height/float(img.height)
                    top_offset = (1 - height_ratio)/2.0
                else:
                    top_offset = 0
                img.crop(0.0+side_offset,
                         0.0+top_offset,
                         1.0-side_offset,
                         1.0-top_offset)
                img = img.execute_transforms(output_encoding=images.JPEG)
            except:
                img = pic
        elif self.request.get('size') == 'thumbnail':
            img = images.Image(pic)
            img.resize(width=100) #, height=180)
            img = img.execute_transforms(output_encoding=images.JPEG)
        else:
            img = pic

        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(img)

def upload_pic(path, rev, client=dropbox_api()):
    this_pic = client.request_file(path)
    this_pic = mb_limit(this_pic)
    try:
        title = re.search(r'([^\/]*)\..{,3}$', path).group(1)
    except:
        try:
            title = re.search(r'[^\/]*$').group(0)
        except:
            title = path
    new_picture = models.Picture(
        key_name=hashlib.md5(path).hexdigest(),
        path = str(path),
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

def random_pic_update(template_values):
    pic_keys = memcache.get('pic_keys')
    if pic_keys == None or pic_keys == []:
        query = models.Picture.all().filter('sidebar =', True)
        pic_keys = []
        for p in query:
            pic_keys.append(str(p.key().name()))
        memcache.set('pic_keys', pic_keys)
        pic_keys = memcache.get('pic_keys')

    if len(pic_keys) > 0:
        ran_num = random.randint(0, len(pic_keys)-1)
        template_values['random_picture_key'] = pic_keys[ran_num]
    return template_values
