#!/usr/bin/env python3
"""
Snapchat Mass Reporter - Main entry point
"""

import sys
import click
from src.reporter import SnapchatMassReporter
from src.config import load_config
from src.logger import setup_logger

logger = setup_logger(__name__)


@click.group()
def cli():
    """Snapchat Mass Reporter CLI"""
    pass


@cli.command()
@click.option('--targets', '-t', required=True, help='Path to targets file')
@click.option('--report-type', '-r', default='spam', help='Type of report')
@click.option('--delay', '-d', default=1.0, help='Delay between reports (seconds)')
@click.option('--dry-run', is_flag=True, help='Dry run mode')
def report(targets, report_type, delay, dry_run):
    """Start mass reporting campaign"""
    try:
        config = load_config()
        reporter = SnapchatMassReporter(config)
        
        click.echo(click.style('\n🚀 Snapchat Mass Reporter', fg='cyan', bold=True))
        click.echo(click.style('=' * 50, fg='cyan'))
        
        with open(targets, 'r') as f:
            target_list = [line.strip() for line in f if line.strip()]
        
        click.echo(f'Loaded {len(target_list)} targets')
        click.echo(f'Report type: {report_type}')
        click.echo(f'Delay: {delay}s')
        
        if dry_run:
            click.echo(click.style('\n⚠️  DRY RUN MODE - No actual reports will be sent', fg='yellow'))
        
        if click.confirm('\nProceed?'):
            stats = reporter.report_targets(target_list, report_type, delay, dry_run)
            reporter.print_statistics(stats)
        else:
            click.echo('Cancelled.')
    
    except FileNotFoundError:
        click.echo(click.style(f'Error: File not found - {targets}', fg='red'), err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f'Error: {str(e)}', fg='red'), err=True)
        sys.exit(1)


@cli.command()
@click.option('--input', '-i', required=True, help='Input targets file')
@click.option('--output', '-o', default='cleaned_targets.txt', help='Output file')
def validate(input, output):
    """Validate and clean targets file"""
    try:
        from src.utils import validate_targets
        valid, invalid = validate_targets(input, output)
        
        click.echo(click.style(f'\n✓ Valid targets: {valid}', fg='green'))
        click.echo(click.style(f'✗ Invalid targets: {invalid}', fg='red'))
        click.echo(f'\nCleaned targets saved to: {output}')
    
    except Exception as e:
        click.echo(click.style(f'Error: {str(e)}', fg='red'), err=True)
        sys.exit(1)


@cli.command()
def config():
    """Show current configuration"""
    try:
        cfg = load_config()
        click.echo(click.style('\n📋 Current Configuration', fg='cyan', bold=True))
        click.echo(click.style('=' * 50, fg='cyan'))
        for key, value in cfg.items():
            if 'password' in key.lower():
                value = '***' if value else None
            click.echo(f'{key}: {value}')
    
    except Exception as e:
        click.echo(click.style(f'Error: {str(e)}', fg='red'), err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
