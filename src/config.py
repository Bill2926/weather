import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """Application configuration"""
    
    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.base_url = os.getenv('WEATHER_API_BASE_URL')
        self.daily_url = os.getenv('METEO_WEATHER_API_BASE_URL')
        self.geocoding_url = os.getenv('GEO_CODING_API_BASE_URL')
        
        # Validate
        if not self.api_key:
            raise ValueError("WEATHER_API_KEY not found in .env file")
    
    @classmethod
    def load(cls):
        """Factory method to load config"""
        return cls()