import requests

from shorty.shortlink import utils
from shorty.shortlink.shorteners.request_based_shortener import RequestBasedShortener

__all__ = (
    'BitlyShortener',
)


class BitlyShortener(RequestBasedShortener):
    shorten_endpoint = 'shorten'

    def __init__(self, provider_url: str, api_key: str,
                 domain: str | None = None, group_guid: str | None = None, timeout: float | None = None):
        """
        Initialize `BitLyShortener`.

        :param: provider_url: Bitly provider base url. For example: 'https://bit.ly'
        :param: api_key: Bitly API key.
        :param: domain: Bitly domain. See https://dev.bitly.com/api-reference#shortenlink for details.
        :param: group_guid: Bitly group GUID. See https://dev.bitly.com/api-reference#shortenlink for details.
        :param: timeout: Timeout to reach Bitly API. See `requests.request` for details.
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

    def make_shorten_request(self, request_data: dict) -> requests.Response:
        return requests.post(
            utils.urljoin(self._provider_url, self.shorten_endpoint),
            json=request_data,
            headers=self._headers,
            timeout=self._timeout,
        )

    def short_link_from_response(self, response: requests.Response):
        return response.json()['link']
