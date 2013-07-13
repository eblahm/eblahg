import webapp2
import models
import random
import render
import urllib
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache

def random_pic_update(template_values):
    pic_ids = memcache.get('pic_keys')
    if pic_ids == None:
        query = models.pics.all().filter('sidebar =', True)
        pic_keys = []
        for p in query:
            pic_keys.append(str(p.key()))
        memcache.set('pic_keys', pic_keys)
        pic_keys = memcache.get('pic_keys')

    ran_num = random.randint(0, len(pic_ids))
    try:
        template_values['random_picture_id'] = pic_ids[ran_num]
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
    def get(self, id):
        rec = models.pics.get_by_id(id)

        height = self.request.get('h')
        width = self.request.get('w')
        if height != "" and width != "":
            sbar_height = int(float(height))
            sbar_width = int(float(width))

            img = images.Image(rec.pic)
            img.resize(height=sbar_height)
            if img.width <= sbar_width:
                img = img.execute_transforms(output_encoding=images.JPEG)
            else:
                ratio = sbar_width/float(img.width)
                left = (1 - float(ratio)) / 2
                right = left + ratio
                if img.height > img.width:
                    left = left * 0.7
                    right = 1 - left
                img.crop(left, 0.0, right, 1.0)
                img = img.execute_transforms(output_encoding=images.JPEG)
        elif self.request.get('size') == 'thumbnail':
            img = images.Image(rec.pic)
            img.resize(width=100) #, height=180)
            img = img.execute_transforms(output_encoding=images.JPEG)
        else:
            img = rec.pic

        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(img)

