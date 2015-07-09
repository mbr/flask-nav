from flask import url_for, request, current_app
from markupsafe import Markup

from . import get_renderer


class NavigationItem(object):
    active = False

    def render(self, renderer=None, **kwargs):
        return Markup(
            get_renderer(current_app, renderer)(**kwargs).visit(self)
        )


class TagItem(NavigationItem):
    def __init__(self, title, **attribs):
        self.title = title
        self.attribs = attribs


class View(NavigationItem):
    def __init__(self, title, endpoint, *args, **kwargs):
        self.title = title
        self.endpoint = endpoint
        self.url_for_args = args
        self.url_for_kwargs = kwargs

    def get_url(self):
        return url_for(self.endpoint,
                       *self.url_for_args,
                       **self.url_for_kwargs)

    @property
    def active(self):
        # this is a better check than checking for request.endpoint
        # because it takes arguments to the view into account
        return request.path == self.get_url()


class Separator(NavigationItem):
    pass


class Subgroup(NavigationItem):
    def __init__(self, title, *items):
        self.title = title
        self.items = items

    @property
    def active(self):
        return any(item.active for item in self.items)


class Label(TagItem):
    pass


class Link(TagItem):
    pass


class Navbar(Subgroup):
    pass
