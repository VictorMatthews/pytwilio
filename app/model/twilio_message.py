from typing import List, Optional
from pydantic import BaseModel


class TwilioMessage(BaseModel):
    message: Optional[str] = None
    numbers: List[str] = []
