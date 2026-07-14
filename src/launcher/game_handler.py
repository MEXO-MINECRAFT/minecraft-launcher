"""Spielstart und Monitoring"""
import subprocess
import time
from pathlib import Path
from typing import Optional, Callable
from threading import Thread
from src.utils.logger import logger
from src.launcher.versions import MinecraftVersion
from src.auth.login import UserProfile


class GameProcess:
    """Verwaltet den Spielprozess"""
    
    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.is_running: bool = False
        self.start_time: float = 0
        self.on_stop_callback: Optional[Callable] = None
    
    def start_game(
        self,
        version: MinecraftVersion,
        user: UserProfile,
        java_path: str,
        ram_gb: int
    ) -> bool:
        """Startet Minecraft"""
        try:
            # RAM in MB
            ram_mb = ram_gb * 1024
            
            # Kommandozeile für Spielstart
            cmd = [
                java_path,
                f"-Xmx{ram_mb}M",
                f"-Xms{ram_mb // 2}M",
                "-XX:+UnlockExperimentalVMOptions",
                "-XX:G1NewCollectionPercentage=20",
                "-XX:G1ReservePercent=5",
                "-XX:InitiatingHeapOccupancyPercent=15",
                "-XX:G1HeapRegionSize=16M",
                "-XX:MinMetaspaceExpansion=21807104",
                "-XX:MaxMetaspaceExpansion=352321536",
                "-Dfile.encoding=UTF-8",
                "-Duser.country=DE",
                "-Duser.language=de",
                "-cp",
                "minecraft.jar",
                "net.minecraft.client.main.Main",
                "--username", user.username,
                "--version", version.version,
                "--gameDir", ".minecraft",
                "--assetsDir", ".minecraft/assets"
            ]
            
            logger.info(f"🎮 Starte Minecraft {version.version}...")
            logger.info(f"👤 Spieler: {user.username}")
            logger.info(f"💾 RAM: {ram_gb}GB")
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.is_running = True
            self.start_time = time.time()
            
            # Starte Monitoring in separatem Thread
            monitor_thread = Thread(target=self._monitor_process, daemon=True)
            monitor_thread.start()
            
            logger.info("✓ Minecraft erfolgreich gestartet")
            return True
        
        except Exception as e:
            logger.error(f"✗ Fehler beim Starten von Minecraft: {e}")
            self.is_running = False
            return False
    
    def _monitor_process(self):
        """Überwacht den Spielprozess"""
        if not self.process:
            return
        
        self.process.wait()
        self.is_running = False
        
        runtime = time.time() - self.start_time
        hours = int(runtime // 3600)
        minutes = int((runtime % 3600) // 60)
        seconds = int(runtime % 60)
        
        logger.info(
            f"🛑 Minecraft beendet. Spielzeit: {hours}h {minutes}m {seconds}s"
        )
        
        if self.on_stop_callback:
            self.on_stop_callback()
    
    def stop_game(self):
        """Beendet das Spiel"""
        if self.process and self.is_running:
            try:
                self.process.terminate()
                logger.info("⏹️ Minecraft Beendigung angefordert")
            except Exception as e:
                logger.error(f"✗ Fehler beim Beenden: {e}")
    
    def is_game_running(self) -> bool:
        """Prüft ob Spiel läuft"""
        return self.is_running
    
    def get_runtime(self) -> float:
        """Gibt Spiellaufzeit in Sekunden zurück"""
        if self.is_running:
            return time.time() - self.start_time
        return 0.0


class GameMonitor:
    """Überwacht Performance während des Spiels"""
    
    def __init__(self):
        self.fps: int = 0
        self.ram_used: float = 0
        self.cpu_used: float = 0
    
    def update_stats(self, fps: int, ram_gb: float, cpu: float):
        """Aktualisiert Statistiken (würde durch echtes Parsing erfolgen)"""
        self.fps = fps
        self.ram_used = ram_gb
        self.cpu_used = cpu
    
    def get_stats(self) -> dict:
        """Gibt aktuelle Statistiken zurück"""
        return {
            'fps': self.fps,
            'ram_gb': self.ram_used,
            'cpu': self.cpu_used
        }
