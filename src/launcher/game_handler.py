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
        """Startet Minecraft"""
        try:
            # RAM in MB
            ram_mb = ram_gb * 1024
            
            # Minecraft Verzeichnis
            minecraft_dir = Path.home() / ".minecraft"
            minecraft_dir.mkdir(exist_ok=True)
            
            logger.info(f"🎮 Starte Minecraft {version.version}...")
            logger.info(f"👤 Spieler: {user.username}")
            logger.info(f"💾 RAM: {ram_gb}GB ({ram_mb}MB)")
            logger.info(f"📂 Minecraft Dir: {minecraft_dir}")
            logger.info(f"☕ Java: {java_path}")
            
            # Kommandozeile für Spielstart mit echten Minecraft-Argumenten
            cmd = [
                java_path,
                f"-Xmx{ram_mb}M",
                f"-Xms{int(ram_mb * 0.5)}M",
                "-XX:+UnlockExperimentalVMOptions",
                "-XX:G1NewCollectionPercentage=20",
                "-XX:G1ReservePercent=5",
                "-XX:InitiatingHeapOccupancyPercent=15",
                "-XX:G1HeapRegionSize=16M",
                "-Dfile.encoding=UTF-8",
                "-Duser.country=DE",
                "-Duser.language=de",
                "-Djava.io.tmpdir=" + str(minecraft_dir / "temp"),
                "-cp",
                "minecraft.jar",
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
            
            logger.info("✅ Java-Prozess wird gestartet...")
            logger.debug(f"Kommando: {' '.join(cmd)}")
            
            # Starte Minecraft als echter Prozess
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(minecraft_dir)
            )
            
            self.is_running = True
            self.start_time = time.time()
            
            logger.info(f"✅ Minecraft Prozess gestartet (PID: {self.process.pid})")
            
            # Starte Monitoring in separatem Thread
            monitor_thread = Thread(target=self._monitor_process, daemon=True)
            monitor_thread.start()
            
            return True
        
        except FileNotFoundError:
            logger.error(f"❌ Java nicht gefunden: {java_path}")
            self.is_running = False
            return False
        except Exception as e:
            logger.error(f"❌ Fehler beim Starten von Minecraft: {e}")
            self.is_running = False
            return False
    
    def _monitor_process(self):
        """Überwacht den Spielprozess"""
        if not self.process:
            return
        
        try:
            # Warte auf Prozessende
            self.process.wait()
            
            logger.info("📋 Minecraft-Output wird gelesen...")
            
        except Exception as e:
            logger.error(f"❌ Fehler beim Monitoring: {e}")
        finally:
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
                logger.info("⏹️ Beende Minecraft...")
                self.process.terminate()
                
                # Warte 5 Sekunden
                try:
                    self.process.wait(timeout=5)
                    logger.info("✅ Minecraft ordnungsgemäß beendet")
                except subprocess.TimeoutExpired:
                    logger.warning("⚠️ Minecraft reagiert nicht, erzwinge Beendigung...")
                    self.process.kill()
                    self.process.wait()
                    logger.info("✅ Minecraft erzwungen beendet")
                    
            except Exception as e:
                logger.error(f"❌ Fehler beim Beenden: {e}")
    
    def is_game_running(self) -> bool:
        """Prüft ob Spiel läuft"""
        if self.process:
            return self.process.poll() is None
        return False
    
    def get_runtime(self) -> float:
        """Gibt Spiellaufzeit in Sekunden zurück"""
        if self.is_running or self.process:
            return time.time() - self.start_time
        return 0.0


class GameMonitor:
    """Überwacht Performance während des Spiels"""
    
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
        """Gibt aktuelle Statistiken zurück"""
        return {
            'fps': self.fps,
            'ram_gb': self.ram_used,
            'cpu': self.cpu_used
        }
