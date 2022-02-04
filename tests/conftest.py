import functools
import json
import os
import sys
from typing import Callable

import pytest
from flask import Flask
# Set up the path to import from `shorty`.
from flask.testing import FlaskClient

root = os.path.join(os.path.dirname(__file__))
package = os.path.join(root, '..')
sys.path.insert(0, os.path.abspath(package))

from shorty.app import create_app  # noqa

LONG_URL = 'https://long.com'
SHORT_URL = 'https://short.com'


class TestResponseClass(Flask.response_class):
    @property
    def json(self):
        return json.loads(self.data)


Flask.response_class = TestResponseClass


def humanize_werkzeug_client(client_method) -> Callable:
    """
    Wraps a `werkzeug` client method (the client provided by `Flask`) to make it easier to use in tests.
    """

    @functools.wraps(client_method)
    def wrapper(url: str, **kwargs):
        # Always set the content type to `application/json`.
        headers = kwargs.setdefault('headers', {})
        headers['content-type'] = 'application/json'

        # If data is present then make sure it is json encoded.
        if 'data' in kwargs:
            data = kwargs['data']
            if isinstance(data, dict):
                kwargs['data'] = json.dumps(data)

        kwargs['buffered'] = True

        return client_method(url, **kwargs)

    return wrapper


@pytest.fixture(scope='session', autouse=True)
def app(request) -> Flask:
    app = create_app({
        'TESTING': True,
        'DEBUG': True,
        'BITLY_URL': 'https://test.bitly/',
        'TINYURL_URL': 'https://test.tinyurl/',
    })

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    request.addfinalizer(ctx.pop)

    return app


@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def get(client):
    return humanize_werkzeug_client(client.get)


@pytest.fixture
def post(client):
    return humanize_werkzeug_client(client.post)


@pytest.fixture
def long_url() -> str:
    return LONG_URL


@pytest.fixture
def short_url() -> str:
    return SHORT_URL
