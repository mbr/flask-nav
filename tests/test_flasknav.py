import pytest

from flask import Flask
from flask_nav.elements import View


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'testing.local'

    @app.route('/hello/<arg1>/')
    def hello(arg1):
        return str(app.hello_view.active)

    return app


@pytest.fixture()
def hello_view(app):
    v = View('notext', 'hello', arg1=1, q1='q')
    app.hello_view = v
    return v


def test_view_arguments(app, hello_view):
    with app.app_context():

        # since we're using the app context, flask should generate an
        # external url. inside a real request, chances are a relative url
        # would be generated instead
        assert hello_view.get_url() == 'http://testing.local/hello/1/?q1=q'


def test_active_without_query(app, hello_view):
    with app.app_context():
        url = hello_view.get_url() + '&foo=bar'

    with app.test_client() as c:
        assert 'True' == c.get(url).data.decode('utf8')


def test_active_with_query(app, hello_view):
    hello_view.ignore_query = False

    with app.app_context():
        url = hello_view.get_url() + '&foo=bar'

    with app.test_client() as c:
        assert 'False' == c.get(url).data.decode('utf8')
