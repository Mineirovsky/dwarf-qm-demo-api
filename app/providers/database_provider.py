from dishka import Provider, Scope, provide
from typing import Iterable
from psycopg2 import connect
from psycopg2.extensions import connection as Connection

from app.config import Config

class DatabaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_connection(self, config: Config) -> Iterable[Connection]:
        connection = connect(
            host=config.db.host,
            port=config.db.port,
            user=config.db.user,
            password=config.db.password,
            database=config.db.name,
        )
        yield connection
        connection.close()
