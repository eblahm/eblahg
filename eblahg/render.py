import jinja2
import config
from google.appengine.ext import db

__author__ = 'Matt'

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(config.APP_ROOT_DIR))


def page(handler, template_file, values={}):
    values.update({'settings': config.settings.get_by_key_name('SETTINGS', read_policy=db.STRONG_CONSISTENCY)})
    template = jinja_environment.get_template(template_file)
    handler.response.out.write(template.render(values))


def not_found(handler):
    page(handler, '/templates/404.html')