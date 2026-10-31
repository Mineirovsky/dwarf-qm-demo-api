from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Cookie, HTTPException, Header, Response, status
from typing import Annotated
import base64

from app.config import Config
from app.models import Login, Session
from app.services.identity import IdentityService, JWTService
from app.services.security import EncryptionService

router = APIRouter(route_class=DishkaRoute)

def encrypt_token(encryption_service: EncryptionService, token: str) -> str:
    return base64.b64encode(encryption_service.encrypt(token.encode("utf-8"))).decode("utf-8")

def decrypt_token(encryption_service: EncryptionService, token: str) -> str:
    return encryption_service.decrypt(base64.b64decode(token)).decode("utf-8")


@router.post("/iam/login")
async def login(
    data: Login,
    response: Response,
    config: FromDishka[Config],
    identity_service: FromDishka[IdentityService],
    encryption_service: FromDishka[EncryptionService],
    jwt_service: FromDishka[JWTService],
    user_agent: Annotated[str, Header()] = "Unknown",
):
    session = identity_service.login(data.username, data.password, user_agent)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    encrypted_token = encrypt_token(encryption_service, session.token)

    response.set_cookie(
        key="refresh_token",
        value=encrypted_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=config.session.ttl,
        path="/iam"
    )

    access_token = jwt_service.create_token(session.user_id)

    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/iam/refresh")
async def refresh(
    identity_service: FromDishka[IdentityService],
    encryption_service: FromDishka[EncryptionService],
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> Session:
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not found")

    try:
        decrypted_token = decrypt_token(encryption_service, refresh_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from e

    session = identity_service.refresh_token(decrypted_token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    return session


@router.post("/iam/logout", status_code=204)
async def logout(
    response: Response,
    identity_service: FromDishka[IdentityService],
    encryption_service: FromDishka[EncryptionService],
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not found")

    try:
        decrypted_token = decrypt_token(encryption_service, refresh_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from e


    identity_service.invalidate_session(decrypted_token)

    response.delete_cookie("refresh_token", path="/iam")
