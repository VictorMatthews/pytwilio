from app.logger import get_logger
from app.model.twilio_message import TwilioMessage
from app.services import twilio
from fastapi import APIRouter
from typing import Dict, Optional

router = APIRouter()


@router.get("/")
def health() -> Dict[str, str]:
    """Health check to verify app is running"""
    return {"health": "up"}


@router.post("/message")
def post_message(twilio_message: Optional[TwilioMessage]) -> None:
    """Post endpoint for sending a message via twilio"""
    twilio.send_message(twilio_message)
