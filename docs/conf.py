extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']

project = u'Flask-Nav'
copyright = u'2015, Marc Brinkmann'
author = u'Marc Brinkmann'
version = '0.2'
release = '0.2.dev1'

pygments_style = 'sphinx'
html_theme = 'alabaster'

intersphinx_mapping = {
    'https://docs.python.org/': None,
    'http://flask.pocoo.org/docs/': None,
}
