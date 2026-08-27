"""Configuration management"""

import os
from dotenv import load_dotenv

load_dotenv()


def load_config():
    """
    Load configuration from environment variables
    
    Returns:
        dict: Configuration dictionary
    """
    return {
        'username': os.getenv('SNAPCHAT_USERNAME'),
        'password': os.getenv('SNAPCHAT_PASSWORD'),
        'rate_limit': float(os.getenv('RATE_LIMIT', '1.0')),
        'retry_attempts': int(os.getenv('RETRY_ATTEMPTS', '3')),
        'timeout': int(os.getenv('TIMEOUT', '30')),
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'output_dir': os.getenv('OUTPUT_DIR', 'reports'),
        'log_file': os.getenv('LOG_FILE', 'reports/mass_reporter.log'),
    }


def validate_config(config):
    """
    Validate configuration
    
    Args:
        config (dict): Configuration dictionary
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not config.get('username'):
        return False, 'SNAPCHAT_USERNAME not set'
    if not config.get('password'):
        return False, 'SNAPCHAT_PASSWORD not set'
    if config.get('rate_limit', 0) < 0:
        return False, 'RATE_LIMIT must be >= 0'
    if config.get('retry_attempts', 0) < 0:
        return False, 'RETRY_ATTEMPTS must be >= 0'
    
    return True, None
