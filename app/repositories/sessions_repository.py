from datetime import datetime
from psycopg2 import Error
from psycopg2.extras import RealDictCursor, RealDictRow
from pydantic import ValidationError

from app.repositories import Repository, RepositoryException
from app.models import Session

class SessionsRepository(Repository):
    def create(self, user_id: int, token: str, user_agent: str, expires_at: datetime) -> Session:
        try:
            with self.db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "INSERT INTO sessions (user_id, token, user_agent, expires_at) VALUES (%s, %s, %s, %s) RETURNING *;",
                    (user_id, token, user_agent, expires_at.isoformat())
                )
                session = Session.model_validate(cursor.fetchone())
                self.db_connection.commit()
                return session
        except Error as e:
            self.db_connection.rollback()
            raise RepositoryException(f"Database transaction failed: {e.pgcode}") from e
        except ValidationError as e:
            self.db_connection.rollback()
            raise RepositoryException(f"Malformed database response") from e


    def _make_composed_session_model(self, row: RealDictRow) -> Session:
        return Session.model_validate({
            "id": row["id"],
            "user_id": row["user_id"],
            "token": row["token"],
            "user_agent": row["user_agent"],
            "expires_at": row["expires_at"],
            "created_at": row["created_at"],
            "user": {
                "id": row["user_id"],
                "username": row["u_username"],
                "name": row["u_name"],
                "email": row["u_email"],
                "created_at": row["u_created_at"],
                "updated_at": row["u_updated_at"]}
            }
        )


    def get_by_token(self, token: str) -> Session | None:
        try:
            with self.db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT s.*, u.username AS u_username, u.name AS u_name, u.email AS u_email, u.created_at AS u_created_at, u.updated_at AS u_updated_at FROM sessions s LEFT JOIN users u ON s.user_id = u.id WHERE s.token = %s;", (token,))
                result = cursor.fetchone()
                return self._make_composed_session_model(result) if result else None
        except Error as e:
            raise RepositoryException(f"Database query failed: {e.pgcode}") from e
        except ValidationError as e:
            raise RepositoryException(f"Malformed database response") from e


    def get_valids_from_user(self, user_id: int) -> list[Session]:
        try:
            with self.db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM sessions WHERE user_id = %d AND expires_at > NOW() ORDER BY created_at DESC;",
                    (user_id,)
                )
                return [Session.model_validate(row) for row in cursor.fetchall()]
        except Error as e:
            raise RepositoryException(f"Database query failed: {e.pgcode}") from e
        except ValidationError as e:
            raise RepositoryException(f"Malformed database response") from e


    def invalidate(self, token: str) -> None:
        try:
            with self.db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("UPDATE sessions SET expires_at = NOW() WHERE token = %s;", (token,))
                self.db_connection.commit()
        except Error as e:
            self.db_connection.rollback()
            raise RepositoryException(f"Database transaction failed: {e.pgcode}") from e


    def invalidate_all_from_user(self, user_id: int) -> None:
        try:
            with self.db_connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("UPDATE sessions SET expires_at = NOW() WHERE user_id = %d;", (user_id,))
                self.db_connection.commit()
        except Error as e:
            self.db_connection.rollback()
            raise RepositoryException(f"Database transaction failed: {e.pgcode}") from e
