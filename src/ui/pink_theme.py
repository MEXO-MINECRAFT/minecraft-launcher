"""Pink Theme für MEXO Client"""
from enum import Enum


class ThemeMode(Enum):
    """Theme Modus"""
    DARK = "dark"
    LIGHT = "light"


class PinkColors:
    """Pink Farbschema"""
    
    # Dark Pink Theme
    DARK_BG_PRIMARY = "#0A0A0A"        # Sehr dunkles Schwarz
    DARK_BG_SECONDARY = "#1A1A1A"     # Dunkles Grau
    DARK_BG_TERTIARY = "#2D2D2D"      # Mittleres Grau
    DARK_TEXT_PRIMARY = "#FFFFFF"     # Weiß
    DARK_TEXT_SECONDARY = "#D0D0D0"   # Helles Grau
    DARK_ACCENT = "#FF1493"           # Tiefes Pink (Deep Pink)
    DARK_ACCENT_HOVER = "#FF69B4"     # Helles Pink (Hot Pink)
    DARK_ACCENT_GLOW = "#FF1493CC"    # Pink mit Glow
    DARK_DANGER = "#FF4444"           # Rötliches Pink
    DARK_WARNING = "#FFB347"          # Orange
    DARK_SUCCESS = "#4CAF50"          # Grün
    DARK_BORDER = "#404040"           # Dunkle Border
    DARK_SHADOW = "#FF1493"           # Pink Shadow
    
    # Light Pink Theme
    LIGHT_BG_PRIMARY = "#FAFAFA"      # Nahezu Weiß
    LIGHT_BG_SECONDARY = "#F5F5F5"    # Helles Grau
    LIGHT_BG_TERTIARY = "#ECECEC"    # Mittleres Grau
    LIGHT_TEXT_PRIMARY = "#1A1A1A"    # Fast Schwarz
    LIGHT_TEXT_SECONDARY = "#555555"  # Dunkles Grau
    LIGHT_ACCENT = "#E91E63"          # Material Design Pink
    LIGHT_ACCENT_HOVER = "#FF1493"    # Tieferes Pink
    LIGHT_ACCENT_GLOW = "#E91E63CC"   # Pink mit Glow
    LIGHT_DANGER = "#F44336"          # Rote
    LIGHT_WARNING = "#FFC107"         # Amber
    LIGHT_SUCCESS = "#4CAF50"         # Grün
    LIGHT_BORDER = "#DDDDDD"          # Helle Border
    LIGHT_SHADOW = "#E91E63"          # Pink Shadow


class DarkPinkTheme:
    """Dunkles Pink Theme Stylesheet"""
    
    STYLESHEET = f"""
    * {{
        outline: none;
    }}
    
    QMainWindow {{
        background-color: {PinkColors.DARK_BG_PRIMARY};
        color: {PinkColors.DARK_TEXT_PRIMARY};
    }}
    
    QWidget {{
        background-color: {PinkColors.DARK_BG_PRIMARY};
        color: {PinkColors.DARK_TEXT_PRIMARY};
    }}
    
    QLabel {{
        color: {PinkColors.DARK_TEXT_PRIMARY};
        background-color: transparent;
    }}
    
    QLineEdit, QTextEdit, QComboBox, QSpinBox {{
        background-color: {PinkColors.DARK_BG_SECONDARY};
        color: {PinkColors.DARK_TEXT_PRIMARY};
        border: 2px solid {PinkColors.DARK_BORDER};
        border-radius: 8px;
        padding: 10px;
        selection-background-color: {PinkColors.DARK_ACCENT};
        font-size: 13px;
    }}
    
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {{
        border: 2px solid {PinkColors.DARK_ACCENT};
        background-color: {PinkColors.DARK_BG_TERTIARY};
    }}
    
    QPushButton {{
        background-color: {PinkColors.DARK_ACCENT};
        color: {PinkColors.DARK_TEXT_PRIMARY};
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: bold;
        font-size: 14px;
        transition: all 0.3s ease;
    }}
    
    QPushButton:hover {{
        background-color: {PinkColors.DARK_ACCENT_HOVER};
        box-shadow: 0 0 20px {PinkColors.DARK_ACCENT};
    }}
    
    QPushButton:pressed {{
        background-color: {PinkColors.DARK_ACCENT};
    }}
    
    QPushButton:disabled {{
        background-color: {PinkColors.DARK_BG_TERTIARY};
        color: {PinkColors.DARK_TEXT_SECONDARY};
    }}
    
    #PlayButton {{
        background-color: {PinkColors.DARK_ACCENT};
        color: white;
        border: none;
        border-radius: 12px;
        padding: 20px 60px;
        font-weight: bold;
        font-size: 18px;
        min-width: 200px;
        min-height: 60px;
    }}
    
    #PlayButton:hover {{
        background-color: {PinkColors.DARK_ACCENT_HOVER};
        box-shadow: 0 0 30px {PinkColors.DARK_ACCENT};
    }}
    
    #PlayButton:pressed {{
        background-color: {PinkColors.DARK_ACCENT};
        box-shadow: 0 0 15px {PinkColors.DARK_ACCENT};
    }}
    
    QGroupBox {{
        color: {PinkColors.DARK_TEXT_PRIMARY};
        border: 2px solid {PinkColors.DARK_ACCENT};
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
        background-color: {PinkColors.DARK_BG_SECONDARY};
        width: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {PinkColors.DARK_ACCENT};
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {PinkColors.DARK_ACCENT_HOVER};
    }}
    
    QTabBar::tab {{
        background-color: {PinkColors.DARK_BG_SECONDARY};
        color: {PinkColors.DARK_TEXT_SECONDARY};
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
        margin-right: 2px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {PinkColors.DARK_ACCENT};
        color: {PinkColors.DARK_TEXT_PRIMARY};
    }}
    
    QTabWidget::pane {{
        border: 1px solid {PinkColors.DARK_BORDER};
    }}
    
    QComboBox::drop-down {{
        border-left: 1px solid {PinkColors.DARK_BORDER};
    }}
    
    QComboBox::down-arrow {{
        image: url(noimg);
    }}
    """


class LightPinkTheme:
    """Helles Pink Theme Stylesheet"""
    
    STYLESHEET = f"""
    * {{
        outline: none;
    }}
    
    QMainWindow {{
        background-color: {PinkColors.LIGHT_BG_PRIMARY};
        color: {PinkColors.LIGHT_TEXT_PRIMARY};
    }}
    
    QWidget {{
        background-color: {PinkColors.LIGHT_BG_PRIMARY};
        color: {PinkColors.LIGHT_TEXT_PRIMARY};
    }}
    
    QLabel {{
        color: {PinkColors.LIGHT_TEXT_PRIMARY};
        background-color: transparent;
    }}
    
    QLineEdit, QTextEdit, QComboBox, QSpinBox {{
        background-color: {PinkColors.LIGHT_BG_SECONDARY};
        color: {PinkColors.LIGHT_TEXT_PRIMARY};
        border: 2px solid {PinkColors.LIGHT_BORDER};
        border-radius: 8px;
        padding: 10px;
        selection-background-color: {PinkColors.LIGHT_ACCENT};
        font-size: 13px;
    }}
    
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {{
        border: 2px solid {PinkColors.LIGHT_ACCENT};
        background-color: {PinkColors.LIGHT_BG_TERTIARY};
    }}
    
    QPushButton {{
        background-color: {PinkColors.LIGHT_ACCENT};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: bold;
        font-size: 14px;
    }}
    
    QPushButton:hover {{
        background-color: {PinkColors.LIGHT_ACCENT_HOVER};
        box-shadow: 0 0 20px {PinkColors.LIGHT_ACCENT};
    }}
    
    QPushButton:pressed {{
        background-color: {PinkColors.LIGHT_ACCENT};
    }}
    
    QPushButton:disabled {{
        background-color: {PinkColors.LIGHT_BG_TERTIARY};
        color: {PinkColors.LIGHT_TEXT_SECONDARY};
    }}
    
    #PlayButton {{
        background-color: {PinkColors.LIGHT_ACCENT};
        color: white;
        border: none;
        border-radius: 12px;
        padding: 20px 60px;
        font-weight: bold;
        font-size: 18px;
        min-width: 200px;
        min-height: 60px;
    }}
    
    #PlayButton:hover {{
        background-color: {PinkColors.LIGHT_ACCENT_HOVER};
        box-shadow: 0 0 30px {PinkColors.LIGHT_ACCENT};
    }}
    
    #PlayButton:pressed {{
        background-color: {PinkColors.LIGHT_ACCENT};
        box-shadow: 0 0 15px {PinkColors.LIGHT_ACCENT};
    }}
    
    QGroupBox {{
        color: {PinkColors.LIGHT_TEXT_PRIMARY};
        border: 2px solid {PinkColors.LIGHT_ACCENT};
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
        background-color: {PinkColors.LIGHT_BG_SECONDARY};
        width: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {PinkColors.LIGHT_ACCENT};
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {PinkColors.LIGHT_ACCENT_HOVER};
    }}
    
    QTabBar::tab {{
        background-color: {PinkColors.LIGHT_BG_SECONDARY};
        color: {PinkColors.LIGHT_TEXT_SECONDARY};
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
        margin-right: 2px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {PinkColors.LIGHT_ACCENT};
        color: white;
    }}
    
    QTabWidget::pane {{
        border: 1px solid {PinkColors.LIGHT_BORDER};
    }}
    
    QComboBox::drop-down {{
        border-left: 1px solid {PinkColors.LIGHT_BORDER};
    }}
    """


def get_pink_theme_stylesheet(mode: ThemeMode) -> str:
    """Gibt Pink-Theme Stylesheet zurück"""
    if mode == ThemeMode.DARK:
        return DarkPinkTheme.STYLESHEET
    else:
        return LightPinkTheme.STYLESHEET
