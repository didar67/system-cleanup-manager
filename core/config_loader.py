import yaml
import os

def load_config(config_path: str) -> dict:
    """
    Load and validate YAML configuration file.

    :param config_path: Path to the YAML config file.
    :return: Configuration dictionary.
    :raises FileNotFoundError: If the file does not exist.
    :raises KeyError: If required keys are missing.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file {config_path} not found.")

    # Load YAML content into a dictionary
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Ensure all required configuration keys are present
    required_keys = [
        'log_file', 'log_level', 'cleanup_paths',
        'dry_run', 'extensions', 'older_than_days', 'exclude'
        ]
    for key in required_keys:
        if key not in config:
            raise KeyError(f"Missing required config key: {key}")

    return config
