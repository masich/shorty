import pytest
from pytest_mock import MockerFixture
from werkzeug.exceptions import InternalServerError

from shorty import error_handlers
from shorty.shortlink.exceptions import APIValidationError


def _error_handler_1(*_, **__):
    pass


def _error_handler_2(*_, **__):
    pass


@pytest.fixture
def error_handlers_fixt() -> dict:
    return {}


@pytest.fixture
def internal_error() -> InternalServerError:
    return InternalServerError()


@pytest.fixture
def detailed_error() -> APIValidationError:
    return APIValidationError(errors=({'error': 'some_error_1'},))


@pytest.fixture
def generic_error() -> ValueError:
    return ValueError('Some error')


def test_add_error_handler(mocker: MockerFixture, error_handlers_fixt) -> None:
    mocker.patch.object(error_handlers, 'error_handlers', error_handlers_fixt)
    error_handlers.add_error_handler(Exception)(_error_handler_1)
    error_handlers.add_error_handler(ValueError)(_error_handler_2)

    assert len(error_handlers_fixt) == 2
    assert error_handlers_fixt[Exception] == _error_handler_1
    assert error_handlers_fixt[ValueError] == _error_handler_2


def test_http_error_handler(mocker: MockerFixture, internal_error) -> None:
    mock_jsonify = mocker.patch.object(error_handlers, 'jsonify')
    _, status_code = error_handlers.http_error_handler(internal_error)

    assert status_code == internal_error.code
    mock_jsonify.assert_called_once_with(
        {
            'name': internal_error.name,
            'description': internal_error.description,
        }
    )


def test_http_error_handler_detailed(mocker: MockerFixture, detailed_error) -> None:
    mock_jsonify = mocker.patch.object(error_handlers, 'jsonify')
    _, status_code = error_handlers.http_error_handler(detailed_error)

    assert status_code == detailed_error.code
    mock_jsonify.assert_called_once_with(
        {
            'name': detailed_error.name,
            'description': detailed_error.description,
            'errors': detailed_error.errors,
        }
    )


def test_generic_error_handler(mocker: MockerFixture, generic_error, internal_error, app) -> None:
    mock_jsonify = mocker.patch.object(error_handlers, 'jsonify')
    _, status_code = error_handlers.generic_error_handler(generic_error)

    assert status_code == internal_error.code
    mock_jsonify.assert_called_once_with(
        {
            'name': internal_error.name,
            'description': repr(generic_error),
        }
    )
