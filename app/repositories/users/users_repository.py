from app.models import User
import bcrypt

DEFAULT_PASSWORD = bcrypt.hashpw("password".encode(), bcrypt.gensalt())

USERS = [
    User(
        id=1,
        name="John Doe",
        password=DEFAULT_PASSWORD.decode(),
        email="john.doe@example.com",
        created_at="2021-01-01T00:00:00Z",
        updated_at="2021-01-01T00:00:00Z"
    ),
]

class UsersRepository:
    def __init__(self):
        pass

    def get_all(self):
        return USERS

    def get_by_email(self, email: str):
        return next((user for user in USERS if user.email == email), None)
