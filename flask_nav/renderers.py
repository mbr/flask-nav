from flask import current_app

from visitor import Visitor


class SimpleRenderer(Visitor):
    def visit_object(self, node):
        if current_app.debug:
            return '<!-- no implementation in {} to render {} -->'.format(
                self.__class__.__name__, node.__class__.__name__,
            )
        return ''
