from dishka import Provider, Scope, provide

from app.services.identity import IdentityService

from app.repositories.users import UsersRepository

class ServicesProvider(Provider):
    def __init__(self):
        super().__init__()

    @provide(scope=Scope.REQUEST)
    def get_identity_service(self, users_repository: UsersRepository) -> IdentityService:
        service = IdentityService(users_repository)
        return service
