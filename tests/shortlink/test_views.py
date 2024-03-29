from typing import Type
from unittest.mock import Mock

import pytest
from werkzeug import exceptions as flask_exceptions

from shorty.shortlink.exceptions import APIValidationError
from shorty.shortlink.shorteners import BitlyShortener, TinyurlShortener, exceptions as shortener_exceptions
from shorty.shortlink.views import ShortlinksAPI
from tests.conftest import ShorteningProviderName, SHORT_URL


@pytest.fixture(params=[Mock(return_value=SHORT_URL)])
def mocked_shortener(request):
    shortener = Mock()
    shortener.shorten = request.param
    return shortener


class TestShortlinksAPI:
    @pytest.mark.parametrize(
        'json',
        (
            {'url': 'https://test.com', 'provider': 'tinyurl'},
            {'url': 'http://test.com:8080/some/path#fragment', 'provider': 'tinyurl'},
            {'url': 'https://test.com', 'provider': 'bitly'},
        )
    )
    def test_parse_request_json_ok(self, json: dict) -> None:
        assert ShortlinksAPI.parse_request_json(json)

    @pytest.mark.parametrize(
        'json,expected_exception',
        (
            ({'url': 'https://test.com', 'provider': 'invalid_provider_name'}, APIValidationError),
            ({'url': 'htts://test.com', 'provider': 'bitly'}, APIValidationError),
            ({'url': 'testcom', 'provider': 'bitly'}, APIValidationError),
        )
    )
    def test_parse_request_json_invalid(self, json: dict, expected_exception: Type[Exception]) -> None:
        with pytest.raises(expected_exception):
            ShortlinksAPI.parse_request_json(json)

    def test_get_short_link_ok(self, short_url, mocked_shortener, long_url) -> None:
        assert short_url == ShortlinksAPI.get_short_link(long_url, mocked_shortener)

    @pytest.mark.parametrize(
        'mocked_shortener,expected_exception',
        (
            (Mock(side_effect=shortener_exceptions.ShorteningProviderTimeout), flask_exceptions.GatewayTimeout),
            (Mock(side_effect=shortener_exceptions.ShorteningProviderRequestException), flask_exceptions.BadGateway),
        ),
        indirect=('mocked_shortener',)
    )
    def test_get_short_link_ok(self, mocked_shortener, long_url, expected_exception) -> None:
        with pytest.raises(expected_exception):
            ShortlinksAPI.get_short_link(long_url, mocked_shortener)

    @pytest.mark.parametrize(
        'provider,shortener_class',
        (
            (ShorteningProviderName.BITLY, BitlyShortener),
            (ShorteningProviderName.TINYURL, TinyurlShortener),
        )
    )
    def test_post_bitly(self, post, mocker, provider, shortener_class, short_url, long_url, mock_allowed_providers):
        shortener = mocker.patch.object(shortener_class, attribute='shorten', return_value=short_url)
        response = post(
            '/shortlinks',
            data={
                'url': long_url,
                'provider': provider,
            }
        )

        assert 200 == response.status_code
        assert long_url == response.json['url']
        assert short_url == response.json['link']
        shortener.assert_called_once_with(long_url)

    def test_post_empty_provider_all(self, post, mocker, short_url, long_url, mock_allowed_providers):
        shorteners = (
            mocker.patch.object(
                BitlyShortener,
                attribute='shorten',
                side_effect=shortener_exceptions.ShortenerException,
            ),
            mocker.patch.object(TinyurlShortener, attribute='shorten', return_value=short_url),
        )
        response = post('/shortlinks', data={'url': long_url})

        for shortener in shorteners:
            shortener.assert_called_once_with(long_url)

        assert 200 == response.status_code
        assert long_url == response.json['url']
        assert short_url == response.json['link']

    def test_post_empty_provider_first(self, post, mocker, short_url, long_url, mock_allowed_providers):
        bitly_shortener = mocker.patch.object(BitlyShortener, attribute='shorten', return_value=short_url)
        tinyurl_shortener = mocker.patch.object(TinyurlShortener, attribute='shorten', return_value=short_url)
        response = post('/shortlinks', data={'url': long_url})

        assert 200 == response.status_code
        assert long_url == response.json['url']
        assert short_url == response.json['link']
        bitly_shortener.assert_called_once_with(long_url)
        tinyurl_shortener.assert_not_called()

    def test_post_empty_provider_all_invalid(self, post, mocker, short_url, long_url, mock_allowed_providers):
        shorteners = (
            mocker.patch.object(
                BitlyShortener,
                attribute='shorten',
                side_effect=shortener_exceptions.ShortenerException,
            ),
            mocker.patch.object(
                TinyurlShortener,
                attribute='shorten',
                side_effect=shortener_exceptions.ShortenerException,
            ),
        )
        response = post('/shortlinks', data={'url': long_url})

        for shortener in shorteners:
            shortener.assert_called_once_with(long_url)

        assert 500 == response.status_code
