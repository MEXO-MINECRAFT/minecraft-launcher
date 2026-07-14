"""Dark/Light Theme System"""
from enum import Enum


class ThemeMode(Enum):
    """Theme Modus"""
    DARK = "dark"
    LIGHT = "light"


class Colors:
    """Farbschema"""
    
    # Dark Theme
    DARK_BG_PRIMARY = "#1E1E1E"
    DARK_BG_SECONDARY = "#2D2D2D"
    DARK_BG_TERTIARY = "#3A3A3A"
    DARK_TEXT_PRIMARY = "#FFFFFF"
    DARK_TEXT_SECONDARY = "#B0B0B0"
    DARK_ACCENT = "#4CAF50"  # Minecraft Green
    DARK_ACCENT_HOVER = "#66BB6A"
    DARK_DANGER = "#F44336"
    DARK_WARNING = "#FFC107"
    DARK_SUCCESS = "#4CAF50"
    DARK_BORDER = "#404040"
    
    # Light Theme
    LIGHT_BG_PRIMARY = "#FFFFFF"
    LIGHT_BG_SECONDARY = "#F5F5F5"
    LIGHT_BG_TERTIARY = "#ECECEC"
    LIGHT_TEXT_PRIMARY = "#1E1E1E"
    LIGHT_TEXT_SECONDARY = "#666666"
    LIGHT_ACCENT = "#2E7D32"  # Darker Green
    LIGHT_ACCENT_HOVER = "#388E3C"
    LIGHT_DANGER = "#D32F2F"
    LIGHT_WARNING = "#F57C00"
    LIGHT_SUCCESS = "#388E3C"
    LIGHT_BORDER = "#CCCCCC"


class DarkTheme:
    """Dunkles Theme Stylesheet"""
    
    STYLESHEET = f"""
    QMainWindow {{
        background-color: {Colors.DARK_BG_PRIMARY};
        color: {Colors.DARK_TEXT_PRIMARY};
    }}
    
    QWidget {{
        background-color: {Colors.DARK_BG_PRIMARY};
        color: {Colors.DARK_TEXT_PRIMARY};
    }}
    
    QLabel {{
        color: {Colors.DARK_TEXT_PRIMARY};
    }}
    
    QLineEdit, QTextEdit, QComboBox, QSpinBox {{
        background-color: {Colors.DARK_BG_SECONDARY};
        color: {Colors.DARK_TEXT_PRIMARY};
        border: 1px solid {Colors.DARK_BORDER};
        border-radius: 6px;
        padding: 8px;
        selection-background-color: {Colors.DARK_ACCENT};
    }}
    
    QPushButton {{
        background-color: {Colors.DARK_ACCENT};
        color: {Colors.DARK_TEXT_PRIMARY};
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 14px;
    }}
    
    QPushButton:hover {{
        background-color: {Colors.DARK_ACCENT_HOVER};
    }}
    
    QPushButton:pressed {{
        background-color: {Colors.DARK_ACCENT};
    }}
    
    QPushButton:disabled {{
        background-color: {Colors.DARK_BG_TERTIARY};
        color: {Colors.DARK_TEXT_SECONDARY};
    }}
    
    QGroupBox {{
        color: {Colors.DARK_TEXT_PRIMARY};
        border: 2px solid {Colors.DARK_BORDER};
        border-radius: 8px;
        padding-top: 12px;
        margin-top: 8px;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 12px;
        padding: 0 3px 0 3px;
    }}
    
    QScrollBar:vertical {{
        background-color: {Colors.DARK_BG_SECONDARY};
        width: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {Colors.DARK_BORDER};
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {Colors.DARK_TEXT_SECONDARY};
    }}
    
    QTabBar::tab {{
        background-color: {Colors.DARK_BG_SECONDARY};
        color: {Colors.DARK_TEXT_SECONDARY};
        padding: 8px 20px;
        border-radius: 6px 6px 0 0;
        margin-right: 2px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {Colors.DARK_ACCENT};
        color: {Colors.DARK_TEXT_PRIMARY};
    }}
    """


class LightTheme:
    """Helles Theme Stylesheet"""
    
    STYLESHEET = f"""
    QMainWindow {{
        background-color: {Colors.LIGHT_BG_PRIMARY};
        color: {Colors.LIGHT_TEXT_PRIMARY};
    }}
    
    QWidget {{
        background-color: {Colors.LIGHT_BG_PRIMARY};
        color: {Colors.LIGHT_TEXT_PRIMARY};
    }}
    
    QLabel {{
        color: {Colors.LIGHT_TEXT_PRIMARY};
    }}
    
    QLineEdit, QTextEdit, QComboBox, QSpinBox {{
        background-color: {Colors.LIGHT_BG_SECONDARY};
        color: {Colors.LIGHT_TEXT_PRIMARY};
        border: 1px solid {Colors.LIGHT_BORDER};
        border-radius: 6px;
        padding: 8px;
        selection-background-color: {Colors.LIGHT_ACCENT};
    }}
    
    QPushButton {{
        background-color: {Colors.LIGHT_ACCENT};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 14px;
    }}
    
    QPushButton:hover {{
        background-color: {Colors.LIGHT_ACCENT_HOVER};
    }}
    
    QPushButton:pressed {{
        background-color: {Colors.LIGHT_ACCENT};
    }}
    
    QPushButton:disabled {{
        background-color: {Colors.LIGHT_BG_TERTIARY};
        color: {Colors.LIGHT_TEXT_SECONDARY};
    }}
    
    QGroupBox {{
        color: {Colors.LIGHT_TEXT_PRIMARY};
        border: 2px solid {Colors.LIGHT_BORDER};
        border-radius: 8px;
        padding-top: 12px;
        margin-top: 8px;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 12px;
        padding: 0 3px 0 3px;
    }}
    
    QScrollBar:vertical {{
        background-color: {Colors.LIGHT_BG_SECONDARY};
        width: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {Colors.LIGHT_BORDER};
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {Colors.LIGHT_TEXT_SECONDARY};
    }}
    
    QTabBar::tab {{
        background-color: {Colors.LIGHT_BG_SECONDARY};
        color: {Colors.LIGHT_TEXT_SECONDARY};
        padding: 8px 20px;
        border-radius: 6px 6px 0 0;
        margin-right: 2px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {Colors.LIGHT_ACCENT};
        color: white;
    }}
    """


def get_theme_stylesheet(mode: ThemeMode) -> str:
    """Gibt Stylesheet für Theme zurück"""
    if mode == ThemeMode.DARK:
        return DarkTheme.STYLESHEET
    else:
        return LightTheme.STYLESHEET
