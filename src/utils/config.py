"""Configuration management for the trading system."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv


class Config:
    """Configuration manager with environment variable support."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Path to YAML config file. Defaults to config/config.yaml
        """
        # Load environment variables
        load_dotenv()
        
        # Determine config path
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
        else:
            config_path = Path(config_path)
        
        # Load YAML configuration
        with open(config_path, "r") as f:
            self._config = yaml.safe_load(f)
        
        # Substitute environment variables
        self._substitute_env_vars(self._config)
    
    def _substitute_env_vars(self, obj: Any) -> None:
        """Recursively substitute environment variables in config.
        
        Args:
            obj: Configuration object to process
        """
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                    env_var = value[2:-1]
                    obj[key] = os.getenv(env_var, value)
                else:
                    self._substitute_env_vars(value)
        elif isinstance(obj, list):
            for item in obj:
                self._substitute_env_vars(item)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., "binance.api_key")
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section.
        
        Args:
            section: Section name
            
        Returns:
            Configuration section as dictionary
        """
        return self._config.get(section, {})
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access."""
        return self.get(key)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Config({self._config})"

