from fastapi import FastAPI

from app.routers.info_router import router as info_router
from app.routers.iam.me_router import router as iam_me_router
from app.routers.login_router import router as login_router

def initialize_routers(app: FastAPI):
    app.include_router(info_router)
    app.include_router(iam_me_router)
    app.include_router(login_router)
