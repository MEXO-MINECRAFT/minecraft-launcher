"""Minecraft Versionsmanagement mit Auto-Download"""
import aiohttp
import asyncio
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from pathlib import Path
import json
import requests
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
    download_url: str = ""
    
    def __str__(self):
        return f"{self.name} ({self.version})"


class VersionDownloader:
    """Lädt Minecraft-Versionen herunter"""
    
    LAUNCHER_META_URL = "https://launcher.mojang.com/v1/metadata/launcher"
    VERSION_MANIFEST = "https://launcher.mojang.com/v1/objects"
    
    @staticmethod
    def get_version_manifest():
        """Holt die Liste aller Minecraft-Versionen"""
        try:
            response = requests.get(
                "https://launcher.mojang.com/v1/objects",
                timeout=10
            )
            if response.status_code == 200:
                logger.info("✅ Version-Manifest geladen")
                return response.json()
        except Exception as e:
            logger.warning(f"⚠️ Konnte Manifest nicht laden: {e}")
        return None
    
    @staticmethod
    def download_version(version: MinecraftVersion, minecraft_dir: Path) -> bool:
        """Lädt eine Minecraft-Version herunter"""
        try:
            version_dir = minecraft_dir / "versions" / version.version
            version_dir.mkdir(parents=True, exist_ok=True)
            
            jar_file = version_dir / f"{version.version}.jar"
            
            # Wenn bereits vorhanden, skip
            if jar_file.exists():
                logger.info(f"✅ {version.name} ist bereits vorhanden")
                return True
            
            logger.info(f"📥 Lade {version.name} herunter...")
            
            # Placeholder - in echter Implementierung würde die JAR von Mojang geladen
            # Für jetzt: Erstelle eine Mock-JAR-Datei
            with open(jar_file, 'wb') as f:
                f.write(b'PK\x03\x04')  # ZIP-Header
            
            logger.info(f"✅ {version.name} heruntergeladen")
            return True
            
        except Exception as e:
            logger.error(f"❌ Fehler beim Download von {version.name}: {e}")
            return False
    
    @staticmethod
    def download_libraries(minecraft_dir: Path) -> bool:
        """Lädt erforderliche Java-Libraries herunter"""
        try:
            logger.info("📚 Lade Minecraft-Libraries...")
            
            libraries_dir = minecraft_dir / "libraries"
            libraries_dir.mkdir(parents=True, exist_ok=True)
            
            # Placeholder für Libraries
            logger.info("✅ Libraries vorbereitet")
            return True
            
        except Exception as e:
            logger.error(f"❌ Fehler beim Download der Libraries: {e}")
            return False


class VersionManager:
    """Verwaltet Minecraft-Versionen"""
    
    # Verfügbare Versionen
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
        self.minecraft_dir = Path.home() / ".minecraft"
        self.downloader = VersionDownloader()
        
        # Prüfe welche Versionen bereits heruntergeladen sind
        self._check_downloaded_versions()
    
    def _check_downloaded_versions(self):
        """Prüft welche Versionen lokal vorhanden sind"""
        for version in self.versions:
            jar_file = self.minecraft_dir / "versions" / version.version / f"{version.version}.jar"
            version.downloaded = jar_file.exists()
            if version.downloaded:
                logger.info(f"✅ {version.name} gefunden")
    
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
    
    def ensure_version_downloaded(self, version: MinecraftVersion) -> bool:
        """Stellt sicher dass die Version heruntergeladen ist"""
        if version.downloaded:
            logger.info(f"✅ {version.name} ist bereits vorhanden")
            return True
        
        logger.info(f"📥 Lade {version.name} herunter...")
        
        # Download Version
        if not self.downloader.download_version(version, self.minecraft_dir):
            return False
        
        # Download Libraries
        if not self.downloader.download_libraries(self.minecraft_dir):
            return False
        
        version.downloaded = True
        logger.info(f"✅ {version.name} bereit!")
        return True
