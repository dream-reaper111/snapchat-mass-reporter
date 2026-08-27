"""Main reporter class for Snapchat mass reporting"""

import time
import requests
from typing import List, Dict, Any
from src.logger import setup_logger
from src.snapchat_api import SnapchatAPI

logger = setup_logger(__name__)


class SnapchatMassReporter:
    """
    Main class for handling mass reporting on Snapchat
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the reporter
        
        Args:
            config (dict): Configuration dictionary
        """
        self.config = config
        self.api = SnapchatAPI(config)
        self.stats = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
        }
    
    def report_targets(self, targets: List[str], report_type: str, 
                      delay: float = 1.0, dry_run: bool = False) -> Dict[str, int]:
        """
        Report multiple targets
        
        Args:
            targets (list): List of target usernames/IDs
            report_type (str): Type of report (spam, abuse, etc.)
            delay (float): Delay between reports in seconds
            dry_run (bool): If True, don't actually send reports
            
        Returns:
            dict: Statistics of the operation
        """
        self.stats['total'] = len(targets)
        
        logger.info(f'Starting mass report campaign: {report_type}')
        logger.info(f'Total targets: {len(targets)}')
        logger.info(f'Delay between reports: {delay}s')
        
        for idx, target in enumerate(targets, 1):
            try:
                logger.info(f'[{idx}/{len(targets)}] Processing: {target}')
                
                if dry_run:
                    logger.info(f'[DRY RUN] Would report {target} for {report_type}')
                    self.stats['successful'] += 1
                else:
                    success = self.api.report_user(target, report_type)
                    if success:
                        self.stats['successful'] += 1
                        logger.info(f'✓ Successfully reported: {target}')
                    else:
                        self.stats['failed'] += 1
                        logger.warning(f'✗ Failed to report: {target}')
                
                # Apply delay between requests
                if idx < len(targets):
                    time.sleep(delay)
            
            except Exception as e:
                self.stats['failed'] += 1
                logger.error(f'Error reporting {target}: {str(e)}')
        
        logger.info('Mass report campaign completed')
        return self.stats
    
    def print_statistics(self, stats: Dict[str, int]) -> None:
        """
        Print operation statistics
        
        Args:
            stats (dict): Statistics dictionary
        """
        logger.info(f'\n' + '='*50)
        logger.info('CAMPAIGN STATISTICS')
        logger.info(f'{'='*50}')
        logger.info(f'Total targets: {stats["total"]}')
        logger.info(f'Successful: {stats["successful"]} ({stats["successful"]/stats["total"]*100:.1f}%)')
        logger.info(f'Failed: {stats["failed"]} ({stats["failed"]/stats["total"]*100:.1f}%)')
        logger.info(f'Skipped: {stats["skipped"]}')
        logger.info('='*50)
