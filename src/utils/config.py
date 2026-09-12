"""Configuration management"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Load and manage configuration"""

    def __init__(self, config_file: str = 'config/trading_config.yaml'):
        """Initialize configuration
        
        Args:
            config_file: Path to config file
        """
        load_dotenv()
        self.config = self._load_config(config_file)

    @staticmethod
    def _load_config(config_file: str) -> dict:
        """Load YAML configuration file
        
        Args:
            config_file: Path to config file
            
        Returns:
            Configuration dictionary
        """
        if Path(config_file).exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}

    def get(self, key: str, default=None):
        """Get configuration value
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def get_env(self, key: str, default=None):
        """Get environment variable
        
        Args:
            key: Environment variable name
            default: Default value
            
        Returns:
            Environment variable value
        """
        return os.getenv(key, default)
