import jinja2
import config


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(config.APP_ROOT_DIR)
)

def load(template_file, values={}):
    template = jinja_env.get_template(template_file)
    return template.render(values)

def page(handler, template_file, values={}):

    values.update(config.settings)
    values.update({'social_links': load('/templates/resources/social_links.html', config.social_links)})
    values.update(config.social_links)
    template = jinja_env.get_template(template_file)
    handler.response.out.write(template.render(values))


def not_found(handler):
    page(handler, '/templates/404.html')
