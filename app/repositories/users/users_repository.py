from psycopg2.extras import RealDictCursor

from app.repositories import Repository
from app.models import User

class UsersRepository(Repository):
    def get_all(self) -> list[User]:
        with self.db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT id, username, name, email, created_at, updated_at FROM users;")
            return [User.model_validate(row) for row in cursor.fetchall()]

    def get_by_username(self, username: str) -> User | None:
        with self.db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s;", (username,))
            result = cursor.fetchone()
            return User.model_validate(result) if result else None
