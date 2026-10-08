from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str = Field(exclude=True)
    created_at: str
    updated_at: str
