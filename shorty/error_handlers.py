import logging
from typing import Callable, Type

from flask import Response, jsonify, current_app
from werkzeug.exceptions import HTTPException, InternalServerError

__all__ = (
    'error_handlers',
    'http_error_handler',
    'generic_error_handler',
)

logger = logging.getLogger(__name__)

error_handlers: dict[Type[Exception | int], Callable[[Exception], tuple[Response, int]]] = {}


def add_error_handler(code_or_exception: Type[Exception] | int):
    def wrapper(func: Callable[[Exception], tuple[Response, int]]):
        error_handlers[code_or_exception] = func
        return func

    return wrapper


@add_error_handler(Exception)
def generic_error_handler(exception: Exception) -> tuple[Response, int]:
    """
    Error handler for generic Exceptions.

    :param exception: Exception to handle.
    :return: Response and HTTP status code.
    """
    logger.exception(exception)
    http_exception = InternalServerError(
        original_exception=exception,
        description=repr(exception) if current_app.debug else None
    )

    return http_error_handler(http_exception)


@add_error_handler(HTTPException)
def http_error_handler(exception: HTTPException) -> tuple[Response, int]:
    error_payload = {
        'name': exception.name,
        'description': exception.description,
    }

    if hasattr(exception, 'errors'):
        error_payload['errors'] = exception.errors

    return jsonify(error_payload), exception.code
