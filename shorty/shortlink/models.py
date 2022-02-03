from enum import Enum

from pydantic import BaseModel, HttpUrl

__all__ = (
    'ShorteningProviderName',
    'ShortenersRequest',
    'ShortenersResponse',
)


class ShorteningProviderName(str, Enum):
    BIT_LY = 'bit.ly'
    TINYURL = 'tinyurl.com'


class ShortenersRequest(BaseModel):
    url: HttpUrl  # Url to shorten
    provider: ShorteningProviderName | None  # Shortening provider to use for shortening

    class Config:
        use_enum_values = True


class ShortenersResponse(BaseModel):
    url: HttpUrl  # Original long url
    link: HttpUrl  # Short link
