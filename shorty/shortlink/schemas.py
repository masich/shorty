from typing import Iterable

from pydantic import BaseModel, HttpUrl, validator, errors

__all__ = (
    'ShortlinksRequest',
    'ShortlinksResponse',
    'init_schemas',
)


class ShortlinksRequest(BaseModel):
    url: HttpUrl  # Url to shorten
    provider: str | None  # Shortening provider to use for shortening

    __allowed_providers__ = tuple()

    def __init__(self, **kwargs):
        if not self.__allowed_providers__:
            raise ValueError('Allowed providers are\'t initialised. Call `init_allowed_providers` for initialisation.')

        super().__init__(**kwargs)

    @validator('provider')
    def validate_provider(cls, provider_value: str | None) -> str | None:
        if not (provider_value is None or provider_value in cls.__allowed_providers__):
            raise errors.WrongConstantError(given=provider_value, permitted=cls.__allowed_providers__)

        return provider_value

    @classmethod
    def init_allowed_providers(cls, providers: Iterable[str]) -> None:
        """
        Initialise allowed providers.
        makes it possible to set up validation dynamically.
        """
        cls.__allowed_providers__ = tuple(providers)


class ShortlinksResponse(BaseModel):
    url: HttpUrl  # Original long url
    link: HttpUrl  # Short link


def init_schemas(provider_names: Iterable[str]) -> None:
    """
    Initialise Shortlink schemas.
    """
    ShortlinksRequest.init_allowed_providers(provider_names)
