import math
from app.config import settings
from app.logger import get_logger
from app.model.twilio_message import TwilioMessage
from twilio.rest import Client
from typing import Dict, Optional

logger = get_logger(__name__)
client = Client(settings.twilio_account_sid, settings.twilio_auth_token)


def send_message(twilio_message: Optional[TwilioMessage] = None) -> None:
    """Attempt to send the message via twilio"""
    if twilio_message == None:
        logger.info("No message passed in, cannot send")
        return

    for number in twilio_message.numbers:
        number = format_number(number)
        if not is_valid_number(number):
            logger.info(f"Invalid U.S. number, will not send to {number}")
            continue

        message_instance = client.messages.create(
            messaging_service_sid=settings.twilio_messaging_service_sid,
            to=number,
            body=twilio_message.message,
        )
        logger.info(f"Message sent: {message_instance.sid}")


def is_valid_number(number: str) -> bool:
    """Validate the passed in number"""
    # Passed in number should have been formatted and start with +1
    if len(number) != 12:
        return False
    if not number[2:].isnumeric():
        return False
    return True


def format_number(number: str) -> str:
    """Convert (012) 345-6789 to +10123456789"""
    # Should not be more 17 characters '+1 (012) 345-6789', but allow some room for extra spaces
    if len(number) > 20:
        return number

    # Strip know formatting characters
    number = number.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
    if number.startswith("+1"):
        return number

    return f"+1{number}"
