from visitor import Visitor
from .ext import Nav


@Nav.renderer
class SimpleRenderer(Visitor):
    pass  # TODO: Implement
