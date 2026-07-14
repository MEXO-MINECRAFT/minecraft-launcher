"""System-Informationen und Hardware-Erkennung"""
import psutil
import platform
from pathlib import Path
from typing import Optional, Tuple
from src.utils.logger import logger


class SystemInfo:
    """Sammelt und stellt Systeminformationen zur Verfügung"""
    
    @staticmethod
    def get_total_ram() -> float:
        """Gesamter RAM in GB"""
        return round(psutil.virtual_memory().total / (1024 ** 3), 2)
    
    @staticmethod
    def get_available_ram() -> float:
        """Verfügbarer RAM in GB"""
        return round(psutil.virtual_memory().available / (1024 ** 3), 2)
    
    @staticmethod
    def get_ram_percent() -> float:
        """RAM-Auslastung in Prozent"""
        return psutil.virtual_memory().percent
    
    @staticmethod
    def get_cpu_percent() -> float:
        """CPU-Auslastung in Prozent"""
        return psutil.cpu_percent(interval=1)
    
    @staticmethod
    def get_cpu_count() -> Tuple[int, int]:
        """Anzahl der CPU-Kerne (physisch, logisch)"""
        return psutil.cpu_count(logical=False), psutil.cpu_count(logical=True)
    
    @staticmethod
    def get_os_info() -> dict:
        """Betriebssystem-Informationen"""
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }
    
    @staticmethod
    def get_python_version() -> str:
        """Python-Version"""
        return platform.python_version()
    
    @staticmethod
    def print_system_info():
        """Druckt Systeminformationen aus"""
        logger.info("=" * 50)
        logger.info("SYSTEM INFORMATIONEN")
        logger.info("=" * 50)
        
        os_info = SystemInfo.get_os_info()
        logger.info(f"OS: {os_info['system']} {os_info['release']}")
        logger.info(f"Architektur: {os_info['machine']}")
        logger.info(f"Python: {SystemInfo.get_python_version()}")
        
        phys, log = SystemInfo.get_cpu_count()
        logger.info(f"CPU Cores: {phys} (physisch), {log} (logisch)")
        
        total_ram = SystemInfo.get_total_ram()
        avail_ram = SystemInfo.get_available_ram()
        logger.info(f"RAM: {total_ram}GB total, {avail_ram}GB verfügbar")
        
        logger.info("=" * 50)


class JavaFinder:
    """Findet Java-Installation auf dem System"""
    
    @staticmethod
    def find_java() -> Optional[str]:
        """Versucht Java-Installation zu finden"""
        import shutil
        import subprocess
        
        # Versuche 'java' im PATH zu finden
        java_path = shutil.which('java')
        
        if java_path:
            try:
                # Verifiziere Java-Installation
                result = subprocess.run(
                    [java_path, '-version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    logger.info(f"✓ Java gefunden: {java_path}")
                    return java_path
            except Exception as e:
                logger.warning(f"Fehler beim Verifizieren von Java: {e}")
        
        logger.warning("✗ Java nicht gefunden")
        return None
    
    @staticmethod
    def get_java_version(java_path: str) -> Optional[str]:
        """Ruft Java-Version ab"""
        import subprocess
        
        try:
            result = subprocess.run(
                [java_path, '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            # Java-Version ist im stderr
            return result.stderr.strip()
        except Exception as e:
            logger.error(f"Fehler beim Auslesen der Java-Version: {e}")
            return None
