from dishka import Provider, Scope, provide
from app.config import Config

class BaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return Config()
