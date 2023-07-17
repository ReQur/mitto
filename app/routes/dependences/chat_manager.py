from fastapi import Depends, Request, HTTPException, status, Response

from app.data import models
from app.data.schemes.chat import ChatUsers, Chat
from app.data.schemes.message import MessageSend, Message
from app.data.schemes.user import UserInfo
from app.services.chat import ChatService, chat_service
from app.services.message import MessageService, message_service


class BadRequest(HTTPException):
    def __init__(
        self,
        message: str,
    ) -> None:
        status_code: int = status.HTTP_400_BAD_REQUEST
        super().__init__(status_code=status_code, detail=message)


class ChatManager:
    messages: MessageService
    chats: ChatService

    def __init__(self, messages=message_service, chats=chat_service):
        self.messages = messages
        self.chats = chats

    def initiate_chat(
        self,
        initiator: UserInfo,
        recipient: UserInfo,
        message_text: str,
    ):
        users = ChatUsers(user_ids=[initiator.id, recipient.id])
        chat = self.chats.add(users)
        message = MessageSend(
            text=message_text, chat_id=chat.id, owner_id=initiator.id
        )
        return self.messages.add(message)

    def retain_message(self, message: MessageSend):
        if not self.chats.get(message.owner_id, message.chat_id):
            raise BadRequest("Cannot send message to this chat")

        return self.messages.add(message)

    def get_messages(
        self, user: UserInfo, chat_id
    ) -> dict[int, models.Message]:
        if not self.chats.get(user.id, chat_id):
            raise BadRequest("Cannot read messages from this chat")

        return self.messages.get_all(chat_id)

    def get_chats(self, user: UserInfo) -> dict[int, Chat]:
        return self.chats.get_all(user.id)


chat_manager = ChatManager()
