"""Logging configuration"""

import logging
import os
from logging.handlers import RotatingFileHandler
from src.config import load_config


def setup_logger(name):
    """
    Setup logger with file and console handlers
    
    Args:
        name (str): Logger name
        
    Returns:
        logging.Logger: Configured logger
    """
    config = load_config()
    log_level = config.get('log_level', 'INFO')
    log_file = config.get('log_file')
    output_dir = config.get('output_dir')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler
    if log_file:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, log_level))
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    logger.addHandler(console_handler)
    
    return logger
