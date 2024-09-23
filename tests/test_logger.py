import pytest
import logging
from app import logger
from unittest.mock import MagicMock, patch, call


def test_get_logger():
    test_logger = logger.get_logger(__name__)
    assert test_logger.name == "tests.test_logger"
    assert len(test_logger.handlers) == 1


@patch("logging.StreamHandler")
@patch("logging.getLogger")
def test_set_uvicorn_loggers(
    mock_get_logger: MagicMock, mock_uvicorn_handler: MagicMock
):
    mock_logger_uvicorn_access = MagicMock()
    logger_uvicorn_error = MagicMock()
    mock_get_logger.side_effect = [mock_logger_uvicorn_access, logger_uvicorn_error]

    logger.set_uvicorn_loggers()

    mock_uvicorn_handler().setLevel.assert_called_once_with(logging.INFO)
    mock_uvicorn_handler().setFormatter.assert_called_once_with(logger.formatter)
    mock_get_logger.assert_has_calls([call("uvicorn.access"), call("uvicorn.error")])
    mock_logger_uvicorn_access.handlers.clear.assert_called_once_with()
    mock_logger_uvicorn_access.addHandler.assert_called_once_with(
        mock_uvicorn_handler()
    )
    assert not logger_uvicorn_error.propagate
    logger_uvicorn_error.addHandler.assert_called_once_with(mock_uvicorn_handler())
