from dishka import Provider, Scope, provide

from app.config import Config

from app.repositories.users import UsersRepository
from app.repositories import SessionsRepository

from app.services.identity import IdentityService, JWTService
from app.services.security import EncryptionService

class ServicesProvider(Provider):
    def __init__(self):
        super().__init__()

    @provide(scope=Scope.REQUEST)
    def get_identity_service(
        self,
        config: Config,
        users_repository: UsersRepository,
        sessions_repository: SessionsRepository,
    ) -> IdentityService:
        service = IdentityService(config, users_repository, sessions_repository)
        return service

    @provide(scope=Scope.REQUEST)
    def get_encryption_service(
        self,
        config: Config
    ) -> EncryptionService:
        service = EncryptionService(config)
        return service

    @provide(scope=Scope.REQUEST)
    def get_jwt_service(
        self,
        config: Config
    ) -> JWTService:
        service = JWTService(config)
        return service
