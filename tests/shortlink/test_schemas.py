import pytest
from pydantic import ValidationError

from shorty.shortlink import schemas
from tests.conftest import ShorteningProviderName


def test_shortlinks_request_uninitialised_providers(long_url, mock_allowed_providers) -> None:
    with pytest.raises(ValueError):
        schemas.ShortlinksRequest(url=long_url, provider=ShorteningProviderName.BITLY)


def test_shortlinks_request_initialised_providers(long_url, mock_allowed_providers) -> None:
    schemas.ShortlinksRequest.init_allowed_providers(ShorteningProviderName)
    schemas.ShortlinksRequest(url=long_url, provider=None)
    schemas.ShortlinksRequest(url=long_url, provider=ShorteningProviderName.BITLY)
    schemas.ShortlinksRequest(url=long_url, provider=ShorteningProviderName.TINYURL)


def test_shortlinks_request_initialised_providers_error(long_url, mock_allowed_providers) -> None:
    schemas.ShortlinksRequest.init_allowed_providers(ShorteningProviderName)
    with pytest.raises(ValidationError):
        schemas.ShortlinksRequest(url=long_url, provider='invalid_provider')
