import webapp2
import models
import random
import render
import urllib
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache

def random_pic_update(template_values):
    folder_serialized = memcache.get('sidebar_folder_serialized')
    if folder_serialized == None:
        query = models.pics.all().filter('collection =', 'sidebar').run(limit=2000)
        fs = []
        for p in query:
            fs.append(str(p.key()))
        memcache.set('sidebar_folder_serialized', fs)
        folder_serialized = memcache.get('sidebar_folder_serialized')
    limit = len(folder_serialized) - 1
    if limit >= 1:
        ran_num = random.randint(0, limit)
        random_pic = db.get(folder_serialized[ran_num])
    else:
        random_pic = models.pics.all().filter('collection =', 'sidebar').get()
    try:
        template_values['random_picture_key'] = str(random_pic.key())
        template_values['random_picture_path'] = urllib.quote(random_pic.key().name())
    except:
        pass
    return template_values



class sbar(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'image/jpeg'
        dbk = self.request.get('k')
        pic = db.get(dbk).pic
        sbar_height = int(float(str(self.request.get('h'))))
        sbar_width = int(float(str(self.request.get('w'))))

        try:
            img = images.Image(pic)
            img.resize(height=sbar_height)
            if img.width <= sbar_width:
                final_pic = img.execute_transforms(output_encoding=images.JPEG)
            else:
                ratio = sbar_width/float(img.width)
                left = (1 - float(ratio)) / 2
                right = left + ratio
                if img.height > img.width:
                    left = left * 0.7
                    right = 1 - left
                img.crop(left, 0.0, right, 1.0)
                final_pic = img.execute_transforms(output_encoding=images.JPEG)
        except:
            final_pic = pic

        self.response.out.write(final_pic)


class single(webapp2.RequestHandler):
    def get(self):
        size = self.request.get('size')
        rec = db.get(self.request.get('k'))
        if size == 'thumbnail':
            img = images.Image(rec.pic)
            img.resize(width=100) #, height=180)
            img = img.execute_transforms(output_encoding=images.JPEG)
        else:
            img = rec.pic
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(img)

