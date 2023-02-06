# Shorty
Shorty is a simple URL shortening microservice that supports two shortening providers: bit.ly and tinyurl.com. It's easy to use and extendable: if you want to add a new provider, you only have to implement [shortener interface](https://github.com/masich/shorty/blob/master/shorty/shortlink/shorteners/shortener.py) and change the [configuration file](https://github.com/masich/shorty/blob/master/shorty/config.py).

It has an endpoint: `POST /shortlinks`, which can be used for shortening purposes. This endpoint accepts JSON with the following schema:

| param    | type   | required | description                        |
|----------|--------|----------|------------------------------------|
| url      | string | Y        | The URL to shorten                 |
| provider | string | N        | The provider to use for shortening |

Suppose the client hasn't specified any `provider` on request. In that case, the service will use the first provider from the available ones (bitly or tinyurl, by default), which will successfully return shortened URL after processing.

Its response is a `Shortlink` resource containing the following:

| param    | type   | required | description                        |
|----------|--------|----------|------------------------------------|
| url      | string | Y        | The original URL                   |
| link     | string | Y        | The shortened link                 |

For example:

```json
{
  "url": "https://example.com",
  "link": "https://bit.ly/e2142sa"
}
```

Also, it returns a JSON response with a sensible HTTP status in case of
errors or failures.

> Test coverage is 97%.

Running guide
-------------

1. Install project requirements.

```shell
pip install -r requirements.txt
```

2. Set up environment variables.

| variable name                          | type   | required | default                      | description                           |
|----------------------------------------|--------|----------|------------------------------|---------------------------------------|
| SHORTY_BITLY_API_KEY                   | string | Y        |                              | Bitly service API key.                |
| SHORTY_BITLY_GROUP_GUID                | string | Y        |                              | Bitly group GUID for shortening.      |
| SHORTY_BITLY_URL                       | string | N        | https://api-ssl.bitly.com/v4 | Bitly service base URL.               |
| SHORTY_BITLY_DOMAIN                    | string | N        | None                         | Bitly domain for shortening base URL. |
| SHORTY_BITLY_REQUEST_TIMEOUT_SECONDS   | string | N        | 1.0                          | Bitly service request timeout.        |
| SHORTY_TINYURL_URL                     | string | N        | https://tinyurl.com          | Tinyurl base url.                     |
| SHORTY_TINYURL_REQUEST_TIMEOUT_SECONDS | string | N        | 1.0                          | Tinyurl request timeout.              |
| SHORTY_DEBUG                           | string | N        | True                         | Run Shorty in debug mode or not.      |
| SHORTY_TESTING                         | string | N        | False                        | Run Shorty in testing mode or not.    |
| SHORTY_LOGGING_LEVEL                   | string | N        | DEBUG                        | Shorty service logging level.         |
| SHORTY_DEFAULT_HOST                    | string | N        | 0.0.0.0                      | Default Shorty service host.          |
| SHORTY_DEFAULT_PORT                    | string | N        | 8080                         | Default Shorty service port.          |

2. (Optional). For testing purposes, you can create the `.env` file with the following content in the project's root
   directory.

```dotenv
SHORTY_BITLY_URL='https://mockbin.org/bin/383dbfe8-947f-4020-ba72-0a7366e95fbe'  # mocked bitly endpoint
SHORTY_TINYURL_URL='https://mockbin.org/bin/f011a7bc-3544-4eb7-a185-4b2ef6b99e33'  # mocked tinyurl endpoint
SHORTY_BITLY_API_KEY='some_api_key'
SHORTY_BITLY_GROUP_GUID='some_group_id'
```

3. Run the Shorty service using the following command from the project's root directory:

```shell
python run.py --host <SOME_HOST> --post <SOME_PORT>
```

`--host` and `--port` are optional and will use `$SHORTY_DEFAULT_HOST` and `$SHORTY_DEFAULT_PORT` respectively by
default.

4. Enjoy shortening!

Running guide
-------------

You can access Swagger documentation for Shorty by going to the `apidocs/` endpoint.
    
