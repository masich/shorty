import os

import pytest
from pytest_mock import MockerFixture

from shorty import utils


@pytest.mark.parametrize(
    'base,url,expected',
    (
        ('https://some.url', 'path', 'https://some.url/path'),
        ('http://some.url', 'path', 'http://some.url/path'),
        ('some.url', 'path', 'some.url/path'),
        ('https://some.url/', 'path', 'https://some.url/path'),
        ('http://some.url/', 'path', 'http://some.url/path'),
        ('some.url/', 'path', 'some.url/path'),
    )
)
def test_urljoin(base, url, expected) -> None:
    assert utils.urljoin(base, url) == expected


@pytest.mark.parametrize(
    'env_name,converter,environ,expected',
    (
        ('SOME_VAR', str, {'SOME_VAR': 'some_value'}, 'some_value'),
        ('SOME_VAR', int, {'SOME_VAR': '12'}, 12),
        ('SOME_VAR', float, {'SOME_VAR': '12'}, 12.0),
    )
)
def test_get_env_ok(env_name, converter, environ, expected, mocker: MockerFixture) -> None:
    mocker.patch.object(os, attribute='environ', new=environ)
    assert utils.get_env(env_name, converter=converter) == expected


@pytest.mark.parametrize(
    'env_name,default,environ,expected',
    (
        ('SOME_VAR', 'some_value', {}, 'some_value'),
        ('SOME_VAR', 'some_value', {'SOME_VAR_2': '12'}, 'some_value'),
    )
)
def test_get_env_default(env_name, default, environ, expected, mocker: MockerFixture) -> None:
    mocker.patch.object(os, attribute='environ', new=environ)
    assert utils.get_env(env_name, default=default) == expected


@pytest.mark.parametrize(
    'env_name,converter,environ,exception',
    (
        ('SOME_VAR', str, {}, ValueError),
        ('SOME_VAR', int, {}, ValueError),
        ('SOME_VAR', int, {'SOME_VAR': 'invalid_value'}, ValueError),
    )
)
def test_get_env_error(env_name, converter, environ, exception, mocker: MockerFixture) -> None:
    mocker.patch.object(os, attribute='environ', new=environ)
    with pytest.raises(exception):
        utils.get_env(env_name, converter=converter)
