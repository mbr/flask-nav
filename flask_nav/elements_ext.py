#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    elements_ext
    -----------------------------
    Override navigation items class in flask_nav.elements
"""
from flask_nav.elements import NavigationItem
from flask import url_for, request


class Link(NavigationItem):
    """An item that contains a link to a destination and a title.

    :param text: The text inside the tag.
    :param dest: The `a` tag href attribute.
    :param icon: The font-awesome class.
    """

    def __init__(self, text, dest, icon=None):
        self.text = text
        self.dest = dest
        self.icon = icon

    def get_url(self):
        return self.dest


class RawTag(NavigationItem):
    """An item usually expressed by a single HTML tag.

    :param title: The text inside the tag.
    :param attribs: Attributes on the item.
    """

    def __init__(self, content, **attribs):
        self.content = content
        self.attribs = attribs


class View(Link):
    """Application-internal link.

    The ``endpoint``, ``*args`` and ``**kwargs`` are passed on to
    :func:`~flask.url_for` to get the link.

    :param text: The text for the link.
    :param endpoint: The name of the view.
    :param icon: The font-awesome class.
    :param kwargs: Extra keyword arguments for :func:`~flask.url_for`
    """

    #: Whether or not to consider query arguments (``?foo=bar&baz=1``) when
    #: determining whether or not a ``View`` is active.

    #: By default, query arguments are ignored."""
    ignore_query = True

    def __init__(self, text, endpoint, **kwargs):
        self.text = text
        self.endpoint = endpoint
        self.icon = kwargs.pop('icon', None)
        self.url_for_kwargs = kwargs

    def get_url(self):
        """Return url for this item.

        :return: A string with a link.
        """
        return url_for(self.endpoint, **self.url_for_kwargs)

    @property
    def active(self):
        if not request.endpoint == self.endpoint:
            return False

        # rebuild the url and compare results. we can't rely on using get_url()
        # because whether or not an external url is created depends on factors
        # outside our control

        _, url = request.url_rule.build(self.url_for_kwargs,
                                        append_unknown=not self.ignore_query)

        if self.ignore_query:
            return url == request.path

        # take query string into account.
        # FIXME: ensure that the order of query parameters is consistent
        return url == request.full_path


class Separator(NavigationItem):
    """Separator.

    A seperator inside the main navigational menu or a Subgroup. Not all
    renderers render these (or sometimes only inside Subgroups).
    """
    pass


class Subgroup(NavigationItem):
    """Nested substructure.

    Usually used to express a submenu.

    :param title: The title to display (i.e. when using dropdown-menus, this
                  text will be on the button).
    :param items: Any number of :class:`.NavigationItem` instances  that
                  make up the navigation element.
    :param icon: The font-awesome class.
    """

    def __init__(self, title, *items, icon=None):
        self.title = title
        self.icon = icon
        self.items = list(items)

    @property
    def active(self):
        return any(item.active for item in self.items)


class Text(NavigationItem):
    """Label text.

    Not a ``<label>`` text, but a text label nonetheless. Precise
    representation is up to the renderer, but most likely something like
    ``<span>``, ``<div>`` or similar.
    """

    def __init__(self, text):
        self.text = text


class Navbar(Subgroup):
    """Top level navbar.

    :param title: The navbar-brand to display.
    :param static_endpoint: Name of static endpoint.
    :param logo_filename: Name of logo image in static folder.
    :param navbar_inverse: Use :css_class:`navbar-inverse` instead of :css_class:`navbar-default` if `True`.
    :param navbar_fixed: Set navbar fixed or not.
                        see 'top':'navbar-fixed-top', 'bottom':'navbar-fixed-bottom', else: 'default'.
    :param items: Any number of :class:`.NavigationItem` instances  that
                  make up the navigation element.
    """

    def __init__(self, title, *items, static_endpoint='static', logo_filename=None, navbar_inverse=False,
                 navbar_fixed=None):
        self.title = title
        self.static_endpoint = static_endpoint
        self.logo_filename = logo_filename
        self.navbar_inverse = navbar_inverse
        self.navbar_fixed = navbar_fixed
        self.items = list(items)

    def get_logo_file_url(self):
        """Return url for logo image.

        :return: A string with a img link.
        """
        return url_for(self.static_endpoint, filename=self.logo_filename)


class Nav(NavigationItem):
    """Navbar nav.

    Usually used to express a `ul`tag with `li`s. See :css_class:`navbar-nav`

    :param navbar_right: set navbar display on right or left. Set `False` on left, `True` on right.
    :param items: Any number of :class:`.NavigationItem` instances  that
                  make up the navigation element.
    """

    def __init__(self, *items, navbar_right=False):
        self.navbar_right = navbar_right
        self.items = list(items)


class Search(NavigationItem):
    """Navbar search form.

    Usually used to express a simple search `form`tag.
    :param action: The form `action` attribute.
    :param icon: The font-awesome class.
    :param btn_text: The search button text to display.
    :param input_placeholder: The form>div>input `placeholder` attribute.
    :param input_name: The form>div>input `name` attribute.
    :param input_id: The form>div>input `id` attribute.
    :param navbar_right: set navbar display on right or left. Set `False` on left, `True` on right.
    """

    def __init__(self, action, icon=None, btn_text=None, input_placeholder='Search', input_name=None, input_id=None,
                 navbar_right=False):
        self.action = action
        self.icon = icon
        self.btn_text = btn_text
        self.input_placeholder = input_placeholder
        self.input_name = input_name
        self.input_id = input_id
        self.navbar_right = navbar_right
