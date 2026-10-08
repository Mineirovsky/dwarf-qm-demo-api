from dishka.integrations.fastapi import setup_dishka
from dishka import make_async_container

from app.providers import (
    BaseProvider,
    DatabaseProvider,
    RepositoriesProvider,
    ServicesProvider,
)

from fastapi import FastAPI

def initialize_container(app: FastAPI):
    container = make_async_container(
        BaseProvider(),
        DatabaseProvider(),
        RepositoriesProvider(),
        ServicesProvider(),
    )

    setup_dishka(app=app, container=container)
