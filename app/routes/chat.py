import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.data import models
from app.data.schemes.chat import Chat
from app.data.schemes.message import MessageSend
from app.data.schemes.user import UserInfo
from app.routes.dependences.authorization import (
    DeactivatedAccount,
    Unauthorized,
    authorization_handler,
)
from app.routes.dependences.chat_manager import chat_manager, BadRequest
from app.services.user import (
    user_service,
    InactiveUserException,
    UserServiceException,
)

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=dict[int, Chat])
async def get_chats(
    claims: Annotated[
        UserInfo, Depends(authorization_handler.validate_access_token)
    ]
) -> dict[int, Chat]:
    try:
        user = user_service.get(claims.id)
    except InactiveUserException:
        raise DeactivatedAccount()
    except UserServiceException:
        raise Unauthorized("Who are you? Please reauthenticate to the system")

    return chat_manager.get_chats(user)


@router.get("/{chat_id}/messages", response_model=dict[int, models.Message])
async def get_messages(
    claims: Annotated[
        UserInfo, Depends(authorization_handler.validate_access_token)
    ],
    chat_id: int,
) -> dict[int, models.Message]:
    try:
        user = user_service.get(claims.id)
    except InactiveUserException:
        raise DeactivatedAccount()
    except UserServiceException:
        raise Unauthorized("Who are you? Please reauthenticate to the system")

    return chat_manager.get_messages(user, chat_id)


@router.post("/send-message", response_model=models.Message)
async def send_message(
    claims: Annotated[
        UserInfo, Depends(authorization_handler.validate_access_token)
    ],
    message: MessageSend,
):
    try:
        user = user_service.get(claims.id)
    except InactiveUserException:
        raise DeactivatedAccount()
    except UserServiceException:
        raise Unauthorized("Who are you? Please reauthenticate to the system")

    if user.id != message.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Message owner_id and your id isn't match",
        )

    return chat_manager.retain_message(message)


@router.post("/initiate/{recipient_id}", response_model=models.Message)
async def initiate_chat(
    claims: Annotated[
        UserInfo, Depends(authorization_handler.validate_access_token)
    ],
    recipient_id: int,
    message: str,
):
    try:
        user = user_service.get(claims.id)
    except InactiveUserException:
        raise DeactivatedAccount()
    except UserServiceException:
        raise Unauthorized("Who are you? Please reauthenticate to the system")

    try:
        recipient = user_service.get(recipient_id)
    except InactiveUserException:
        raise BadRequest("Recipient account is deactivated")
    except UserServiceException:
        raise BadRequest("Cannot find asked account")

    return chat_manager.initiate_chat(
        user, recipient, message
    )
