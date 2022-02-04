import pytest

from shorty.shortlink import utils


@pytest.mark.parametrize(
    'base,url,expected',
    (
        ('https://some.url', 'path', 'https://some.url/path'),
        ('http://some.url', 'path', 'http://some.url/path'),
        ('some.url', 'path', 'some.url/path'),
        ('https://some.url/', 'path', 'https://some.url/path'),
        ('http://some.url/', 'path', 'http://some.url/path'),
        ('some.url/', 'path', 'some.url/path'),
    )
)
def test_urljoin(base, url, expected) -> None:
    assert utils.urljoin(base, url) == expected
