from .renderers import SimpleRenderer


def register_renderer(app, id, renderer, force=True):
    renderers = app.extensions.setdefault('nav_renderers', {})

    if force:
        renderers[id] = renderer
    else:
        renderers.setdefault(id, renderer)


def get_renderer(app, id):
    return app.extensions.get('nav_renderers', {})[id]


class Nav(object):
    renderers = {}

    def __init__(self, app=None):
        self.elems = {}
        self.renderers = {}

        if app:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['nav'] = self
        app.add_template_global(self.elems, 'nav')

        # register some renderers that ship with flask-nav
        register_renderer(app, 'simple', SimpleRenderer)
        register_renderer(app, None, SimpleRenderer, force=False)

    def register_element(self, id, elem):
        self.elems[id] = elem

    @classmethod
    def renderer(cls, id):
        def wrapper(renderer_class):
            cls.renderers[id] = renderer_class
            return renderer_class

        return wrapper
