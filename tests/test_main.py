import pytest
from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch


@pytest.mark.asyncio
@patch("app.main.set_uvicorn_loggers")
async def test_set_uvicorn_loggers_at_startup(mock_set_uvicorn_loggers: MagicMock):
    with TestClient(app=app) as client:
        mock_set_uvicorn_loggers.assert_called_once_with()
