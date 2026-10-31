import jwt
from datetime import datetime, timedelta
from dishka import FromDishka

from app.config import Config
from app.services import Service

class JWTService(Service):
    def __init__(self,config: FromDishka[Config]):
        self.config = config

    def create_token(self, user_id: int, expires_in = timedelta(minutes=5)) -> str:
        payload = {
            "sub": str(user_id),
            "exp": int((datetime.now() + expires_in).timestamp()),
        }
        return jwt.encode(payload, self.config.security.hmac_key, algorithm="HS256")

    def verify_token(self, token: str) -> int | None:
        try:
            payload = jwt.decode(token, self.config.security.hmac_key, algorithms=["HS256"])
            return int(payload["sub"])
        except jwt.InvalidTokenError:
            return None
