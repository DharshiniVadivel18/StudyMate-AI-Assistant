"""
Configuration settings for StudyMate
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for StudyMate application"""
    
    # Application settings
    APP_NAME = "StudyMate"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Demo mode (uses simulated responses instead of real AI)
    DEMO_MODE = os.getenv("DEMO_MODE", "True").lower() == "true"
    
    # File upload settings
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    ALLOWED_EXTENSIONS = ['.pdf']
    UPLOAD_FOLDER = Path("temp_uploads")
    
    # AI Model settings
    MODEL_NAME = os.getenv("MODEL_NAME", "ibm/granite-3b-code-instruct")
    EMBEDDING_DIMENSION = 384
    
    # Search settings
    MAX_SEARCH_RESULTS = 10
    DEFAULT_CONFIDENCE_THRESHOLD = 0.7
    DEFAULT_TEMPERATURE = 0.7
    
    # Chunking settings
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
    
    # Session settings
    SESSION_TIMEOUT_MINUTES = 60
    MAX_QA_HISTORY = 50
    
    # UI settings
    THEME_COLOR = "#667eea"
    SECONDARY_COLOR = "#764ba2"
    
    # Export settings
    EXPORT_FORMATS = ["pdf", "csv", "json"]
    
    # IBM Watsonx settings
    IBM_API_KEY = os.getenv("IBM_API_KEY")
    IBM_PROJECT_ID = os.getenv("IBM_PROJECT_ID")
    IBM_BASE_URL = os.getenv("IBM_BASE_URL", "https://us-south.ml.cloud.ibm.com")
    
    def __init__(self):
        """Initialize configuration"""
        # Create upload folder if it doesn't exist
        self.UPLOAD_FOLDER.mkdir(exist_ok=True)
    
    @property
    def is_demo_mode(self) -> bool:
        """Check if running in demo mode"""
        return self.DEMO_MODE
    
    @property
    def max_file_size_bytes(self) -> int:
        """Get max file size in bytes"""
        return self.MAX_FILE_SIZE_MB * 1024 * 1024
    
    @property
    def has_ibm_credentials(self) -> bool:
        """Check if IBM credentials are available"""
        return bool(self.IBM_API_KEY and self.IBM_PROJECT_ID)

# Global configuration instance
config = Config()
