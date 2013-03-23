from HTMLParser import HTMLParser
from google.appengine.api import memcache
__author__ = 'Matt'

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

def get_memcached_data(memcache_name, query, format="dict"):
    serialized_version_name = memcache_name + "_serialized"
    if format == 'serialized':
        version_control_object = memcache.get(serialized_version_name)
    else:
        version_control_object = memcache.get(memcache_name)

    if version_control_object == None:
        db_mirror = {}
        serialized = []
        for i in query:
            db_mirror[str(i.key().name())] = i.rev
            serialized.append(str(i.key()))
        memcache.set(memcache_name, db_mirror)
        memcache.set(serialized_version_name, serialized)

        if format == 'serialized':
            version_control_object = memcache.get(serialized_version_name)
        else:
            version_control_object = memcache.get(memcache_name)

    return version_control_object
