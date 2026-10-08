from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from app.models import Login
from app.services.identity import IdentityService

router = APIRouter(route_class=DishkaRoute)

@router.post("/login")
async def login(data: Login, identity_service: FromDishka[IdentityService]):
    result = identity_service.authenticate(data)
    if result.is_ok():
        return result.value()
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
