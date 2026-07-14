#!/usr/bin/env python3
"""MEXO Client - Moderner Minecraft Java Edition Launcher"""

import sys
from src.ui.main_window import main
from src.utils.logger import logger


if __name__ == "__main__":
    try:
        logger.info("="*60)
        logger.info("🎮 MEXO Client - Minecraft Launcher")
        logger.info("="*60)
        main()
    except Exception as e:
        logger.critical(f"Kritischer Fehler: {e}")
        sys.exit(1)
