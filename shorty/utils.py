import importlib
import os
from typing import TypeVar, Type
from urllib.parse import urljoin as legacy_url_join

__all__ = (
    'urljoin',
    'get_env',
)

T = TypeVar('T')

_NOT_SET = object()


def get_env(env_name: str, default: T | None = _NOT_SET, converter: Type[T] = str) -> T | None:
    """
    Get environment variable with a given `name` converted to a specific type using `converter`.
    """
    try:
        return converter(os.environ[env_name])
    except KeyError:
        if default is _NOT_SET:
            raise ValueError(f'Environment variable is required but not set. Env name: {env_name}')
        return default


def urljoin(base: str, url: str, allow_fragments: bool = True) -> str:
    """
    Join `base` url to a `url`.
    """
    if not base.endswith('/'):
        base += '/'

    return legacy_url_join(base, url, allow_fragments=allow_fragments)


def dynamically_load(class_path: str) -> Type:
    """
    Dynamically load shortener's class by its full class path.

    :param class_path: Full class path for shortener to load. Must be in form of <module>.<shortener class name>
    """
    module, shortener_class_name = class_path.rsplit('.', maxsplit=1)
    class_ = getattr(importlib.import_module(module), shortener_class_name)

    return class_
