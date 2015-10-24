Advanced topics
===============

Renderers
---------

Elements from the :mod:`flask_nav.elements` module do not have any methods for
conversion to HTML code; this functionality is placed in
:class:`.Renderer` classes. These implement the visitor_
pattern and allow specifying a multitude of ways of converting your
navigational structure into HTML.

Whenever :meth:`flask_nav.elements.NavigationItem.render` is called, it just
looks up the desired renderer and calls the ``visit`` method of the renderer on
itself. The result is returned as a markupsafe string.


Implementing custom renderers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As an example, we are going to create a new renderer that uses nothing but
``<div>`` tags [1]_. Flask-
Nav uses the dominate_ library to create HTML output which we also use here:

.. code-block:: python

    from dominate import tags
    from flask_nav.renderers import Renderer

    class JustDivRenderer(Renderer):
        def visit_Navbar(self, node):
            sub = []
            for item in node.items:
                sub.append(self.visit(item))

            return tags.div('Navigation:', *sub)

        def visit_View(self, node):
            return tags.div('{} ({})'.format(node.title, node.get_url()))

        def visit_Subgroup(self, node):
            # almost the same as visit_Navbar, but written a bit more concise
            return tags.div(node.title,
                            *[self.visit(item) for item in node.items])


Now that we have our renderer, we need to register it on the app. This can be
done inside your ``create_app`` function (or elsewhere), by calling register

.. code-block:: python

    from flask_nav import register_renderer

    def create_app():
        # [...]

        register_renderer(app, 'just_div', JustDivRenderer)
        return app

Now we can use it inside the template:


.. code-block:: jinja

    {{nav.top.render(renderer='just_div')}}


If you are defining your custom renderers close to where the extension instance
lives, instead of ``register_renderer``, the :meth:`~.Nav.renderer`-decorator
can be used:

.. code-block:: python

    @nav.renderer()
    class JustDivRenderer(Renderer):
        pass  # ...

    # upon registration, 'just_div_renderer' will be a registered



Elements
--------

Any navigational structure is composed out of items. Thanks to the visitor
pattern, these can be of any class, but it is worthwhile to make all descend
from :class:`.NavigationItem`.

Typically, :class:`.Navbar` is the top level object of a navigational bar, but
that is not a requirement. Furthermore, if the renderer supports it, any part
of a navigational structure can be rendered on its own, be it a lone link or
full submenu.


Custom elements
~~~~~~~~~~~~~~~

Sometimes you may need to implement your own Element classes. This is easily
done by subclassing either :class:`.NavigationItem` or a more concrete class
(``get_auth_user`` is a placeholder here for any way your favorite
authentication framework returns the current user):


.. code-block:: python

    class UserGreeting(Text):
        def __init__(self):
            pass

        @property
        def text(self):
            return 'Hello, {}'.format('bob')


Note that when subclassing :class:`.NavigationItem`, renderers will most likely
not have a default rendering method. By subclassing :class:`.Text` in the
example, existing methods on renderers for the text class can be used, as
visitors will go up the full inheritance chain when a visitor for the current
class cannot be found.


Dynamic construction
--------------------

In the `Custom elements` section, a bit of dynamic behavior is already seen:
The greeting changes depending on who's logged in. This does not alter the
structure of the bar though, there is always a ``UserGreeting`` object inside
the structure.

To create dynamic instance of navbars, simply pass a :func:`callable` object
like a function to :meth:`.register_element`:

.. code-block:: python

    def top_nav():
        return Navbar(...)

    nav.register_element('top_nav', top_nav)

This is a common pattern, for this reason the :meth:`.navigation`-decorator is
available:

.. code-block:: python

    @nav.navigation
    def top_nav():
        # ...

The ``top_nav()`` function will be called every time a navbar must be rendered.
At this point, a user should have already logged, making it possible for
example to present him with menu items only available to registered users.

This mechanism can also be used to lazily instantiate navbars, if they are
expensive to setup but rarely used. It is also possible to preinstantiate
non-dynamic parts and just compose these with dynamic instances.

.. _visitor: https://en.wikipedia.org/wiki/Visitor_pattern
.. _dominate: https://github.com/Knio/dominate/
.. [1] Which is probably not a good idea, but a valid example.
