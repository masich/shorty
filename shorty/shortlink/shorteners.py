import logging
from abc import ABC, abstractmethod

import requests

from shorty.shortlink import utils

__all__ = (
    'Shortener',
    'RequestBaseShorteningProvider',
    'BitLyShortener',
    'TinyUrlShortener',
)

logger = logging.getLogger(__name__)


class Shortener(ABC):
    @abstractmethod
    def shorten(self, long_url: str) -> str:
        """
        Shorten a given `long_url`.

        :param long_url: Long url to shorten.
        :return: Short url pointing to a given `long_url`.
        """
        pass


class RequestBaseShorteningProvider(Shortener, ABC):
    @abstractmethod
    def prepare_request_data(self, long_url: str) -> dict:
        """
        Prepare request data for future shortening provider request.

        :param long_url: Long url to shorten.
        :return: Data that will be used to make shortening provider request.
        """
        pass

    @abstractmethod
    def _make_shorten_request(self, request_data: dict) -> requests.Response:
        """
        Request shortening provider using a given `request_data` and return its response.

        :param request_data: Data to make shortening provider request.
        :return: Shortening provider response.
        """
        pass

    @abstractmethod
    def _short_link_from_response(self, response: requests.Response):
        """
        Retrieve a short link from a given shortening provider `response`.

        :param response: Shortening provider response.
        :return: Short url.
        """
        pass

    def shorten(self, long_url) -> str:
        data = self.prepare_request_data(long_url=long_url)
        logger.debug('%s. Prepared request data: %s', self.__class__.__name__, data)

        response = self._make_shorten_request(request_data=data)

        logger.info('%s. Received response from provider', self.__class__.__name__)
        logger.debug('%s. Provider response status code: %s', self.__class__.__name__, response.status_code)
        logger.debug('%s. Provider response status content: %s', self.__class__.__name__, response.content)
        response.raise_for_status()

        return self._short_link_from_response(response)


class BitLyShortener(RequestBaseShorteningProvider):
    shorten_endpoint = 'shorten'

    def __init__(self, provider_url: str, api_key: str,
                 domain: str | None = None, group_guid: str | None = None, timeout: float | None = None):
        """
        Initialize `BitLyShortener`.

        :param provider_url: Bitly provider base url. For example: 'https://bit.ly'
        :param api_key: Bitly API key.
        :param domain: Bitly domain. See https://dev.bitly.com/api-reference#shortenlink for details.
        :param group_guid: Bitly group GUID. See https://dev.bitly.com/api-reference#shortenlink for details.
        :param timeout: Timeout to reach Bitly API. See `requests.request` for details.
        """
        self._provider_url = provider_url
        self._domain = domain
        self._group_guid = group_guid
        self._timeout = timeout
        self._headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }

    def prepare_request_data(self, long_url: str):
        data = {'long_url': long_url}
        if self._group_guid:
            data['group_guid'] = self._group_guid
        if self._domain:
            data['domain'] = self._domain

        return data

    def _make_shorten_request(self, request_data: dict) -> requests.Response:
        return requests.post(
            utils.urljoin(self._provider_url, self.shorten_endpoint),
            json=request_data,
            headers=self._headers,
            timeout=self._timeout,
        )

    def _short_link_from_response(self, response: requests.Response):
        return response.json()['link']


class TinyUrlShortener(RequestBaseShorteningProvider):
    shorten_endpoint = 'api-create.php'

    def __init__(self, provider_url: str, timeout: float | None = None):
        """
        Initialize `TinyUrlShortener`.

        :param provider_url: Tinyurl provider base url. For example: 'https://tinyurl.com'
        :param timeout: Timeout to reach Tinyurl API. See `requests.request` for details.
        """
        self._provider_url = provider_url
        self._timeout = timeout

    def prepare_request_data(self, long_url: str) -> dict:
        return {'url': long_url}

    def _make_shorten_request(self, request_data: dict) -> requests.Response:
        return requests.get(
            utils.urljoin(self._provider_url, self.shorten_endpoint),
            params=request_data,
            timeout=self._timeout,
        )

    def _short_link_from_response(self, response: requests.Response):
        return response.content.decode()
