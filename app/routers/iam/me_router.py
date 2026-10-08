from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.services.identity import IdentityService

router = APIRouter(route_class=DishkaRoute)

@router.get("/iam/me")
async def get_me(identity_service: FromDishka[IdentityService]):
    return identity_service.get_me()
