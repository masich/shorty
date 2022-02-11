from flask import Config

from shorty.utils import get_env

DEFAULT_TIMEOUT_SECONDS = 1.0


class AppConfig(Config):
    SHORTENERS = {
        'bitly': {
            'class_path': 'shorty.shortlink.shorteners.bitly_shortener.BitlyShortener',
            'kwargs': {
                'provider_url': get_env('SHORTY_BITLY_URL', 'https://api-ssl.bitly.com/v4'),
                'api_key': get_env('SHORTY_BITLY_API_KEY'),
                'domain': get_env('SHORTY_BITLY_DOMAIN', None),
                'group_guid': get_env('SHORTY_BITLY_GROUP_GUID'),
                'timeout': get_env('SHORTY_BITLY_REQUEST_TIMEOUT_SECONDS', DEFAULT_TIMEOUT_SECONDS, converter=float),
            }
        },
        'tinyurl': {
            'class_path': 'shorty.shortlink.shorteners.tinyurl_shortener.TinyurlShortener',
            'kwargs': {
                'provider_url': get_env('SHORTY_TINYURL_URL', 'https://tinyurl.com'),
                'timeout': get_env('SHORTY_TINYURL_REQUEST_TIMEOUT_SECONDS', DEFAULT_TIMEOUT_SECONDS, converter=float),
            }
        }
    }

    # App config
    DEBUG = get_env('SHORTY_DEBUG', True, converter=bool)
    TESTING = get_env('SHORTY_TESTING', False, converter=bool)
    LOGGING_LEVEL = get_env('SHORTY_LOGGING_LEVEL', 'DEBUG')
    DEFAULT_HOST = get_env('SHORTY_DEFAULT_HOST', '0.0.0.0')
    DEFAULT_PORT = get_env('SHORTY_DEFAULT_PORT', 8080, converter=int)
    JSON_SORT_KEYS = False
