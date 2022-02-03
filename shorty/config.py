import os

# Shortening providers config
# bitly config
# BITLY_URL = 'https://mockbin.org/bin/383dbfe8-947f-4020-ba72-0a7366e95fbe'  # 'https://api-ssl.bitly.com/v4'  # https://mockbin.org/bin/383dbfe8-947f-4020-ba72-0a7366e95fbe
BITLY_URL = os.getenv('SHORTY_BITLY_URL') or 'https://api-ssl.bitly.com/v4'
BITLY_API_KEY = os.getenv('SHORTY_BITLY_API_KEY') or 'some_api_key'
BITLY_GROUP_GUID = os.getenv('SHORTY_BITLY_GROUP_GUID') or 'some_group_id'
BITLY_REQUEST_TIMEOUT_SECONDS = os.getenv('SHORTY_BITLY_REQUEST_TIMEOUT_SECONDS')

# tinyurl config
TINYURL_URL = os.getenv('SHORTY_TINYURL_URL') or 'https://tinyurl.com'
TINYURL_REQUST_TIMEOUT_SECONDS = os.getenv('SHORTY_TINYURL_REQUST_TIMEOUT_SECONDS')

# App config
DEBUG = os.getenv('SHORTY_DEBUG') or True
TESTING = bool(os.getenv('SHORTY_TESTING'))
JSON_SORT_KEYS = False
LOGGING_LEVEL = os.getenv('SHORTY_LOGGING_LEVEL') or 'DEBUG' if DEBUG else 'WARNING'
HOST = os.getenv('SHORTY_HOST') or '0.0.0.0'
PORT = os.getenv('SHORTY_PORT') or 8080
