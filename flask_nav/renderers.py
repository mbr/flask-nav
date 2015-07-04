from flask import current_app

from dominate import tags
from visitor import Visitor


class BaseRenderer(Visitor):
    def visit_object(self, node):
        if current_app.debug:
            return '<!-- no implementation in {} to render {} -->'.format(
                self.__class__.__name__, node.__class__.__name__,
            )
        return ''


class SimpleRenderer(BaseRenderer):
    def visit_Link(self, node):
        return tags.a(node.title, title=node.title, **node.attribs)

    def visit_Navbar(self, node):
        cont = tags.nav(_class='navbar')

        for item in node.items:
            cont.add(tags.li(self.visit(item)))

        return cont

    def visit_View(self, node):
        kwargs = {}
        if node.active:
            kwargs['_class'] = 'active'
        return tags.a(node.title,
                      href=node.get_url(),
                      title=node.title,
                      **kwargs)

    def visit_Subgroup(self, node):
        group = tags.ul()

        for item in node.items:
            group.add(tags.li(self.visit(item)))

        return group

    def visit_Separator(self, node):
        return tags.span(_class='separator')

    def visit_Label(self, node):
        return tags.span(node.title, _class='nav-label')
