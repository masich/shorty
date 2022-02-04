from typing import Iterable

from flask import Response
from werkzeug.exceptions import UnprocessableEntity

__all__ = (
    'APIValidationError',
)


class APIValidationError(UnprocessableEntity):
    """
    Custom API Exception to provide additional information about validation error.
    """
    name = 'ValidationError'
    description = 'Received request with invalid data'

    def __init__(self, description: str | None = None, response: Response | None = None, errors: Iterable[dict] = None):
        super(APIValidationError, self).__init__(description=description, response=response)
        self.errors = errors
