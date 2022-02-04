import logging
from abc import ABC, abstractmethod

import requests

from shorty.shortlink.shorteners import exceptions
from shorty.shortlink.shorteners.shortener import Shortener

__all__ = (
    'RequestBasedShortener',
)

logger = logging.getLogger(__name__)


class RequestBasedShortener(Shortener, ABC):
    @abstractmethod
    def prepare_request_data(self, long_url: str) -> dict:
        """
        Prepare request data for future shortening provider request.

        :param: long_url: Long url to shorten.
        :return: Data that will be used to make shortening provider request.
        """
        pass

    @abstractmethod
    def make_shorten_request(self, request_data: dict) -> requests.Response:
        """
        Request shortening provider using a given `request_data` and return its response.

        :param: request_data: Data to make shortening provider request.
        :return: Shortening provider response.
        """
        pass

    @abstractmethod
    def short_link_from_response(self, response: requests.Response) -> str:
        """
        Retrieve a short link from a given shortening provider `response`.

        :param: response: Shortening provider response.
        :return: Short url.
        """
        pass

    def shorten(self, long_url) -> str:
        """
        Shorten a given `long_url` using a specific shortening provider.

        :param: long_url: Long url to shorten.
        :raises: exceptions.CouldNotReachShorteningProvider: If provider could not be reached during request.
        :raises: exceptions.ShorteningProviderTimeout: If timeout error occurred during shortening provider request.
        :raises: exceptions.ShorteningProviderRequestException: If some other error occurred during request.
        :raises: exceptions.InvalidShorteningProviderResponse: If provider request returned invalid response.
        :return: Short url pointing to a given `long_url`.
        """
        data = self.prepare_request_data(long_url=long_url)
        logger.debug('%s. Prepared request data: %s', self.__class__.__name__, data)

        try:
            response = self.make_shorten_request(request_data=data)
        except requests.exceptions.Timeout as e:
            raise exceptions.ShorteningProviderTimeout from e
        except requests.exceptions.HTTPError as e:
            raise exceptions.ShorteningProviderRequestException from e

        logger.info('%s. Received response from provider', self.__class__.__name__)
        logger.debug('%s. Provider response status code: %s', self.__class__.__name__, response.status_code)
        logger.debug('%s. Provider response status content: %s', self.__class__.__name__, response.content)

        try:
            response.raise_for_status()
            return self.short_link_from_response(response)
        except Exception as e:
            raise exceptions.InvalidShorteningProviderResponse from e
