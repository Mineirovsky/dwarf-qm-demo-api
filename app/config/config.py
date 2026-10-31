import os

from .db import DBConfig
from .session import SessionConfig
from .security import SecurityConfig

class Config:
    def __init__(self):
        self.db = DBConfig()

        self.version = os.getenv("APP_VERSION", "0.1.0")
        self.session = SessionConfig()
        self.security = SecurityConfig()
