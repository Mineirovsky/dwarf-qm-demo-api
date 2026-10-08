from dishka import Provider, Scope, provide
from app.repositories.users import UsersRepository

class RepositoriesProvider(Provider):
    def __init__(self):
        super().__init__()

    @provide(scope=Scope.REQUEST)
    def get_users_repository(self) -> UsersRepository:
        repository = UsersRepository()
        return repository
