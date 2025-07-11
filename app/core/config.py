import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    
    # Azure OpenAI Configuration
    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "")
    azure_openai_deployment_name: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
    
    # Default system prompt for the agent
    default_system_prompt: str = """You are an AI image analyzer. Your task is to analyze 
    the provided image based on the user's prompt. Be objective, detailed, and informative 
    in your analysis. If no image is provided, you should gracefully handle text-only 
    queries while noting the absence of an image."""

# Global instance to be imported and used across the app
settings = Settings()
