import logging
from typing import Any, Mapping

from dotenv import load_dotenv
from flask import Flask

from shorty.error_handlers import error_handlers
from shorty.shortlink.views import blueprint as shortlink_bp

__all__ = (
    'create_app',
)

DEFAULT_CONFIG = 'shorty.config.AppConfig'
DOTENV_PATH = '.env'


def create_app(settings_overrides: Mapping[str, Any] | None = None) -> Flask:
    """
    Create and configure `Flask` application.

    :param: settings_overrides: Mapping to override `Flask` application config.
    :param: import_name: `Flask` application name.
    """
    load_dotenv(DOTENV_PATH)
    app = Flask(__name__)
    configure_settings(app, settings_overrides=settings_overrides)
    configure_logging(app)
    configure_blueprints(app)
    configure_error_handlers(app)

    return app


def configure_logging(app: Flask) -> None:
    level = logging.getLevelName(app.config.get('LOGGING_LEVEL'))
    app.logger.setLevel(level)
    logging.basicConfig(level=level)


def configure_settings(app: Flask, settings_overrides: Mapping[str, Any] | None) -> None:
    app.config.from_object(DEFAULT_CONFIG)

    if settings_overrides:
        app.config.update(settings_overrides)


def configure_blueprints(app: Flask) -> None:
    app.register_blueprint(shortlink_bp)


def configure_error_handlers(app: Flask) -> None:
    for exception_type, error_handler in error_handlers.items():
        app.register_error_handler(exception_type, error_handler)
