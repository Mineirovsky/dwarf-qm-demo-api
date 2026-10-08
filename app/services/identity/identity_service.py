
import bcrypt
from dishka.integrations.fastapi import FromDishka

from app.repositories.users import UsersRepository

from app.types import Ok, Err, Result
from app.models import Login, User

class IdentityService:
    def __init__(self, users_repository: FromDishka[UsersRepository]):
        self.users_repository = users_repository


    def authenticate(self, data: Login) -> Result[User, str]:
        user = self.users_repository.get_by_email(data.email)
        if not user:
            return Err("User not found")

        if not bcrypt.checkpw(data.password.encode(), user.password.encode()):
            return Err("Password is incorrect")

        return Ok(user)


    def get_me(self):
        return self.users_repository.get_all()
