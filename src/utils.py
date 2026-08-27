"""Utility functions"""

import re
from src.logger import setup_logger

logger = setup_logger(__name__)


def validate_username(username: str) -> bool:
    """
    Validate Snapchat username format
    
    Args:
        username (str): Username to validate
        
    Returns:
        bool: True if valid
    """
    # Snapchat usernames: 3-25 characters, alphanumeric + dots, underscores, hyphens
    pattern = r'^[a-zA-Z0-9._-]{3,25}$'
    return bool(re.match(pattern, username))


def validate_targets(input_file: str, output_file: str) -> tuple:
    """
    Validate and clean targets file
    
    Args:
        input_file (str): Path to input file
        output_file (str): Path to output file
        
    Returns:
        tuple: (valid_count, invalid_count)
    """
    valid_targets = []
    invalid_count = 0
    
    try:
        with open(input_file, 'r') as f:
            for line in f:
                target = line.strip()
                if target and validate_username(target):
                    valid_targets.append(target)
                elif target:
                    invalid_count += 1
                    logger.warning(f'Invalid target: {target}')
        
        # Write cleaned targets
        with open(output_file, 'w') as f:
            f.write('\n'.join(valid_targets))
        
        logger.info(f'Validated {len(valid_targets)} targets, {invalid_count} invalid')
        return len(valid_targets), invalid_count
    
    except FileNotFoundError:
        logger.error(f'File not found: {input_file}')
        raise
    except Exception as e:
        logger.error(f'Error validating targets: {str(e)}')
        raise


def batch_list(items: list, batch_size: int) -> list:
    """
    Split list into batches
    
    Args:
        items (list): List to batch
        batch_size (int): Size of each batch
        
    Returns:
        list: List of batches
    """
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
