import os
from core.config_loader import load_config
from core.logger import get_logger
from core.cleaner import SystemCleaner

def main():
    """
    Main entry point for the cleanup tool.
    Loads configuration, confirms with user, initializes and runs the cleaner.
    """
    config_path = os.getenv('CLEANER_CONFIG', 'config/config.yaml')
    config = load_config(config_path)  # Load config from YAML

    logger = get_logger(config['log_file'], config.get('log_level', 'INFO'))  # Setup logger

    # Ask for confirmation before performing deletions (if not dry run)
    if not config.get('dry_run', False):
        confirm = input("\u26a0\ufe0f Are you sure you want to delete files? [y/N]: ")
        if confirm.lower() != 'y':
            print("\u274c Cleanup cancelled.")
            return

    # Initialize cleaner with config values
    cleaner = SystemCleaner(
        paths=config['cleanup_paths'],
        logger=logger,
        dry_run=config['dry_run'],
        extensions=config['extensions'],
        older_than_days=config['older_than_days'],
        exclude=config['exclude']
    )
    cleaner.clean()  # Run the cleaner

if __name__ == "__main__":
    main()