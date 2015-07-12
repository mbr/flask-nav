Getting started
===============

To create a navigational element with Flask-Nav, it must first be created and
registered on the application. Usually, your navigation should be a
:class:`.Navbar` instance:

.. code-block:: python

    from flask_nav.elements import Navbar, View

    topbar = Navbar('',
        View('Home', 'frontend.index'),
        View('Your Account', 'frontend.account_info'),
    )

Items are added by simply passing them to the :class:`.Navbar`-constructor.
This is purely convenience, instead it is possible to append to the ``items``
attribute of ``topbar`` as well. Each :class:`.View` instance gets a piece of
text to display as the first parameter, everything afterwards is passed on
straight to :func:`~flask.url_for`.


Registering the bar
-------------------

It is possible to just pass in a navigational element as a normal parameter to
:func:`~flask.render_template`. Usually it does make sense to register it
on our extension instance using :meth:`.register_element`:

.. code-block:: python

    from flask_nav import Nav

    nav = Nav()
    nav.register_element('top', topbar)

    # [...]
    # later on, initialize your app:
    nav.init_app(app)


Rendering the navbar
--------------------

Once a navbar is available, it can be rendered in the template. The template
global ``nav`` allows looking up registered elements as attributes:

.. code-block:: jinja

   <html>
   <!-- ... -->
   <body>
   {{nav.top.render()}}
   </body>
   </html>

This will render the navigation bar using the default (equal to ``None``)
renderer. Alternatively, a renderer can be specified by name:

.. code-block:: jinja

   {{nav.top.render(renderer='simple')}}
