import pytest
from app.services import twilio
from app.model.twilio_message import TwilioMessage
from unittest.mock import MagicMock, patch


def test_send_message():
    mock_logger = MagicMock()
    twilio.logger = mock_logger
    mock_client = MagicMock()
    mock_message_instance = MagicMock()
    mock_message_instance.sid = "fake_message_instance_sid"
    mock_client.messages.create.return_value = mock_message_instance
    twilio.client = mock_client
    twilio_message = TwilioMessage(
        message="Testing send message", numbers=["(012) 345-6789"]
    )

    twilio.send_message(twilio_message)
    mock_client.messages.create.assert_called_once_with(
        messaging_service_sid="fake_twilio_messaging_service_sid",
        to="+10123456789",
        body="Testing send message",
    )
    mock_logger.info.assert_called_once_with("Message sent: fake_message_instance_sid")


def test_send_message_no_message():
    mock_logger = MagicMock()
    twilio.logger = mock_logger
    mock_client = MagicMock()
    twilio.client = mock_client

    twilio.send_message()

    mock_logger.info.assert_called_once_with("No message passed in, cannot send")
    mock_client.assert_not_called()


def test_send_message_invalid_message():
    mock_logger = MagicMock()
    twilio.logger = mock_logger
    mock_client = MagicMock()
    twilio.client = mock_client
    twilio_message = TwilioMessage(message="Testing send message", numbers=["1"])

    twilio.send_message(twilio_message)

    mock_logger.info.assert_called_once_with(
        "Invalid U.S. number, will not send to +11"
    )
    mock_client.assert_not_called()


def test_is_valid_number():
    number = "+10123456789"
    assert twilio.is_valid_number(number)


def test_is_valid_number_invalid_len():
    number = "some value longer than 12"
    assert not twilio.is_valid_number(number)


def test_is_valid_number_nan():
    number = "+1ABCDEFGHIJ"
    assert not twilio.is_valid_number(number)


def test_format_number():
    number = "(012) 345-6789"
    formatted_number = twilio.format_number(number)
    assert formatted_number == "+10123456789"


def test_format_number_len_too_large():
    number = "someone entered a really long value instead of a number"
    formatted_number = twilio.format_number(number)
    assert formatted_number == number


def test_format_number_starts_with_plus_one():
    number = " +1 (012) 345-6789  "
    formatted_number = twilio.format_number(number)
    assert formatted_number == "+10123456789"
