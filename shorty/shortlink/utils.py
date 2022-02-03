from urllib.parse import urljoin as legacy_url_join

__all__ = (
    'urljoin',
)


def urljoin(base: str, url: str, allow_fragments: bool = True) -> str:
    """
    Join `base` url to a `url`.
    """
    if not base.endswith('/'):
        base += '/'

    return legacy_url_join(base, url, allow_fragments=allow_fragments)
