import os

from flask import Config

from shorty.utils import get_env


class AppConfig(Config):
    BITLY_URL = get_env('SHORTY_BITLY_URL', default='https://api-ssl.bitly.com/v4')
    BITLY_API_KEY = get_env('SHORTY_BITLY_API_KEY')
    BITLY_GROUP_GUID = get_env('SHORTY_BITLY_GROUP_GUID')
    BITLY_REQUEST_TIMEOUT_SECONDS = get_env('SHORTY_BITLY_REQUEST_TIMEOUT_SECONDS', 1.0, converter=float)

    # Tinyurl config
    TINYURL_URL = os.getenv('SHORTY_TINYURL_URL', 'https://tinyurl.com')
    TINYURL_REQUEST_TIMEOUT_SECONDS = get_env('SHORTY_TINYURL_REQUEST_TIMEOUT_SECONDS', 1.0, converter=float)

    # App config
    DEBUG = get_env('SHORTY_DEBUG', True, converter=bool)
    TESTING = get_env('SHORTY_TESTING', False, converter=bool)
    LOGGING_LEVEL = get_env('SHORTY_LOGGING_LEVEL', 'DEBUG')
    DEFAULT_HOST = get_env('SHORTY_DEFAULT_HOST', '0.0.0.0')
    DEFAULT_PORT = get_env('SHORTY_DEFAULT_PORT', 8080, converter=int)
    JSON_SORT_KEYS = False
