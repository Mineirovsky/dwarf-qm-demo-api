import os

class SessionConfig:
    def __init__(self):
        self.ttl = int(os.getenv("SESSION_TTL", "2_592_000")) # 30 days
