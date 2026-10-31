from dishka import Provider, Scope, provide
from psycopg2.extensions import connection

from app.repositories import SessionsRepository
from app.repositories.users import UsersRepository

class RepositoriesProvider(Provider):
    def __init__(self):
        super().__init__()

    @provide(scope=Scope.REQUEST)
    def get_users_repository(self, db_connection: connection) -> UsersRepository:
        repository = UsersRepository(db_connection)
        return repository

    @provide(scope=Scope.REQUEST)
    def get_sessions_repository(self, db_connection: connection) -> SessionsRepository:
        repository = SessionsRepository(db_connection)
        return repository
