Other software
==============

Flask-Navigation
----------------

Flask-Nav owes a some good core ideas to Flask-Navigation_, which is about a
year older and the first place the author looked before deciding to write
Flask-Nav. In defense of the reimplementation (opposed to just submitting
patches for Flask-Navigation_) [1]_, here are some key differences:

* Flask-Navigation_ rolls all element types into a single ``Item`` class,
  which serves as label, view and link element. This makes it a little hard
  to extend.
* The HTML generation in Flask-Navigation_ is done inside the package itself,
  while Flask-Nav uses a more complete, external solution.
* Navigational structure creation and rendering are separate in Flask-Nav
  (see :class:`.Renderer`). This allows for more than one way of
  rendering the same navbar, allowing other packages (such as Flask-Bootstrap_,
  see below) to supply renderers as well.
* Some technical choices were deemed a little strange and have been avoided
  (`BoundTypeProperty <https://flask-navigation.readthedocs.org/en/latest/
   #flask.ext.navigation.utils.BoundTypeProperty>`).
* While Flask-Navigation_ uses signals and hooks to regenerate navigation bars
  on every request, Flask-Nav achievies dynamic behaviour by lazily
  instantiating naviigation bars when they are needed and at the last
  possible moment.


.. _Flask-Navigation: https://flask-navigation.readthedocs.org/en/latest/
.. [1] All this information refers to Flask-Navigation 0.2.0 or
       `38fa83 <https://github.com/tonyseek/flask-navigation/
       tree/38fa83addcbe62f31516763fbe3c0bbdc793dc96>`_, which were the
       most recent versions when Flask-Nav was written.


Flask-Bootstrap
---------------

The initial driving force behind Flask-Nav was the desire to create a macro for
Flask-Bootstrap_ that would render Bootstrap-y navigational items. See the
Flask-Bootstrap_ docs for details.

.. _Flask-Bootstrap: http://pythonhosted.org/Flask-Bootstrap

