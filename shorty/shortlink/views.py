import logging
from typing import Mapping

import pydantic
from flask import blueprints, jsonify, Response, request as flask_request
from flask.views import MethodView
from werkzeug import exceptions as flask_exceptions

from shorty.shortlink import shorteners
from shorty.shortlink.exceptions import APIValidationError
from shorty.shortlink.models import ShorteningProviderName, ShortenersRequest, ShortenersResponse
from shorty.shortlink.shorteners import exceptions as shortener_exceptions

__all__ = (
    'blueprint',
    'ShortlinksAPI',
)

logger = logging.getLogger(__name__)

blueprint = blueprints.Blueprint('shortlink', __name__)


class ShortlinksAPI(MethodView):
    _provider_shortener_mapping: dict[ShorteningProviderName, shorteners.RequestBasedShortener]

    @classmethod
    def init_provider_shorter_mapping(cls, setup_state: blueprints.BlueprintSetupState) -> None:
        """
        Initialise mapping includes all available shortening providers.
        Must be invoked oly after initialisation of the `Flask` application.
        """
        cls._provider_shortener_mapping = {
            ShorteningProviderName.BITLY: shorteners.BitlyShortener(
                provider_url=setup_state.app.config['BITLY_URL'],
                api_key=setup_state.app.config['BITLY_API_KEY'],
                group_guid=setup_state.app.config.get('BITLY_GROUP_GUID'),
                timeout=setup_state.app.config.get('BITLY_REQUEST_TIMEOUT_SECONDS'),
            ),
            ShorteningProviderName.TINYURL: shorteners.TinyurlShortener(
                provider_url=setup_state.app.config['TINYURL_URL'],
                timeout=setup_state.app.config.get('TINYURL_REQUEST_TIMEOUT_SECONDS'),
            ),
        }

    @classmethod
    def parse_request_json(cls, json: Mapping) -> ShortenersRequest:
        try:
            return ShortenersRequest(**json)
        except pydantic.ValidationError as e:
            logger.info('%s. Received invalid request. Body: %s', cls.__name__, json)
            logger.info('%s. Validation error: %s', cls.__name__, e)
            raise APIValidationError(errors=e.errors())

    @classmethod
    def get_short_link(cls, shortener: shorteners.RequestBasedShortener, provider_name: str, long_link: str) -> str:
        try:
            short_link = shortener.shorten(long_link)
        except shortener_exceptions.ShorteningProviderTimeout:
            exception_to_raise = flask_exceptions.GatewayTimeout
        except shortener_exceptions.ShorteningProviderRequestException:
            exception_to_raise = flask_exceptions.BadGateway
        else:
            logger.info('%s. Successfully shortened link. Provider: %s', cls.__name__, provider_name)
            logger.debug('%s. Shortening: %s -> %s', cls.__name__, long_link, short_link)
            return short_link

        logger.exception('An error occurred while calling shortening provider. Provider: %s', provider_name)
        raise exception_to_raise

    @classmethod
    def post(cls) -> Response:
        request = cls.parse_request_json(flask_request.json)
        logger.debug('%s. Received request. Body: %s', cls.__name__, flask_request.json)

        short_link = cls.get_short_link(
            shortener=cls._provider_shortener_mapping[request.provider],
            provider_name=request.provider,
            long_link=request.url,
        )
        response_data = ShortenersResponse(
            url=request.url,
            link=short_link,
        )
        response = jsonify(response_data.dict())
        logger.debug('%s. Prepared response: %s', cls.__name__, response.data)

        return response


blueprint.record(ShortlinksAPI.init_provider_shorter_mapping)
blueprint.add_url_rule('/shortlinks', view_func=ShortlinksAPI.as_view('shortlinks'))
