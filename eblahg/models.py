from fix_path import fix
import datetime
import re

from google.appengine.ext import db
from google.appengine.api import search
from google.appengine.api import memcache
fix()
import markdown
import logging


def slugify(value):
    """
    Adapted from Django's django.template.defaultfilters.slugify.
    """
    import unicodedata
    value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

class articles(db.Model):
    title = db.StringProperty()
    body = db.TextProperty()
    body_html = db.TextProperty()
    slug = db.StringProperty()
    pub_date = db.DateTimeProperty(auto_now_add=True)
    author = db.UserProperty(auto_current_user_add=True)

    tags = db.StringListProperty()
    word_count = db.IntegerProperty()
    last_updated = db.DateTimeProperty()
    rev = db.StringProperty()
    path = db.StringProperty()

    def put(self):
        self.word_count = len([w for w in self.body.replace('\n', "").split(" ") if w.strip() <> ""])

        if self.slug == None:
            self.slug = slugify(self.title)
        self.test_for_slug_collision()
        self.populate_html_fields()

        key = super(articles, self).put()
        text_write = create_doc(self)
        return key
    def delete(self):
        search.Index(name='articles').delete(str(self.key()))
        key = super(articles, self).delete()
        return key

    def test_for_slug_collision(self):
        # Build the time span to check for slug uniqueness

        # Create a query to check for slug uniqueness in the specified time span
        query = articles.all(keys_only=True).filter('slug = ', self.slug)
        query_count = query.count()

        if query_count > 0:
            if query_count == 1 and not self.is_saved():
                if self.is_saved():
                    if self.key() == query.get().key():
                        pass
                    else:
                        logging.error('Slug not unique!')
                        assert False

    def populate_html_fields(self):
        # Setup Markdown with the code highlighter
        md = markdown.Markdown(extensions=['codehilite', 'footnotes'])
        if self.body != None:
            self.body_html = md.convert(self.body)


class pics(db.Model):
    title = db.StringProperty()
    path = db.StringProperty()
    rev = db.StringProperty()
    pic = db.BlobProperty()
    sidebar = db.BooleanProperty()


def create_doc(rec):
    def normalize(field):
        if field <> None:
            return field.encode('ascii', 'ignore')
        else:
            return field
    if rec.tags <> None:
        tags = normalize(", ".join(rec.tags))
    else:
        tags = None
    new_doc = search.Document(doc_id=str(rec.key()),
        fields=[search.TextField(name='title', value=normalize(rec.title)),
                search.TextField(name='body', value=normalize(rec.body)),
                search.TextField(name='tags', value=tags),
                search.DateField(name='date', value=rec.pub_date.date()),])
    search.Index(name="articles").put(new_doc)
    return 'good'


