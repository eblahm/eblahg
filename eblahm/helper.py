import webapp2
from datetime import datetime
import urllib
import urllib2
from HTMLParser import HTMLParser
import xml.etree.ElementTree as etree
from eblahm import models


def accessdateconvert(access_date_string):
    #2005-01-13 07:56:00
    adate = datetime(int(access_date_string[0:4]), int(access_date_string[5:7]), int(access_date_string[8:10]), int(access_date_string[11:13]), int(access_date_string[14:16]), int(access_date_string[17:19]))
    return adate

def build_db(handler):
    # doc_index = search.Index(name='Post')
    # for document in doc_index.get_range(ids_only=True):
    #     doc_index.delete(document.doc_id)
    # for p in models.Post.all():
    #     p.delete()
    #
    #
    # for pic in models.pics.all():
    #     pic.delete()
    # x = data.pic_file_names.split("\n")
    # num=0
    # for fn in x:
    #     if fn == "":
    #         continue
    #     url = 'https://dl.dropbox.com/u/10718699/Leslie_Halbe_Photos/%s' % (urllib.quote(fn))
    #     req = urllib2.Request(url)
    #     response = urllib2.urlopen(req)
    #     pic_file = response
    #     # this_fn = '/Users/Matt/Dropbox/Public/Leslie_Halbe_Photos/%s' % (fn)
    #     # pic_file = open(this_fn, 'r')
    #     regex = re.search('L W Halbe collection - (.+)\.jpg', fn)
    #     try:
    #         title = regex.group(1)
    #     except:
    #         title = fn
    #     this_key_name = "lw%i" % (num)
    #     new = models.pics(key_name=this_key_name)
    #     new.pic = db.Blob(pic_file.read())
    #     new.title = title
    #     new.alt_url = url
    #     new.collection = "LW Halbe"
    #     new.put()
    #     num += 1
    #     if num > 15:
    #         break

    image_links = []
    ignore = ["http://photos1.blogger.com/pbp.gif", "http://photos1.blogger.com/pbh.gif" ]
    body_parsed = [""]
    current_tag = ["o"]
    link = [""]
    bundle = [""]
    class hp(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == "a":
                body_parsed[0] += bundle[0]
                bundle[0] = ""
                for a in attrs:
                    if a[0] == "href":
                        link[0] = "(%s) " % (a[1])
                current_tag[0] = "a"
            elif tag == 'blockquote':
                body_parsed[0] += bundle[0]
                bundle[0] = ""
            elif tag == 'p':
                current_tag[0] = "p"
            elif tag == "img":
                this_img = {"alt":None, "url":""}
                for a in attrs:
                    if a[0] == 'src':
                        this_img["url"] = a[1]
                    if a[0] == 'alt':
                        this_img["alt"] = a[1]
                if this_img["url"] not in ignore:
                    image_links.append(this_img)

        def handle_data(self, data):
            bundle[0] += data

        def handle_endtag(self, tag):
            if current_tag[0] == "a" and tag == "a":
                if bundle[0].strip() == "":
                    bundle[0] = "link"
                body_parsed[0] = body_parsed[0] + " [" + bundle[0] + "]" + link[0]
                link[0] = ""
                bundle[0] = ""
                current_tag[0] = "o"
            elif current_tag[0] == "blockquote" and tag == "blockquote":
                body_parsed[0] = "> " + bundle[0].replace('\n', "> ")
                bundle[0] = ""
            elif current_tag[0] == "li" and tag == "li":
                body_parsed[0] = "- " + bundle[0].replace('\n', "- ")
                bundle[0] = ""
                current_tag[0] = "o"
            elif current_tag[0] == "p" or current_tag[0] == "o" and tag == 'p':
                body_parsed[0] = body_parsed[0] + '\n \n' + bundle[0]
                bundle[0] = ""
                current_tag[0] = "o"


    url = 'https://dl.dropbox.com/u/10718699/theundergroundonuswordpress2012-11-17.xml'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    page = response.read()
    parsed = etree.fromstring(page)
    channel = parsed.find('channel')
    etree.register_namespace('wp', "http://wordpress.org/export/1.2/")
    items = channel.findall('item')

    x = 0
    for i in items:
        this_body = i.find('{http://purl.org/rss/1.0/modules/content/}encoded').text
        if this_body <> None:
            this_title = i.find('title').text
            if this_title <> None:
                pass
                # this_title = new_post.title.encode('ascii', 'ignore')
            else:
                this_title = "Untitled"

            try:
                this_date = rssdateconvert(i.find('pubDate').text)
            except:
                this_date = datetime.now()
            slug = i.find('{http://wordpress.org/export/1.2/}post_name').text
            if slug == "None" or slug == None or slug == "":
                slug = "Untitled%i" % (x)
            # try:
            #     this_body = str(this_body).encode('utf-8', 'ignore').decode('utf-8')
            # except:
            #     this_body = this_body.encode('utf-8', 'ignore').decode('utf-8')
            this_body = this_body.replace("<br />", "\n\n").replace('<br>', "\n")



            parser = hp()
            parser.feed(this_body)
            body_parsed[0] += bundle[0]
            this_body = body_parsed[0]

            post_pics = []
            if len(image_links) > 0:
                for img in image_links:
                    # new = models.pics()
                    url = img["url"]
                    req = urllib2.Request(url)
                    try:
                        response = urllib2.urlopen(req)
                    except:
                        continue
                    pic = response.read()
                    try:
                        pfn = '"'+str(img["alt"])+'"'
                    except:
                        pfn = '"'+img["alt"].encode('ascii', 'ignore')+'"'
                    if pfn.replace('"', "").strip() == "" or pfn.replace('"', "") == 'None':
                        pfn = '"untitled%i"' % (x)
                        x += 1
                    pic_fpath = '/Users/Matt/Dropbox/eblahm/pics/%s.jpg' % (pfn.replace('"', ""))
                    pic_file = file(pic_fpath, 'w')
                    pic_file.write(pic)
                    post_pics.append(pfn)

            fpath = '/Users/Matt/Dropbox/eblahm/posts/%s.md' % (this_title)
            this_file = file(fpath, 'w')
            meta = "title: %s\nslug: %s\ndate: %s\n" % (this_title, slug, this_date.strftime('%m-%d-%Y %I:%M%p').lower())
            if len(post_pics) > 0:
                meta += 'pics: %s\n' % (", ".join(post_pics))
            this_body = meta + this_body
            try:
                this_file.write(this_body)
            except:
                this_body = this_body.encode('ascii', 'ignore')
                this_file.write(this_body)
            this_file.close()

                    # new.pic = db.Blob(pic_file.read())
                    # new.alt_url = img["url"]
                    # new.parent = new_post

                    # new.collection = "old_blogs"
                    # try:
                    #     new.put()
                    # except:
                    #     pass


            #			attch = i.find('{http://wordpress.org/export/1.2/}attachment_url'
            # new_post.tags = []


            # new_post.put()
            image_links = []
            body_parsed = [""]
            current_tag = ["o"]
            link = [""]
            bundle = [""]
            x += 1
    return 'good'
        #        found_comments = i.findall('{http://wordpress.org/export/1.2/}comment')
        #			if found_comments <> None:
        #				for c in list(found_comments):
        #					cdata = {}
        #					new_comment = models.comments()
        #					new_comment.ref = new
        #					new_comment.author = c.find('{http://wordpress.org/export/1.2/}comment_author').text
        #					new_comment.date = accessdateconvert(c.find('{http://wordpress.org/export/1.2/}comment_date').text)
        #					new_comment.email = c.find('{http://wordpress.org/export/1.2/}comment_author_email').text
        #					new_comment.comment = c.find('{http://wordpress.org/export/1.2/}comment_content').text
        #					new_comment.put()

def build_yonant(handler):
    image_links = []
    ignore = ["http://photos1.blogger.com/pbp.gif", "http://photos1.blogger.com/pbh.gif" ]
    body_parsed = [""]
    current_tag = ["o"]
    link = [""]
    bundle = [""]

    class yonant_parser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == "a":
                body_parsed[0] += bundle[0]
                bundle[0] = ""
                for a in attrs:
                    if a[0] == "href":
                        link[0] = "(%s) " % (a[1])
                current_tag[0] = "a"
            elif tag == 'blockquote':
                body_parsed[0] += bundle[0]
                bundle[0] = ""
            elif tag == 'p':
                current_tag[0] = "p"
            elif tag == "img":
                this_img = {"alt":None, "url":""}
                for a in attrs:
                    if a[0] == 'src':
                        this_img["url"] = a[1]
                    if a[0] == 'alt':
                        this_img["alt"] = a[1]
                if this_img["url"] not in ignore:
                    image_links.append(this_img)

        def handle_data(self, data):
            bundle[0] += data

        def handle_endtag(self, tag):
            if current_tag[0] == "a" and tag == "a":
                if bundle[0].strip() == "":
                    bundle[0] = "link"
                body_parsed[0] = body_parsed[0] + " [" + bundle[0].strip() + "]" + link[0]
                link[0] = ""
                bundle[0] = ""
                current_tag[0] = "o"
            elif current_tag[0] == "blockquote" and tag == "blockquote":
                body_parsed[0] = ">" + bundle[0].replace('\n', ">")
                bundle[0] = ""
            elif current_tag[0] == "li" and tag == "li":
                body_parsed[0] = "-" + bundle[0].replace('\n', "-")
                bundle[0] = ""
                current_tag[0] = "o"
            # elif current_tag[0] == 'img':
            #     body_parsed[0] += ' <img src="%s" alt="%s" /> ' % (image_links[0]['url'], image_links[0]['alt'])
            #     current_tag[0] = "o"
            #     image_links[0] = ""
            elif current_tag[0] == "p" or current_tag[0] == "o" and tag == 'p':
                body_parsed[0] = body_parsed[0] + '\n\n' + bundle[0].strip()
                bundle[0] = ""
                current_tag[0] = "o"

    url = 'https://dl.dropbox.com/u/10718699/yonant.xml'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    yonant_data_file = response.read()
    root = etree.fromstring(yonant_data_file)
    # root = yonant_data_parsed.getroot()
    sections = root.find('sections').findall('section')
    def my_decode(etree_element):
        if etree_element == None:
            return etree_element
        else:
            try:
                encoding = etree_element.attrib['encoding']
                text = etree_element.text.decode(encoding)
            except:
                text = etree_element.text
            return text
    x = 0
    for s in sections:
        m = s.find('modules').findall('module')
        c = m[0].find('content')
        if c <> None:
            for post in c.findall('journal-entry'):
                # new_post = models.Post()
                this_title = my_decode(post.find('title'))
                this_body = my_decode(post.find('body'))
                if this_body <> None:
                    parser = yonant_parser()
                    parser.feed(this_body)
                    body_parsed[0] += bundle[0]
                    this_body = body_parsed[0]
                    # <added-on>2010-09-03 01:22:30.0</added-on>
                    d = post.find('added-on').text.split(' ')[0].split('-')
                    h = post.find('added-on').text.split(' ')[1].split(':')
                    this_date = datetime(int(d[0]), int(d[1]),int(d[2]), int(h[0]), int(h[1]), 0)
                    if this_title <> None:
                        slug = urllib.quote(this_title.replace(" ", "_"))
                    else:
                        this_title = "untitled%i" % (x)
                        slug = "untitled%i" % (x)

                    post_pics = []
                    if len(image_links) > 0:
                        for img in image_links:
                            # new = models.pics()
                            url = 'http://yonant.squarespace.com' + img["url"]
                            req = urllib2.Request(url)
                            response = urllib2.urlopen(req)
                            pic = response.read()
                            try:
                                pfn = '"'+str(img["alt"])+'"'
                            except:
                                pfn = '"'+img["alt"].encode('ascii', 'ignore')+'"'
                            if pfn.replace('"', "").strip() == '' or pfn.replace('"', "") == 'None':
                                pfn = '"untitled%i"' % (x)
                                x += 1
                            pic_fpath = '/Users/Matt/Dropbox/eblahm/pics/%s.jpg' % (pfn.replace('"', ""))
                            pic_file = file(pic_fpath, 'w')
                            pic_file.write(pic)
                            post_pics.append(pfn)

                    fpath = '/Users/Matt/Dropbox/eblahm/posts/%s.md' % (this_title)
                    this_file = file(fpath, 'w')
                    meta = "title: %s\nslug: %s\ndate: %s\n" % (this_title, slug, this_date.strftime('%m-%d-%Y %I:%M%p').lower())
                    if len(post_pics) > 0:
                        meta += 'pics: %s\n' % (", ".join(post_pics))
                    this_body = meta + this_body
                    try:
                        this_file.write(this_body)
                    except:
                        this_body = this_body.encode('ascii', 'ignore')
                        this_file.write(this_body)
                    this_file.close()

                image_links = []
                body_parsed = [""]
                current_tag = ["o"]
                link = [""]
                bundle = [""]
                x += 1
    return 'good'

def count_words(handler):
    x = 0
    for i in models.Post.all():
        i.put()
        x += 1
    handler.response.out.write(x)

