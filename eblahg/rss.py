import webapp2
import fix_path
fix_path.fix()
import models
from config import settings
import PyRSS2Gen
import datetime
from google.appengine.ext import db


class main(webapp2.RequestHandler):

    def get(self):
        query = models.articles.all()
        query.order('-pub_date')
        posts = query.fetch(10)

        rss_items = []
        for post in posts:
            this_link = self.request.host_url + "/posts/" + post.slug
            item = PyRSS2Gen.RSSItem(
                title=post.title,
                link=this_link,
                description=post.body_html,
                guid="",
                pubDate=post.pub_date
            )
            rss_items.append(item)

        rss = PyRSS2Gen.RSS2(
            title=settings.blog_title,
            link=settings.url,
            description="a blog by Matt Halbe",
            lastBuildDate=datetime.datetime.now(),
            items=rss_items
        )
        rss_xml = rss.to_xml()
        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.out.write(rss_xml)
