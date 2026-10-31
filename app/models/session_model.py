from datetime import datetime
from pydantic import BaseModel

from .user_model import User

class Session(BaseModel):
    id: int
    user_id: int
    token: str
    user_agent: str
    created_at: datetime
    expires_at: datetime

    user: User | None = None
