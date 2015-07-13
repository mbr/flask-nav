from flask import Flask, render_template
from flask_nav import Nav
from flask_nav.elements import *

nav = Nav()


# registers the "top" menubar
nav.register_element('top', Navbar(
    View('Widgits, Inc.', 'index'),
    View('Our Mission', 'about'),
    Subgroup(
        'Products',
        View('Wg240-Series', 'products', product='wg240'),
        View('Wg250-Series', 'products', product='wg250'),
        Separator(),
        Text('Discontinued Products'),
        View('Wg10X', 'products', product='wg10x'),
    ),
    Link('Tech Support', 'http://techsupport.invalid/widgits_inc'),
))


def create_app(configfile=None):
    app = Flask(__name__)
    nav.init_app(app)

    # not good style, but like to keep our examples short
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/products/<product>/')
    def products(product):
        return render_template('index.html', msg='Buy our {}'.format(product))

    @app.route('/about-us/')
    def about():
        return render_template('index.html')

    return app
