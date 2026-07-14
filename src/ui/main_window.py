"""Hauptfenster des MEXO Clients"""
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QLabel, QSpinBox, QComboBox, QCheckBox, QPushButton, QTabWidget,
    QGroupBox, QGridLayout, QTextEdit, QLineEdit, QFileDialog, QMessageBox,
    QListWidget, QListWidgetItem, QProgressBar
)
from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap, QColor

from src.ui.pink_theme import ThemeMode, get_pink_theme_stylesheet
from src.ui.widgets import PlayButton, HeaderLabel, SubHeaderLabel, CustomButton
from src.launcher.versions import VersionManager, VersionType
from src.launcher.game_handler import GameProcess
from src.auth.login import AuthManager
from src.utils.system_info import SystemInfo, JavaFinder
from src.utils.config import config
from src.utils.logger import logger


class MEXOClient(QMainWindow):
    """Hauptfenster des MEXO Clients"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MEXO Client - Minecraft Launcher")
        self.setGeometry(100, 100, 1200, 750)
        self.setMinimumSize(1000, 650)
        
        # Core-Module
        self.version_manager = VersionManager()
        self.auth_manager = AuthManager()
        self.game_process = GameProcess()
        self.current_theme = ThemeMode.DARK
        self.selected_ram = 4
        self.selected_java_path = JavaFinder.find_java()
        
        # UI erstellen
        self.setup_ui()
        self.apply_theme(self.current_theme)
        
        # System-Info initial anzeigen
        logger.info("🎮 MEXO Client gestartet")
        SystemInfo.print_system_info()
        
        # Status-Update Timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_system_stats)
        self.status_timer.start(2000)  # Alle 2 Sekunden updaten
    
    def setup_ui(self):
        """Erstellt die Benutzeroberfläche"""
        
        # Hauptwidget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Hauptlayout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar, 0)
        
        # Inhalt (Stacked Widget für verschiedene Seiten)
        self.stacked_widget = QStackedWidget()
        self.home_page = self.create_home_page()
        self.settings_page = self.create_settings_page()
        self.logs_page = self.create_logs_page()
        
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.settings_page)
        self.stacked_widget.addWidget(self.logs_page)
        
        main_layout.addWidget(self.stacked_widget, 1)
    
    def create_sidebar(self) -> QWidget:
        """Erstellt die Seitenleiste"""
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #1A1A1A; border-right: 2px solid #FF1493;")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(15)
        
        # MEXO Logo/Titel
        title = QLabel("MEXO")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #FF1493;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Client")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color: #D0D0D0;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        # Navigation Buttons
        self.nav_buttons = {}
        
        nav_data = [
            ("🏠 Home", 0),
            ("⚙️ Einstellungen", 1),
            ("📋 Logs", 2),
        ]
        
        for button_text, page_index in nav_data:
            btn = CustomButton(button_text)
            btn.clicked.connect(lambda checked=False, idx=page_index: self.switch_page(idx))
            self.nav_buttons[page_index] = btn
            layout.addWidget(btn)
        
        # Highlight Home Button
        self.nav_buttons[0].setStyleSheet(
            "background-color: #FF1493; color: white; font-weight: bold; border-radius: 8px;"
        )
        
        layout.addStretch()
        
        # Footer Info
        version_label = QLabel("Version 1.0.0")
        version_label.setFont(QFont("Arial", 9))
        version_label.setStyleSheet("color: #808080;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        return sidebar
    
    def create_home_page(self) -> QWidget:
        """Erstellt die Home-Seite"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header = HeaderLabel("Willkommen bei MEXO Client")
        layout.addWidget(header)
        
        # Info
        info = SubHeaderLabel("Wähle eine Minecraft-Version und starte das Spiel")
        layout.addWidget(info)
        
        layout.addSpacing(20)
        
        # Versionen Sektion
        versions_group = QGroupBox("Verfügbare Versionen")
        versions_layout = QVBoxLayout(versions_group)
        
        self.version_list = QListWidget()
        self.version_list.itemClicked.connect(self.on_version_selected)
        
        for version in self.version_manager.get_all_versions():
            item = QListWidgetItem(
                f"{version.name} ({version.type.value}) - Java {version.java_version}"
            )
            item.setData(Qt.ItemDataRole.UserRole, version)
            self.version_list.addItem(item)
        
        versions_layout.addWidget(self.version_list)
        layout.addWidget(versions_group, 1)
        
        # RAM/Java Einstellungen
        settings_group = QGroupBox("Spieleinstellungen")
        settings_layout = QGridLayout(settings_group)
        
        # RAM Selection
        ram_label = QLabel("RAM (GB):")
        self.ram_spinbox = QSpinBox()
        self.ram_spinbox.setMinimum(1)
        self.ram_spinbox.setMaximum(16)
        self.ram_spinbox.setValue(config.get("game.ram_default", 4))
        self.ram_spinbox.valueChanged.connect(self.on_ram_changed)
        
        settings_layout.addWidget(ram_label, 0, 0)
        settings_layout.addWidget(self.ram_spinbox, 0, 1)
        
        # Java Path
        java_label = QLabel("Java Path:")
        self.java_path_label = QLineEdit()
        self.java_path_label.setText(self.selected_java_path or "Nicht gefunden")
        self.java_path_label.setReadOnly(True)
        
        settings_layout.addWidget(java_label, 1, 0)
        settings_layout.addWidget(self.java_path_label, 1, 1)
        
        layout.addWidget(settings_group)
        
        # System Stats
        stats_group = QGroupBox("Systeminformationen")
        stats_layout = QGridLayout(stats_group)
        
        self.ram_usage_label = QLabel("RAM: Wird geladen...")
        self.cpu_usage_label = QLabel("CPU: Wird geladen...")
        self.java_version_label = QLabel(
            f"Java: {JavaFinder.get_java_version(self.selected_java_path) or 'Nicht gefunden'}"
        )
        
        stats_layout.addWidget(self.ram_usage_label, 0, 0)
        stats_layout.addWidget(self.cpu_usage_label, 0, 1)
        stats_layout.addWidget(self.java_version_label, 1, 0, 1, 2)
        
        layout.addWidget(stats_group)
        
        # Play Button
        play_button_container = QWidget()
        play_button_layout = QHBoxLayout(play_button_container)
        play_button_layout.addStretch()
        
        self.play_button = PlayButton()
        self.play_button.clicked.connect(self.on_play_clicked)
        play_button_layout.addWidget(self.play_button)
        
        play_button_layout.addStretch()
        layout.addWidget(play_button_container)
        
        return page
    
    def create_settings_page(self) -> QWidget:
        """Erstellt die Einstellungen-Seite"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header = HeaderLabel("Einstellungen")
        layout.addWidget(header)
        
        # Theme Selection
        theme_group = QGroupBox("Design")
        theme_layout = QVBoxLayout(theme_group)
        
        theme_label = QLabel("Theme:")
        theme_layout.addWidget(theme_label)
        
        theme_buttons_layout = QHBoxLayout()
        
        dark_btn = CustomButton("🌙 Dunkler Modus")
        dark_btn.clicked.connect(lambda: self.apply_theme(ThemeMode.DARK))
        theme_buttons_layout.addWidget(dark_btn)
        
        light_btn = CustomButton("☀️ Heller Modus")
        light_btn.clicked.connect(lambda: self.apply_theme(ThemeMode.LIGHT))
        theme_buttons_layout.addWidget(light_btn)
        
        theme_layout.addLayout(theme_buttons_layout)
        layout.addWidget(theme_group)
        
        # Features
        features_group = QGroupBox("Features")
        features_layout = QVBoxLayout(features_group)
        
        self.discord_checkbox = QCheckBox("Discord Rich Presence aktivieren")
        self.discord_checkbox.setChecked(config.get("features.discord_rpc", True))
        features_layout.addWidget(self.discord_checkbox)
        
        self.auto_update_checkbox = QCheckBox("Automatische Updates aktivieren")
        self.auto_update_checkbox.setChecked(config.get("features.auto_update", True))
        features_layout.addWidget(self.auto_update_checkbox)
        
        self.shader_checkbox = QCheckBox("Shader-Manager aktivieren")
        self.shader_checkbox.setChecked(config.get("features.shader_manager", True))
        features_layout.addWidget(self.shader_checkbox)
        
        self.mod_checkbox = QCheckBox("Mod-Manager aktivieren")
        self.mod_checkbox.setChecked(config.get("features.mod_manager", True))
        features_layout.addWidget(self.mod_checkbox)
        
        layout.addWidget(features_group)
        
        # Info
        info_group = QGroupBox("Informationen")
        info_layout = QVBoxLayout(info_group)
        
        os_info = SystemInfo.get_os_info()
        info_text = f"""
        OS: {os_info['system']} {os_info['release']}
        CPU Cores: {SystemInfo.get_cpu_count()[1]}
        Total RAM: {SystemInfo.get_total_ram()}GB
        Python: {SystemInfo.get_python_version()}
        """
        
        info_label = QLabel(info_text)
        info_label.setFont(QFont("Courier", 10))
        info_layout.addWidget(info_label)
        
        layout.addWidget(info_group)
        layout.addStretch()
        
        # Save Button
        save_btn = CustomButton("💾 Einstellungen speichern")
        save_btn.clicked.connect(self.on_save_settings)
        layout.addWidget(save_btn)
        
        return page
    
    def create_logs_page(self) -> QWidget:
        """Erstellt die Logs-Seite"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header = HeaderLabel("Spiel-Logs")
        layout.addWidget(header)
        
        info = SubHeaderLabel("Aktuelle Logs und Fehlerausgaben")
        layout.addWidget(info)
        
        # Log Display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Courier", 10))
        self.log_display.setText("Logs erscheinen hier, wenn das Spiel läuft...\n\n")
        layout.addWidget(self.log_display)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        clear_btn = CustomButton("🗑️ Logs löschen")
        clear_btn.clicked.connect(self.on_clear_logs)
        button_layout.addWidget(clear_btn)
        
        export_btn = CustomButton("💾 Logs exportieren")
        export_btn.clicked.connect(self.on_export_logs)
        button_layout.addWidget(export_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        return page
    
    def switch_page(self, page_index: int):
        """Wechselt die aktuelle Seite"""
        self.stacked_widget.setCurrentIndex(page_index)
        
        # Update Button Styling
        for idx, btn in self.nav_buttons.items():
            if idx == page_index:
                btn.setStyleSheet(
                    "background-color: #FF1493; color: white; font-weight: bold; border-radius: 8px;"
                )
            else:
                btn.setStyleSheet("")
    
    def apply_theme(self, theme: ThemeMode):
        """Wendet ein Theme an"""
        self.current_theme = theme
        stylesheet = get_pink_theme_stylesheet(theme)
        self.setStyleSheet(stylesheet)
        logger.info(f"🎨 Theme gewechselt: {theme.value}")
    
    def on_version_selected(self, item):
        """Wird aufgerufen, wenn eine Version ausgewählt wird"""
        version = item.data(Qt.ItemDataRole.UserRole)
        self.version_manager.set_selected_version(version)
        logger.info(f"Version ausgewählt: {version.name}")
    
    def on_ram_changed(self, value: int):
        """RAM-Auswahl geändert"""
        self.selected_ram = value
        logger.debug(f"RAM eingestellt: {value}GB")
    
    def on_play_clicked(self):
        """Play-Button geklickt - STARTET ECHTES MINECRAFT"""
        selected_version = self.version_manager.get_selected_version()
        
        if not selected_version:
            QMessageBox.warning(self, "Fehler", "Bitte wähle eine Minecraft-Version aus.")
            return
        
        if not self.selected_java_path:
            QMessageBox.critical(self, "Fehler", "Java nicht gefunden. Bitte installiere Java 8+.")
            return
        
        # Spieler-Login
        user = self.auth_manager.login_offline("MEXO-Player")
        
        logger.info(f"🎮 Minecraft wird gestartet...")
        logger.info(f"👤 Spieler: {user.username}")
        logger.info(f"📦 Version: {selected_version.version}")
        logger.info(f"💾 RAM: {self.selected_ram}GB")
        
        # Starte echtes Minecraft
        success = self.game_process.start_game(
            version=selected_version,
            user=user,
            java_path=self.selected_java_path,
            ram_gb=self.selected_ram
        )
        
        if success:
            self.log_display.append(
                f"✅ [START] Minecraft {selected_version.version} wird gestartet...\n"
                f"👤 Spieler: {user.username}\n"
                f"💾 RAM: {self.selected_ram}GB\n"
                f"☕ Java: {self.selected_java_path}\n"
                f"⏱️ Zeit: {__import__('datetime').datetime.now().strftime('%H:%M:%S')}\n"
            )
            QMessageBox.information(
                self,
                "✅ Minecraft wird gestartet",
                f"Starte {selected_version.name}\nSpieler: {user.username}\nRAM: {self.selected_ram}GB\n\nMinecraft öffnet sich in Kürze..."
            )
        else:
            self.log_display.append(
                f"❌ [FEHLER] Minecraft konnte nicht gestartet werden!\n"
            )
            QMessageBox.critical(self, "Fehler", "Minecraft konnte nicht gestartet werden. Prüfe die Logs.")
    
    def on_save_settings(self):
        """Speichert die Einstellungen"""
        config.set("features.discord_rpc", self.discord_checkbox.isChecked())
        config.set("features.auto_update", self.auto_update_checkbox.isChecked())
        config.set("features.shader_manager", self.shader_checkbox.isChecked())
        config.set("features.mod_manager", self.mod_checkbox.isChecked())
        
        QMessageBox.information(self, "Erfolgreich", "Einstellungen gespeichert!")
        logger.info("✅ Einstellungen gespeichert")
    
    def on_clear_logs(self):
        """Löscht die Logs"""
        self.log_display.clear()
        logger.info("🗑️ Logs gelöscht")
    
    def on_export_logs(self):
        """Exportiert die Logs"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Logs exportieren",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.log_display.toPlainText())
            QMessageBox.information(self, "Erfolgreich", f"Logs exportiert zu:\n{file_path}")
            logger.info(f"📁 Logs exportiert: {file_path}")
    
    def update_system_stats(self):
        """Aktualisiert die Systeminformationen"""
        try:
            ram_total = SystemInfo.get_total_ram()
            ram_avail = SystemInfo.get_available_ram()
            ram_percent = SystemInfo.get_ram_percent()
            cpu_percent = SystemInfo.get_cpu_percent()
            
            self.ram_usage_label.setText(
                f"RAM: {ram_avail}/{ram_total}GB ({ram_percent:.1f}%)"
            )
            self.cpu_usage_label.setText(f"CPU: {cpu_percent:.1f}%")
        except Exception as e:
            logger.error(f"Fehler beim Updaten der System-Stats: {e}")


def main():
    """Haupteinstiegspunkt"""
    app = __import__('PyQt6.QtWidgets', fromlist=['QApplication']).QApplication(sys.argv)
    
    client = MEXOClient()
    client.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
