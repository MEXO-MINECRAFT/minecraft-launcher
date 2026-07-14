"""Custom Widgets für den MEXO Client"""
from PyQt6.QtWidgets import (
    QPushButton, QLabel, QWidget, QVBoxLayout, QHBoxLayout, 
    QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QEvent, pyqtSignal
from PyQt6.QtGui import QFont, QCursor


class CustomButton(QPushButton):
    """Custom Button mit Hover-Effekt"""
    
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setMinimumHeight(40)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    
    def enterEvent(self, event: QEvent):
        """Hover-Effekt"""
        super().enterEvent(event)
    
    def leaveEvent(self, event: QEvent):
        """Hover-Effekt Ende"""
        super().leaveEvent(event)


class PlayButton(CustomButton):
    """Große Play-Schaltfläche"""
    
    def __init__(self, parent=None):
        super().__init__("▶ SPIELEN", parent)
        self.setObjectName("PlayButton")
        self.setMinimumHeight(70)
        self.setMinimumWidth(250)
        self.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)


class HeaderLabel(QLabel):
    """Header Label mit großem Text"""
    
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        font = QFont("Arial", 24, QFont.Weight.Bold)
        self.setFont(font)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class SubHeaderLabel(QLabel):
    """Sub-Header Label"""
    
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        font = QFont("Arial", 14)
        self.setFont(font)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class RoundedFrame(QFrame):
    """Frame mit abgerundeten Ecken"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)


class ScrollableWidget(QScrollArea):
    """Scrollbares Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
