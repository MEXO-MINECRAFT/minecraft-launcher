"""Login-System (Microsoft & Offline)"""
from enum import Enum
from typing import Optional, Dict
from dataclasses import dataclass
from src.utils.logger import logger


class AuthMode(Enum):
    """Authentifizierungsmodi"""
    OFFLINE = "offline"
    MICROSOFT = "microsoft"


@dataclass
class UserProfile:
    """Benutzer-Profil"""
    username: str
    uuid: str
    token: Optional[str] = None
    mode: AuthMode = AuthMode.OFFLINE
    skin_url: Optional[str] = None
    cape_url: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Konvertiert zu Dictionary"""
        return {
            'username': self.username,
            'uuid': self.uuid,
            'token': self.token,
            'mode': self.mode.value,
            'skin_url': self.skin_url,
            'cape_url': self.cape_url
        }


class AuthManager:
    """Verwaltet Authentifizierung"""
    
    def __init__(self):
        self.current_user: Optional[UserProfile] = None
        self.mode: AuthMode = AuthMode.OFFLINE
    
    def login_offline(self, username: str) -> UserProfile:
        """Offline-Modus Login"""
        import uuid
        
        user_uuid = str(uuid.uuid4())
        self.current_user = UserProfile(
            username=username,
            uuid=user_uuid,
            mode=AuthMode.OFFLINE
        )
        
        logger.info(f"✓ Offline-Login erfolgreich: {username}")
        return self.current_user
    
    def login_microsoft(self, token: str) -> Optional[UserProfile]:
        """Microsoft-Login (Placeholder)"""
        # TODO: Echte Microsoft OAuth2 Implementation
        logger.warning("Microsoft-Login noch nicht implementiert")
        return None
    
    def logout(self):
        """Abmelden"""
        if self.current_user:
            logger.info(f"✓ Abgemeldet: {self.current_user.username}")
        self.current_user = None
    
    def is_logged_in(self) -> bool:
        """Prüft ob angemeldet"""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[UserProfile]:
        """Gibt aktuellen Benutzer zurück"""
        return self.current_user
