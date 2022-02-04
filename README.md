Software Engineer Task
======================

At Plum, we have a lot of services that need to work together to deliver our product. Many of these services talk to
third-party providers to perform their operations – for example moving money, performing background checks, sending
messages or emails, etc.

In a lot of cases - due to business, compliance or technical reasons - we need to support multiple third-party providers
for the same operation, some of which have wildy different specifications, ranging from simple REST APIs to SOAP.

To maintain our sanity, we abstract these third-parties behind interfaces and expose consistent APIs for the rest of the
system to consume. Each service should be able to pick sensible defaults (and fallbacks, if, for example, a provider is
unavailable) or allow the consumer to specify the provider if they wish to do so.

Mission
-------

Your mission, should you choose to accept it, is to build a microservice called `shorty`, which supports two URL
shortening providers: [bit.ly](https://dev.bitly.com/) and [tinyurl.com](https://gist.github.com/MikeRogers0/2907534).
You don't need to actually sign up to these providers, just implement their API. The service exposes a single
endpoint: `POST /shortlinks`. The endpoint should receive JSON with the following schema:

| param    | type   | required | description                        |
|----------|--------|----------|------------------------------------|
| url      | string | Y        | The URL to shorten                 |
| provider | string | N        | The provider to use for shortening |

The response should be a `Shortlink` resource containing:

| param    | type   | required | description                        |
|----------|--------|----------|------------------------------------|
| url      | string | Y        | The original URL                   |
| link     | string | Y        | The shortened link                 |

For example:

```json
{
  "url": "https://example.com",
  "link": "https://bit.ly/8h1bka"
}
```

You are free to decide how to pick between the providers if one is not requested and what your fallback strategy is in
case your primary choice fails. Your endpoint needs to return a JSON response with a sensible HTTP status in case of
errors or failures.

What you need to do
-------------------

1. Create a Python env (using Python 3.6+) and install the requirements.
2. Build the `POST /shortlinks` endpoint. We've provided a skeleton API using `flask`.
3. Write some tests. We've provided a test blueprint using `pytest`.

Deliverable
-----------

You should deliver your solution as a Pull Request in your repo. Document your design choices and anything else you
think we need to know in the PR description.

What we look for
----------------

In a nutshell, we're looking for tidy, production-quality code, a scalable design and sensible tests (unit tests,
integration tests or both?). Imagine that your code will be read by other developers in your team – keep them happy :-)

Resources
---------

1. `Flask`: http://flask.pocoo.org/
2. `pytest`: http://pytest.org/latest/
3. `virtualenvwrapper`: https://virtualenvwrapper.readthedocs.io/en/latest/
4. `HTTP statuses`: https://httpstatuses.com/

Disclaimer
----------

We will not use any of this code for any of Plum's applications.


Running guide
-------------

1. Setup environment variables.

| variable name                         | type   | required | default                      | description                        |
|---------------------------------------|--------|----------|------------------------------|------------------------------------|
| BITLY_API_KEY                         | string | Y        |                              | Bitly service API key.             |
| SHORTY_BITLY_GROUP_GUID               | string | Y        |                              | Bitly group GUID for shortening.   |
| BITLY_URL                             | string | N        | https://api-ssl.bitly.com/v4 | Bitly service base URL.            |
| SHORTY_BITLY_REQUEST_TIMEOUT_SECONDS  | string | N        | 1.0                          | Bitly service request timeout.     |
| SHORTY_TINYURL_URL                    | string | N        | https://tinyurl.com          | Tinyurl base url.                  |
| SHORTY_TINYURL_REQUST_TIMEOUT_SECONDS | string | N        | 1.0                          | Tinyurl request timeout.           |
| SHORTY_DEBUG                          | string | N        | True                         | Run Shorty in debug mode or not.   |
| SHORTY_TESTING                        | string | N        | False                        | Run Shorty in testing mode or not. |
| SHORTY_LOGGING_LEVEL                  | string | N        | DEBUG                        | Shorty service logging level.      |
| SHORTY_DEFAULT_HOST                   | string | N        | 0.0.0.0                      | Default Shorty service host.       |
| SHORTY_DEFAULT_PORT                   | string | N        | 8080                         | Default Shorty service port.       |

2. Optional. For testing purposes you can create the `.env` file with the following content in the project's root
   directory.

```dotenv
SHORTY_BITLY_URL='https://mockbin.org/bin/383dbfe8-947f-4020-ba72-0a7366e95fbe'
SHORTY_TINYURL_URL='https://mockbin.org/bin/f011a7bc-3544-4eb7-a185-4b2ef6b99e33'
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
    