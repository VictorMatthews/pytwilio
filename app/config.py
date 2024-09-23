import dotenv
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class Settings(BaseSettings):
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_messaging_service_sid: str


settings = Settings()
