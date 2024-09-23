import pytest
from app.main import app
from app.model.twilio_message import TwilioMessage
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

client = TestClient(app=app)


def test_get_health():
    result = client.get("/")
    assert result.status_code == 200


@patch("app.services.twilio.send_message")
def test_post_message(mock_send_message: MagicMock):
    fake_twilio_message = {
        "message": "Some fake message to test",
        "numbers": ["Some", "list", "of", "fake", "numbers"],
    }
    result = client.post(url="/message", json=fake_twilio_message)
    assert result.status_code == 200
    mock_send_message.assert_called_once_with(TwilioMessage(**fake_twilio_message))
