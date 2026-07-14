"""Konfigurationsmanager"""
import json
from pathlib import Path
from typing import Any, Dict, Optional
from src.utils.logger import logger


class ConfigManager:
    """Verwaltet die Launcher-Konfiguration"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config: Dict[str, Any] = {}
        self.load()
    
    def load(self):
        """Laden der Konfiguration aus JSON-Datei"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                logger.info(f"✓ Konfiguration geladen: {self.config_file}")
            else:
                logger.warning(f"Konfigurationsdatei nicht gefunden: {self.config_file}")
                self.config = {}
        except Exception as e:
            logger.error(f"✗ Fehler beim Laden der Konfiguration: {e}")
            self.config = {}
    
    def save(self):
        """Speichern der Konfiguration in JSON-Datei"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"✓ Konfiguration gespeichert")
        except Exception as e:
            logger.error(f"✗ Fehler beim Speichern der Konfiguration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Wert aus der Konfiguration abrufen"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """Wert in der Konfiguration setzen"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save()
    
    def get_all(self) -> Dict[str, Any]:
        """Gesamte Konfiguration abrufen"""
        return self.config.copy()


# Globale Config-Instanz
config = ConfigManager()
