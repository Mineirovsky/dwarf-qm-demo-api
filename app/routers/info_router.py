from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from app.config import Config


router = APIRouter(route_class=DishkaRoute)

@router.get("/info")
async def get_info(config: FromDishka[Config]):
    return {
        "name": "DwarfQM",
        "version": config.version,
        "description": "DwarfQM is an intelligent inventory management system.",
        "author": "Gabriel Mineiro",
        "author_email": "gabrielpfgmineiro@gmail.com",
    }
