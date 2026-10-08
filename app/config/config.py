import os
from .db import DBConfig

class Config:
    def __init__(self):
        self.db = DBConfig()

        self.version = os.getenv("APP_VERSION", "0.1.0")
