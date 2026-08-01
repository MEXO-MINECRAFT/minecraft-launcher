"""Minecraft Versionsmanagement mit echtem Mojang-Download"""
import json
import requests
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from pathlib import Path
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
    """Lädt echte Minecraft-Versionen von Mojang"""
    
    MOJANG_LAUNCHER_META = "https://launcher.mojang.com/v1/metadata/launcher"
    VERSION_MANIFEST = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    RESOURCE_BASE = "https://resources.download.minecraft.net"
    LIBRARIES_BASE = "https://libraries.minecraft.net"
    
    @staticmethod
    def get_version_manifest_from_mojang():
        """Holt das offizielle Version-Manifest von Mojang"""
        try:
            logger.info("📥 Lade Minecraft Version-Manifest von Mojang...")
            response = requests.get(VersionDownloader.VERSION_MANIFEST, timeout=10)
            if response.status_code == 200:
                logger.info("✅ Version-Manifest geladen")
                return response.json()
        except Exception as e:
            logger.warning(f"⚠️ Fehler beim Laden des Manifests: {e}")
        return None
    
    @staticmethod
    def download_version_json(version_name: str, minecraft_dir: Path) -> bool:
        """Lädt die version.json für eine Minecraft-Version"""
        try:
            manifest = VersionDownloader.get_version_manifest_from_mojang()
            if not manifest:
                return False
            
            # Finde die Version im Manifest
            version_info = None
            for version in manifest.get('versions', []):
                if version['id'] == version_name:
                    version_info = version
                    break
            
            if not version_info:
                logger.error(f"❌ Version {version_name} nicht in Manifest gefunden")
                return False
            
            # Lade version.json
            version_json_url = version_info['url']
            logger.info(f"📥 Lade version.json für {version_name}...")
            
            response = requests.get(version_json_url, timeout=10)
            if response.status_code != 200:
                logger.error(f"❌ Konnte version.json nicht laden")
                return False
            
            version_json = response.json()
            
            # Speichere version.json
            version_dir = minecraft_dir / "versions" / version_name
            version_dir.mkdir(parents=True, exist_ok=True)
            
            version_json_path = version_dir / f"{version_name}.json"
            with open(version_json_path, 'w') as f:
                json.dump(version_json, f, indent=2)
            
            logger.info(f"✅ version.json gespeichert")
            return True
            
        except Exception as e:
            logger.error(f"❌ Fehler beim Download von version.json: {e}")
            return False
    
    @staticmethod
    def download_minecraft_jar(version_name: str, minecraft_dir: Path) -> bool:
        """Lädt die minecraft.jar Datei"""
        try:
            version_dir = minecraft_dir / "versions" / version_name
            jar_file = version_dir / f"{version_name}.jar"
            
            # Wenn bereits vorhanden, skip
            if jar_file.exists():
                logger.info(f"✅ {version_name}.jar existiert bereits")
                return True
            
            # Lade version.json
            version_json_path = version_dir / f"{version_name}.json"
            if not version_json_path.exists():
                logger.error(f"❌ version.json nicht gefunden")
                return False
            
            with open(version_json_path, 'r') as f:
                version_json = json.load(f)
            
            # Extrahiere JAR download URL
            if 'downloads' not in version_json or 'client' not in version_json['downloads']:
                logger.error(f"❌ Keine JAR URL in version.json")
                return False
            
            jar_url = version_json['downloads']['client']['url']
            jar_size = version_json['downloads']['client'].get('size', 0)
            
            logger.info(f"📥 Lade minecraft.jar ({jar_size / (1024*1024):.1f}MB)...")
            
            response = requests.get(jar_url, stream=True, timeout=30)
            if response.status_code != 200:
                logger.error(f"❌ JAR Download fehlgeschlagen")
                return False
            
            # Speichere JAR mit Progress
            with open(jar_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"✅ minecraft.jar heruntergeladen")
            return True
            
        except Exception as e:
            logger.error(f"❌ Fehler beim JAR Download: {e}")
            return False
    
    @staticmethod
    def download_libraries(version_name: str, minecraft_dir: Path) -> bool:
        """Lädt erforderliche Java-Libraries herunter"""
        try:
            logger.info("📚 Lade Minecraft-Libraries...")
            
            version_dir = minecraft_dir / "versions" / version_name
            version_json_path = version_dir / f"{version_name}.json"
            
            if not version_json_path.exists():
                logger.error(f"❌ version.json nicht gefunden")
                return False
            
            with open(version_json_path, 'r') as f:
                version_json = json.load(f)
            
            libraries = version_json.get('libraries', [])
            libraries_dir = minecraft_dir / "libraries"
            libraries_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"📚 {len(libraries)} Libraries zu laden...")
            
            success_count = 0
            for i, lib in enumerate(libraries):
                try:
                    # Nur auf Windows relevante Libraries laden
                    rules = lib.get('rules', [])
                    if rules:
                        allowed = True
                        for rule in rules:
                            if rule.get('action') == 'disallow':
                                allowed = False
                        if not allowed:
                            continue
                    
                    if 'downloads' not in lib:
                        continue
                    
                    artifact = lib['downloads'].get('artifact')
                    if not artifact:
                        continue
                    
                    lib_url = artifact['url']
                    lib_path = artifact['path']
                    lib_size = artifact.get('size', 0)
                    
                    full_lib_path = libraries_dir / lib_path
                    full_lib_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    if full_lib_path.exists():
                        success_count += 1
                        continue
                    
                    if (i + 1) % 10 == 0:
                        logger.info(f"📚 Lade Library {i+1}/{len(libraries)}...")
                    
                    response = requests.get(lib_url, stream=True, timeout=10)
                    if response.status_code == 200:
                        with open(full_lib_path, 'wb') as f:
                            f.write(response.content)
                        success_count += 1
                
                except Exception as e:
                    logger.debug(f"⚠️ Library-Fehler: {e}")
                    continue
            
            logger.info(f"✅ {success_count}/{len(libraries)} Libraries geladen")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"❌ Fehler beim Library Download: {e}")
            return False
    
    @staticmethod
    def download_assets(version_name: str, minecraft_dir: Path) -> bool:
        """Lädt Minecraft-Assets herunter"""
        try:
            logger.info("🎨 Lade Minecraft-Assets...")
            
            version_dir = minecraft_dir / "versions" / version_name
            version_json_path = version_dir / f"{version_name}.json"
            
            if not version_json_path.exists():
                return False
            
            with open(version_json_path, 'r') as f:
                version_json = json.load(f)
            
            asset_index = version_json.get('assetIndex', {})
            asset_index_url = asset_index.get('url')
            
            if not asset_index_url:
                logger.warning("⚠️ Keine Asset-URL gefunden")
                return True
            
            logger.info(f"🎨 Lade Asset-Index...")
            response = requests.get(asset_index_url, timeout=10)
            if response.status_code != 200:
                logger.warning("⚠️ Asset-Index Download fehlgeschlagen")
                return True
            
            assets_json = response.json()
            assets_dir = minecraft_dir / "assets"
            objects_dir = assets_dir / "objects"
            objects_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"✅ Assets vorbereitet")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Fehler beim Asset Download: {e}")
            return True


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
        """Lädt die komplette Version von Mojang herunter"""
        if version.downloaded:
            logger.info(f"✅ {version.name} ist bereits vorhanden")
            return True
        
        logger.info(f"📥 Lade {version.name} von Mojang herunter...")
        
        # 1. Lade version.json
        if not self.downloader.download_version_json(version.version, self.minecraft_dir):
            return False
        
        # 2. Lade minecraft.jar
        if not self.downloader.download_minecraft_jar(version.version, self.minecraft_dir):
            return False
        
        # 3. Lade Libraries
        if not self.downloader.download_libraries(version.version, self.minecraft_dir):
            logger.warning("⚠️ Fehler bei Libraries, versuche trotzdem zu starten...")
        
        # 4. Lade Assets
        if not self.downloader.download_assets(version.version, self.minecraft_dir):
            logger.warning("⚠️ Fehler bei Assets, versuche trotzdem zu starten...")
        
        version.downloaded = True
        logger.info(f"✅ {version.name} bereit!")
        return True
