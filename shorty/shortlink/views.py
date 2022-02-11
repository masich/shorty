import logging
from typing import Mapping

import pydantic
from flasgger import swag_from
from flask import blueprints, jsonify, Response, request as flask_request
from flask.views import MethodView
from werkzeug import exceptions as flask_exceptions

from shorty import utils
from shorty.shortlink import shorteners, schemas
from shorty.shortlink.exceptions import APIValidationError
from shorty.shortlink.shorteners import exceptions as shortener_exceptions

__all__ = (
    'blueprint',
    'ShortlinksAPI',
)

logger = logging.getLogger(__name__)

blueprint = blueprints.Blueprint('shortlink', __name__)

_shorteners_mapping: dict[str, shorteners.Shortener] = {}


def load_shorteners(setup_state: blueprints.BlueprintSetupState) -> None:
    """
    Initialise mapping includes all available shortening providers.
    Must be invoked oly after initialisation of the `Flask` application.
    """
    _shorteners_mapping.update({
        name: utils.dynamically_load(shortener_config['class_path'])(**shortener_config['kwargs'])
        for name, shortener_config in setup_state.app.config['SHORTENERS'].items()
    })
    schemas.init_schemas(_shorteners_mapping.keys())


class ShortlinksAPI(MethodView):
    @classmethod
    def parse_request_json(cls, json: Mapping) -> schemas.ShortlinksRequest:
        try:
            return schemas.ShortlinksRequest(**json)
        except pydantic.ValidationError as e:
            logger.info('%s. Received invalid request. Body: %s', cls.__name__, json)
            logger.info('%s. Validation error: %s', cls.__name__, e)
            raise APIValidationError(errors=e.errors())

    @classmethod
    def _get_short_link(cls, long_link: str, shortener: shorteners.Shortener) -> str:
        try:
            logger.info('%s. Trying to shorten using %s', cls.__name__, shortener.__class__.__name__)
            logger.debug('%s. Long link: %s', cls.__name__, long_link)
            short_link = shortener.shorten(long_link)
        except shortener_exceptions.ShorteningProviderTimeout:
            exception_to_raise = flask_exceptions.GatewayTimeout
        except shortener_exceptions.ShorteningProviderRequestException:
            exception_to_raise = flask_exceptions.BadGateway
        else:
            logger.info('%s. The link has been successfully shortened.', cls.__name__)
            logger.debug('%s. Shortened: %s -> %s', cls.__name__, long_link, short_link)
            return short_link

        logger.exception('An error occurred during shortening')
        raise exception_to_raise

    @classmethod
    def get_short_link(cls, long_link: str, shortener: shorteners.Shortener, *fallback_shorteners) -> str:
        for shortener in shortener, *fallback_shorteners:
            try:
                return cls._get_short_link(long_link, shortener)
            except Exception as e:
                last_exception = e

        raise last_exception

    @classmethod
    @swag_from('shortlinks.yml')
    def post(cls) -> Response:
        request = cls.parse_request_json(flask_request.json)
        logger.debug('%s. Received request. Body: %s', cls.__name__, flask_request.json)
        logger.info('%s. Provider name from request: %s.', cls.__name__, request.provider)

        if request.provider:
            short_link = cls.get_short_link(request.url, shortener=_shorteners_mapping[request.provider])
        else:
            logger.info('%s. Trying to shorten using all shorteners.', cls.__name__)
            short_link = cls.get_short_link(request.url, *_shorteners_mapping.values())

        response_data = schemas.ShortlinksResponse(url=request.url, link=short_link)
        response = jsonify(response_data.dict())
        logger.debug('%s. Prepared response: %s', cls.__name__, response.data)

        return response


blueprint.record(load_shorteners)
blueprint.add_url_rule('/shortlinks', view_func=ShortlinksAPI.as_view('shortlinks'))
