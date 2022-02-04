import os
from typing import TypeVar, Type
from urllib.parse import urljoin as legacy_url_join

__all__ = (
    'urljoin',
    'get_env',
)

T = TypeVar('T')

_NOT_SET = object()


def get_env(env_name: str, default: T = _NOT_SET, converter: Type[T] = str) -> T:
    """
    Get environment variable with a given `name` converted to a specific type using `converter`.
    """
    env_value = os.getenv(env_name, default=default)
    if env_value == _NOT_SET:
        raise ValueError(f'Environment variable is required but not set. Env name: {env_name}')

    return converter(env_value)


def urljoin(base: str, url: str, allow_fragments: bool = True) -> str:
    """
    Join `base` url to a `url`.
    """
    if not base.endswith('/'):
        base += '/'

    return legacy_url_join(base, url, allow_fragments=allow_fragments)
