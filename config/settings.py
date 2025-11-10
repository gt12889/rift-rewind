"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Riot Games API
    riot_api_key: str = ""
    riot_api_base_url: str = "https://americas.api.riotgames.com"
    
    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    
    # AWS Bedrock
    bedrock_model_id: str = "anthropic.claude-v2"
    bedrock_region: str = "us-east-1"
    
    # Application
    app_env: str = "development"
    app_debug: bool = True
    api_port: int = 8000
    
    # Resource Tagging
    resource_tag_key: str = "rift-rewind-hackathon"
    resource_tag_value: str = "2025"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

