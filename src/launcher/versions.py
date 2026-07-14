"""Minecraft Versionsmanagement"""
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from src.utils.logger import logger


class VersionType(Enum):
    """Versionstypen"""
    RELEASE = "release"
    SNAPSHOT = "snapshot"
    FORGE = "forge"
    FABRIC = "fabric"
    QUILT = "quilt"


@dataclass
class MinecraftVersion:
    """Minecraft Version"""
    name: str
    version: str
    type: VersionType
    release_date: str
    java_version: str = "17"
    downloaded: bool = False
    favorite: bool = False
    
    def __str__(self):
        return f"{self.name} ({self.version})"


class VersionManager:
    """Verwaltet Minecraft-Versionen"""
    
    # Beispiel-Versionen (später aus Mojang API laden)
    AVAILABLE_VERSIONS = [
        MinecraftVersion(
            name="Latest Release",
            version="1.20.4",
            type=VersionType.RELEASE,
            release_date="2023-12-07",
            java_version="17"
        ),
        MinecraftVersion(
            name="Minecraft 1.20.3",
            version="1.20.3",
            type=VersionType.RELEASE,
            release_date="2023-10-30",
            java_version="17"
        ),
        MinecraftVersion(
            name="Minecraft 1.20.1",
            version="1.20.1",
            type=VersionType.RELEASE,
            release_date="2023-08-02",
            java_version="17"
        ),
        MinecraftVersion(
            name="Latest Snapshot",
            version="1.21-pre1",
            type=VersionType.SNAPSHOT,
            release_date="2024-01-15",
            java_version="17"
        ),
        MinecraftVersion(
            name="Minecraft 1.19.2",
            version="1.19.2",
            type=VersionType.RELEASE,
            release_date="2022-08-05",
            java_version="16"
        ),
    ]
    
    def __init__(self):
        self.versions: List[MinecraftVersion] = self.AVAILABLE_VERSIONS.copy()
        self.selected_version: Optional[MinecraftVersion] = None
    
    def get_all_versions(self) -> List[MinecraftVersion]:
        """Gibt alle verfügbaren Versionen zurück"""
        return self.versions
    
    def get_releases(self) -> List[MinecraftVersion]:
        """Gibt nur Release-Versionen zurück"""
        return [v for v in self.versions if v.type == VersionType.RELEASE]
    
    def get_snapshots(self) -> List[MinecraftVersion]:
        """Gibt nur Snapshot-Versionen zurück"""
        return [v for v in self.versions if v.type == VersionType.SNAPSHOT]
    
    def get_favorites(self) -> List[MinecraftVersion]:
        """Gibt nur als Favoriten markierte Versionen zurück"""
        return [v for v in self.versions if v.favorite]
    
    def toggle_favorite(self, version: MinecraftVersion):
        """Markiert/entfernt Favorit"""
        for v in self.versions:
            if v.version == version.version:
                v.favorite = not v.favorite
                logger.info(f"Favorit {'hinzugefügt' if v.favorite else 'entfernt'}: {version.name}")
                break
    
    def set_selected_version(self, version: MinecraftVersion):
        """Setzt die ausgewählte Version"""
        self.selected_version = version
        logger.info(f"✓ Version ausgewählt: {version.name}")
    
    def get_selected_version(self) -> Optional[MinecraftVersion]:
        """Gibt die ausgewählte Version zurück"""
        return self.selected_version
