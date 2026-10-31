import base64
import bcrypt
import secrets
from datetime import datetime, timedelta
from dishka.integrations.fastapi import FromDishka

from app.config import Config
from app.models import User, Session
from app.repositories import SessionsRepository, RepositoryException
from app.repositories.users import UsersRepository
from app.services import Service
from app.services.security import EncryptionService

class IdentityService(Service):
    def __init__(
        self,
        config: FromDishka[Config],
        users_repository: FromDishka[UsersRepository],
        sessions_repository: FromDishka[SessionsRepository],
    ):
        super().__init__(config)
        self.users_repository = users_repository
        self.sessions_repository = sessions_repository


    def authenticate(self, username: str, password: str) -> User | None:
        user = self.users_repository.get_by_username(username)
        if not user:
            return None

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return None

        return user


    def create_session(self, user_id: int, user_agent: str, ttl: timedelta) -> Session | None:
        token = secrets.token_hex()
        expires_at = datetime.now() + ttl

        session = self.sessions_repository.create(user_id, token, user_agent, expires_at)
        return session


    def login(self, username: str, password: str, user_agent: str) -> Session | None:
        authenticated_user = self.authenticate(username, password)

        if not authenticated_user:
            return None

        return self.create_session(
            authenticated_user.id,
            user_agent,
            timedelta(seconds=self.config.session.ttl)
        )


    def get_me(self):
        return self.users_repository.get_all()


    def refresh_token(self, session_token: str):
        session = self.sessions_repository.get_by_token(session_token)
        if not session:
            return None

        if session.expires_at < datetime.now():
            return None

        return session

    def invalidate_session(self, session_token: str):
        self.sessions_repository.invalidate(session_token)
