import os

# Shortening providers config
# Bitly config
BITLY_URL = os.getenv('SHORTY_BITLY_URL', 'https://api-ssl.bitly.com/v4')
BITLY_API_KEY = os.getenv('SHORTY_BITLY_API_KEY', 'some_api_key')
BITLY_GROUP_GUID = os.getenv('SHORTY_BITLY_GROUP_GUID', 'some_group_id')
BITLY_REQUEST_TIMEOUT_SECONDS = float(os.getenv('SHORTY_BITLY_REQUEST_TIMEOUT_SECONDS', 1.0))

# Tinyurl config
TINYURL_URL = os.getenv('SHORTY_TINYURL_URL', 'https://tinyurl.com')
TINYURL_REQUST_TIMEOUT_SECONDS = float(os.getenv('SHORTY_TINYURL_REQUST_TIMEOUT_SECONDS', 1.0))

# App config
DEBUG = bool(os.getenv('SHORTY_DEBUG', True))
TESTING = bool(os.getenv('SHORTY_TESTING'))
LOGGING_LEVEL = os.getenv('SHORTY_LOGGING_LEVEL', 'DEBUG' if DEBUG else 'WARNING')
DEFAULT_HOST = os.getenv('SHORTY_DEFAULT_HOST', '0.0.0.0')
DEFAULT_PORT = int(os.getenv('SHORTY_DEFAULT_PORT', 8080))
JSON_SORT_KEYS = False
