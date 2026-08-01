"""Spielstart und Monitoring"""
import subprocess
import time
import os
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
        """Startet Minecraft - ECHTE Version"""
        try:
            # RAM in MB
            ram_mb = ram_gb * 1024
            
            # Minecraft Verzeichnis
            minecraft_dir = Path.home() / ".minecraft"
            minecraft_dir.mkdir(exist_ok=True)
            
            logger.info(f"Minecraft wird gestartet: {version.version}")
            logger.info(f"Spieler: {user.username}")
            logger.info(f"RAM: {ram_gb}GB")
            
            # WICHTIG: Prüfe ob JAR existiert
            jar_file = minecraft_dir / "versions" / version.version / f"{version.version}.jar"
            
            if not jar_file.exists():
                logger.error(f"FEHLER: JAR nicht gefunden: {jar_file}")
                logger.error("Bitte warte bis der Download fertig ist!")
                return False
            
            logger.info(f"JAR gefunden: {jar_file}")
            
            # Starte mit echtem Minecraft-Befehl
            cmd = [
                java_path,
                f"-Xmx{ram_mb}M",
                f"-Xms{int(ram_mb * 0.5)}M",
                "-XX:+UseG1GC",
                "-XX:+ParallelRefProcEnabled",
                "-XX:G1NewCollectionPercentage=30",
                "-XX:G1ReservePercent=20",
                "-XX:InitiatingHeapOccupancyPercent=20",
                "-XX:MaxGCPauseMillis=50",
                "-XX:G1HeapRegionSize=16M",
                "-Dfile.encoding=UTF-8",
                "-Duser.country=DE",
                "-Duser.language=de",
                "-Djava.net.preferIPv4Stack=true",
                "-cp", str(jar_file),
                "net.minecraft.client.main.Main",
                "--username", user.username,
                "--version", version.version,
                "--gameDir", str(minecraft_dir),
                "--assetsDir", str(minecraft_dir / "assets"),
                "--assetIndex", version.version,
                "--uuid", user.uuid,
                "--accessToken", user.token or "0",
                "--userProperties", "{}",
                "--userType", "legacy"
            ]
            
            logger.info("Starte Java-Prozess...")
            
            # Starte Minecraft
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(minecraft_dir)
            )
            
            self.is_running = True
            self.start_time = time.time()
            
            logger.info(f"Minecraft gestartet! (PID: {self.process.pid})")
            
            # Monitoring
            monitor_thread = Thread(target=self._monitor_process, daemon=True)
            monitor_thread.start()
            
            return True
        
        except FileNotFoundError:
            logger.error(f"FEHLER: Java nicht gefunden: {java_path}")
            return False
        except Exception as e:
            logger.error(f"FEHLER beim Starten: {str(e)}")
            return False
    
    def _monitor_process(self):
        """Ueberwacht den Prozess"""
        if not self.process:
            return
        
        try:
            self.process.wait()
            logger.info("Minecraft wurde beendet")
        except Exception as e:
            logger.error(f"Monitoring Fehler: {e}")
        finally:
            self.is_running = False
    
    def stop_game(self):
        """Beendet das Spiel"""
        if self.process and self.is_running:
            try:
                logger.info("Beende Minecraft...")
                self.process.terminate()
                self.process.wait(timeout=5)
                logger.info("Minecraft beendet")
            except Exception as e:
                logger.error(f"Fehler beim Beenden: {e}")
    
    def is_game_running(self) -> bool:
        """Prüft ob Spiel läuft"""
        if self.process:
            return self.process.poll() is None
        return False
    
    def get_runtime(self) -> float:
        """Gibt Spiellaufzeit zurück"""
        if self.is_running or self.process:
            return time.time() - self.start_time
        return 0.0


class GameMonitor:
    """Ueberwacht Performance"""
    
    def __init__(self):
        self.fps: int = 0
        self.ram_used: float = 0
        self.cpu_used: float = 0
    
    def update_stats(self, fps: int, ram_gb: float, cpu: float):
        """Aktualisiert Statistiken"""
        self.fps = fps
        self.ram_used = ram_gb
        self.cpu_used = cpu
    
    def get_stats(self) -> dict:
        """Gibt Statistiken zurück"""
        return {
            'fps': self.fps,
            'ram_gb': self.ram_used,
            'cpu': self.cpu_used
        }
