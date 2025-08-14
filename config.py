"""
Configuration management for GitHub Models GPT API
"""

import os
from typing import Optional

class Config:
    """Configuration class for the API"""
    
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        """Load configuration from environment variables"""
        # Try to load from .env file if available
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
        
        # Core settings
        self.github_token: Optional[str] = os.getenv('GITHUB_TOKEN')
        self.port: int = int(os.getenv('PORT', 5000))
        self.debug: bool = os.getenv('DEBUG', 'False').lower() == 'true'
        self.log_level: str = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # GitHub Models API settings
        self.github_models_base_url: str = os.getenv(
            'GITHUB_MODELS_BASE_URL', 
            'https://models.inference.ai.azure.com'
        )
        
        # Default model settings
        self.default_model: str = os.getenv('DEFAULT_MODEL', 'gpt-4o')
        self.default_max_tokens: int = int(os.getenv('DEFAULT_MAX_TOKENS', 1000))
        self.default_temperature: float = float(os.getenv('DEFAULT_TEMPERATURE', 0.7))
    
    def is_valid(self) -> bool:
        """Check if the configuration is valid"""
        return self.github_token is not None and len(self.github_token.strip()) > 0
    
    def get_github_headers(self) -> dict:
        """Get headers for GitHub API requests"""
        return {
            'Authorization': f'Bearer {self.github_token}',
            'Content-Type': 'application/json'
        }

# Global config instance
config = Config()