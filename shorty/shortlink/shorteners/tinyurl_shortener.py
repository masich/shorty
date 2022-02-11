import pydantic
import requests

from shorty import utils
from shorty.shortlink.shorteners import exceptions
from shorty.shortlink.shorteners.request_based_shortener import RequestBasedShortener

__all__ = (
    'TinyurlShortener',
)


class TinyurlShortener(RequestBasedShortener):
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

    def make_shorten_request(self, request_data: dict) -> requests.Response:
        return requests.get(
            utils.urljoin(self._provider_url, self.shorten_endpoint),
            params=request_data,
            timeout=self._timeout,
        )

    def short_link_from_response(self, response: requests.Response):
        try:
            url = response.content.decode()
            pydantic.parse_obj_as(pydantic.HttpUrl, url)
        except Exception as e:
            raise exceptions.InvalidShorteningProviderResponse from e

        return url
