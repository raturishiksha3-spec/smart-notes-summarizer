import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_APP = os.getenv('FLASK_APP', 'app.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Database settings
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'smart_notes.db')
    
    # Model settings
    SUMMARIZATION_MODEL = os.getenv('SUMMARIZATION_MODEL', 'facebook/bart-large-cnn')
    QA_MODEL = os.getenv('QA_MODEL', 't5-base')
    MAX_CHUNK_SIZE = int(os.getenv('MAX_CHUNK_SIZE', 1024))
    
    # File upload settings
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    
    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    
    # Summarization settings
    SUMMARY_LENGTH_PARAMS = {
        'short': {'max_length': 100, 'min_length': 30},
        'medium': {'max_length': 200, 'min_length': 50},
        'detailed': {'max_length': 400, 'min_length': 100}
    }
    
    # Text validation
    MIN_TEXT_WORDS = int(os.getenv('MIN_TEXT_WORDS', 50))
    MAX_TEXT_WORDS = int(os.getenv('MAX_TEXT_WORDS', 10000))
    
    # Q&A generation settings
    MAX_QA_PAIRS = int(os.getenv('MAX_QA_PAIRS', 5))
    
    # Cache settings
    ENABLE_MODEL_CACHE = os.getenv('ENABLE_MODEL_CACHE', 'true').lower() == 'true'
    CACHE_DIR = os.getenv('CACHE_DIR', '.cache')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Use stronger secret key in production
    if Config.SECRET_KEY == 'dev-secret-key-change-in-production':
        raise ValueError("SECRET_KEY must be set in production!")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_PATH = ':memory:'  # Use in-memory database for tests

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])