from typing import Any

import pytest
import requests
from pytest_mock import MockerFixture

from shorty.shortlink.shorteners import BitlyShortener, TinyurlShortener, exceptions
from tests.conftest import LONG_URL


class DummyResponse(requests.Response):
    def __init__(self, status_code: int | None = None, content: bytes | None = None, json: dict | None = None):
        super().__init__()
        self.status_code = status_code
        self._json = json
        self._content = content

    def json(self, *_, **__) -> dict[str, Any]:
        return self._json


@pytest.fixture
def empty_response() -> requests.Response:
    return DummyResponse(status_code=200)


class TestBitLyShortener:
    @pytest.fixture
    def request_data(self, long_url) -> dict[str, Any]:
        return {'link': long_url}

    @pytest.fixture(params=(('https://bit.ly', 'api_key', 'some_domain', 'some_guid', 1),))
    def shortener(self, request) -> BitlyShortener:
        return BitlyShortener(*request.param)

    @pytest.fixture
    def response(self, short_url) -> requests.Response:
        return DummyResponse(
            status_code=200,
            json={'link': short_url},
        )

    @pytest.mark.parametrize(
        'shortener,expected',
        (
            (('https://bit.ly', 'api_key'), {'long_url': LONG_URL}),
            (
                ('https://bit.ly', 'api_key', 'some_domain'),
                {'long_url': LONG_URL, 'domain': 'some_domain'},
            ),
            (
                ('https://bit.ly', 'api_key', 'some_domain', 'some_guid'),
                {'long_url': LONG_URL, 'domain': 'some_domain', 'group_guid': 'some_guid'},
            ),
            (
                ('https://bit.ly', 'api_key', 'some_domain', 'some_guid', 1),
                {'long_url': LONG_URL, 'domain': 'some_domain', 'group_guid': 'some_guid'},
            ),
        ),
        indirect=('shortener',),
    )
    def test_prepare_request_data(self, long_url, shortener: BitlyShortener, expected: dict) -> None:
        assert shortener.prepare_request_data(long_url) == expected

    def test_make_shorten_request(self, mocker: MockerFixture, empty_response, shortener, request_data) -> None:
        mock_post = mocker.patch.object(requests, attribute='post', return_value=empty_response)
        assert shortener.make_shorten_request(request_data) == empty_response
        mock_post.assert_called_once_with(
            'https://bit.ly/shorten',
            json=request_data,
            headers={
                'Authorization': 'Bearer api_key',
                'Content-Type': 'application/json',
            },
            timeout=1,
        )

    def test_short_link_from_response(self, shortener, response, short_url) -> None:
        assert shortener.short_link_from_response(response) == short_url

    @pytest.mark.parametrize('status_code', (200, 201, 202, 300, 301, 302, 400, 401, 500))
    def test_shorten(self, mocker: MockerFixture, shortener, request_data, long_url, status_code, short_url):
        mock_prepare_request_data = mocker.patch.object(
            shortener,
            attribute='prepare_request_data',
            return_value=request_data,
        )
        mock_make_request = mocker.patch.object(
            shortener,
            attribute='make_shorten_request',
            return_value=DummyResponse(status_code=status_code, json={'link': short_url}),
        )

        if 200 <= status_code < 400:
            assert shortener.shorten(long_url) == short_url
        else:
            with pytest.raises(exceptions.ShortenerException):
                shortener.shorten(long_url)

        mock_prepare_request_data.assert_called_once_with(long_url=long_url)
        mock_make_request.assert_called_once_with(request_data=request_data)


class TestTinyurlShortener:
    @pytest.fixture
    def request_data(self, long_url) -> dict[str, Any]:
        return {'url': long_url}

    @pytest.fixture(params=(('https://tinyurl.com', 1),))
    def shortener(self, request) -> TinyurlShortener:
        return TinyurlShortener(*request.param)

    @pytest.fixture(params=(200,))
    def response(self, request, short_url) -> requests.Response:
        return DummyResponse(
            status_code=request.param,
            content=short_url.encode(),
        )

    @pytest.mark.parametrize(
        'shortener,expected',
        (
            (('https://bit.ly',), {'url': LONG_URL}),
            (('https://bit.ly', 1), {'url': LONG_URL}),
        ),
        indirect=('shortener',)
    )
    def test_prepare_request_data(self, long_url, shortener: TinyurlShortener, expected: dict) -> None:
        assert shortener.prepare_request_data(long_url) == expected

    def test_make_shorten_request(self, mocker: MockerFixture, empty_response, shortener, request_data) -> None:
        mock_get = mocker.patch.object(requests, attribute='get', return_value=empty_response)
        assert shortener.make_shorten_request(request_data) == empty_response
        mock_get.assert_called_once_with(
            'https://tinyurl.com/api-create.php',
            params=request_data,
            timeout=1,
        )

    def test_short_link_from_response(self, shortener, response, short_url) -> None:
        assert shortener.short_link_from_response(response) == short_url

    @pytest.mark.parametrize(
        'response',
        (200, 201, 202, 300, 301, 302, 400, 401, 500),
        indirect=True,
    )
    def test_shorten(self, mocker: MockerFixture, response: DummyResponse, shortener, request_data, long_url,
                     short_url):
        mock_prepare_request_data = mocker.patch.object(
            shortener,
            attribute='prepare_request_data',
            return_value=request_data,
        )
        mock_make_request = mocker.patch.object(
            shortener,
            attribute='make_shorten_request',
            return_value=response,
        )

        if 200 <= response.status_code < 400:
            assert shortener.shorten(long_url) == short_url
        else:
            with pytest.raises(exceptions.ShortenerException):
                shortener.shorten(long_url)

        mock_prepare_request_data.assert_called_once_with(long_url=long_url)
        mock_make_request.assert_called_once_with(request_data=request_data)
