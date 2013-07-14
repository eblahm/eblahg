from fix_path import fix
import re

from google.appengine.ext import db
from google.appengine.api import search

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

class Article(db.Model):
    title = db.StringProperty()
    body = db.TextProperty()
    body_html = db.TextProperty()
    slug = db.StringProperty()
    word_count = db.IntegerProperty()
    pub_date = db.DateTimeProperty()

    def put(self):
        if self.body != None:
            self.word_count = len([w for w in self.body.replace('\n', "").split(" ") if w.strip() <> ""])
        else:
            self.word_count = 0
        self.slug = slugify(self.title)
        self.test_for_slug_collision()
        key = super(Article, self).put()
        text_write = create_doc(self)
        return key

    def delete(self):
        search.Index(name='articles').delete(str(self.key()))
        key = super(Article, self).delete()
        return key

    def test_for_slug_collision(self):
        query = Article.all(keys_only=True).filter('slug = ', self.slug)
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


class Picture(db.Model):
    title = db.StringProperty()
    path = db.StringProperty()
    rev = db.StringProperty()
    pic = db.BlobProperty()
    sidebar = db.BooleanProperty()


def create_doc(rec):
    def normalize(field):
        if isinstance(field, unicode):
            return field.encode('ascii', 'ignore')
        else:
            return str(field)

    new_doc = search.Document(doc_id=str(rec.key()),
        fields=[search.TextField(name='title', value=normalize(rec.title)),
                search.TextField(name='body', value=normalize(rec.body)),
                search.DateField(name='date', value=rec.pub_date.date()),])
    search.Index(name="articles").put(new_doc)
    return 'good'


