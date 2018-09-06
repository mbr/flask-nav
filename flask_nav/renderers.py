from flask import current_app

from dominate import tags
from dominate.util import raw
from hashlib import sha1
from visitor import Visitor


class Renderer(Visitor):
    """Base interface for navigation renderers.

    Visiting a node should return a string or an object that converts to a
    string containing HTML."""

    def visit_object(self, node):
        """Fallback rendering for objects.

        If the current application is in debug-mode
        (``flask.current_app.debug`` is ``True``), an ``<!-- HTML comment
        -->`` will be rendered, indicating which class is missing a visitation
        function.

        Outside of debug-mode, returns an empty string.
        """
        if current_app.debug:
            return tags.comment('no implementation in {} to render {}'.format(
                self.__class__.__name__,
                node.__class__.__name__, ))
        return ''


class SimpleRenderer(Renderer):
    """A very basic HTML5 renderer.

    Renders a navigational structure using ``<nav>`` and ``<ul>`` tags that
    can be styled using modern CSS.

    :param kwargs: Additional attributes to pass on to the root ``<nav>``-tag.
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def visit_Link(self, node):
        return tags.a(node.text, href=node.get_url())

    def visit_Navbar(self, node):
        kwargs = {'_class': 'navbar'}
        kwargs.update(self.kwargs)

        cont = tags.nav(**kwargs)
        ul = cont.add(tags.ul())

        for item in node.items:
            ul.add(tags.li(self.visit(item)))

        return cont

    def visit_View(self, node):
        kwargs = {}
        if node.active:
            kwargs['_class'] = 'active'
        return tags.a(node.text,
                      href=node.get_url(),
                      title=node.text,
                      **kwargs)

    def visit_Subgroup(self, node):
        group = tags.ul(_class='subgroup')
        title = tags.span(node.title)

        if node.active:
            title.attributes['class'] = 'active'

        for item in node.items:
            group.add(tags.li(self.visit(item)))

        return tags.div(title, group)

    def visit_Separator(self, node):
        return tags.hr(_class='separator')

    def visit_Text(self, node):
        return tags.span(node.text, _class='nav-label')

    def visit_RawTag(self, node):
        return raw(node.content)


class BootstrapExtRenderer(Renderer):
    def __init__(self, html5=True, id=None):
        self.html5 = html5
        self._in_dropdown = False
        self.id = id

    def visit_Navbar(self, node):
        # create a navbar id that is somewhat fixed, but do not leak any
        # information about memory contents to the outside
        node_id = self.id or sha1(str(id(node)).encode()).hexdigest()

        root = tags.nav() if self.html5 else tags.div(role='navigation')
        root_class = 'navbar navbar-inverse' if node.navbar_inverse else 'navbar navbar-default'
        if node.navbar_fixed == 'top':
            root_class += ' navbar-fixed-top'
        elif node.navbar_fixed == 'bottom':
            root_class += ' navbar-fixed-bottom'
        root['class'] = root_class

        cont = root.add(tags.div(_class='container-fluid'))

        # collapse button
        header = cont.add(tags.div(_class='navbar-header'))
        btn = header.add(tags.button())
        btn['type'] = 'button'
        btn['class'] = 'navbar-toggle collapsed'
        btn['data-toggle'] = 'collapse'
        btn['data-target'] = '#' + node_id
        btn['aria-expanded'] = 'false'
        btn['aria-controls'] = 'navbar'

        btn.add(tags.span('Toggle navigation', _class='sr-only'))
        btn.add(tags.span(_class='icon-bar'))
        btn.add(tags.span(_class='icon-bar'))
        btn.add(tags.span(_class='icon-bar'))

        # add a custom _class `navbar-logo` to adjust logo image
        if node.logo_filename is not None:
            logo_a = tags.a(_class='navbar-left navbar-logo')
            logo_a.add(tags.img(src=node.get_logo_file_url()))
            header.add(logo_a)

        # title may also have a 'get_url()' method, in which case we render
        # a brand-link
        if node.title is not None:
            if hasattr(node.title, 'get_url'):
                header.add(tags.a(node.title.text, _class='navbar-brand',
                                  href=node.title.get_url()))
            else:
                header.add(tags.span(node.title, _class='navbar-brand'))

        bar = cont.add(tags.div(
            _class='navbar-collapse collapse',
            id=node_id,
        ))

        for item in node.items:
            bar.add(self.visit(item))

        return root

    def visit_Nav(self, node):
        ul = tags.ul()
        ul['class'] = 'nav navbar-nav navbar-right' if node.navbar_right else 'nav navbar-nav'
        for item in node.items:
            ul.add(self.visit(item))
        return ul

    def visit_Text(self, node):
        if not self._in_dropdown:
            return tags.p(node.text, _class='navbar-text')
        return tags.li(node.text, _class='dropdown-header')

    def visit_Link(self, node):
        a = tags.a(href=node.get_url())
        if node.icon is not None:
            a.add(tags.i(_class=str(node.icon)))
            a.add(tags.span(node.text))
        else:
            a.add_raw_string(node.text)
        li = tags.li()
        li.add(a)

        return li

    def visit_Separator(self, node):
        if not self._in_dropdown:
            raise RuntimeError('Cannot render separator outside Subgroup.')
        return tags.li(role='separator', _class='divider')

    def visit_Subgroup(self, node):
        if not self._in_dropdown:
            li = tags.li(_class='dropdown')
            if node.active:
                li['class'] = 'active'
            a = li.add(tags.a(href='#', _class='dropdown-toggle'))
            if node.icon is not None:
                a.add(tags.i(_class=str(node.icon)))
                a.add(tags.span(node.title))
            else:
                a.add_raw_string(node.title)
            a['data-toggle'] = 'dropdown'
            a['role'] = 'button'
            a['aria-haspopup'] = 'true'
            a['aria-expanded'] = 'false'
            a.add(tags.span(_class='caret'))

            ul = li.add(tags.ul(_class='dropdown-menu'))

            self._in_dropdown = True
            for item in node.items:
                ul.add(self.visit(item))
            self._in_dropdown = False

            return li
        else:
            raise RuntimeError('Cannot render nested Subgroups')

    def visit_View(self, node):
        a = tags.a(href=node.get_url(), title=node.text)
        if node.icon is not None:
            a.add(tags.i(_class=str(node.icon)))
            a.add(tags.span(node.text))
        else:
            a.add_raw_string(node.text)

        item = tags.li()
        item.add(a)
        if node.active:
            item['class'] = 'active'

        return item

    def visit_RawTag(self, node):
        return raw(node.content)

    def visit_Search(self, node):
        form = tags.form(target="_blank", method="get", role="search")
        form['role'] = 'search'
        form['class'] = 'navbar-form navbar-right' if node.navbar_right else 'navbar-form navbar-left'

        # action may also have a 'get_url()' method, in which case we render
        if node.action is not None:
            if hasattr(node.action, 'get_url'):
                form['action'] = node.action.get_url()
            else:
                form['action'] = node.action

        div = form.add(tags.div(_class='form-group'))
        search_input = div.add(tags.input(type="text", _class="form-control", placeholder=node.input_placeholder))
        if node.input_id is not None:
            search_input['id'] = node.input_id
        if node.input_name is not None:
            search_input['name'] = node.input_name

        btn = form.add(tags.button(type="submit", _class="btn btn-default"))
        if node.icon is not None:
            btn.add(tags.i(_class=str(node.icon)))

        if node.btn_text is not None:
            btn.add(tags.span(node.btn_text))

        return form
