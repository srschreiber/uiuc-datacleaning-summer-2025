from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    """
    Configuration settings for the application.
    """
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_endpoint: str = Field(..., env="OPENAI_ENDPOINT")
    openai_model: str = Field(..., env="OPENAI_MODEL")
    openai_version: str = Field("2024-05-01-preview", env="OPENAI_VERSION")

config = Config()
