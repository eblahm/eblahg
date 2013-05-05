import jinja2
import config


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(config.APP_ROOT_DIR)
)


def page(handler, template_file, values={}):
    settings_from_db = config.settings.get_by_key_name('SETTINGS')
    values.update({'settings': settings_from_db})
    values.update(config.social_links)
    template = jinja_env.get_template(template_file)
    handler.response.out.write(template.render(values))


def not_found(handler):
    page(handler, '/templates/404.html')
