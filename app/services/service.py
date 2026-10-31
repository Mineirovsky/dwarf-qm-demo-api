from dishka.integrations.fastapi import FromDishka

from app.config import Config

class Service:
    def __init__(self, config: FromDishka[Config]):
        self.config = config
