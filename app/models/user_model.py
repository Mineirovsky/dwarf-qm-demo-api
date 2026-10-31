from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    username: str
    name: str
    email: str
    password: Annotated[str | None, Field(exclude=True)] = None
    created_at: datetime
    updated_at: datetime
