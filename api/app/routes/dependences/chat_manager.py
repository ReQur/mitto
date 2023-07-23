from fastapi import HTTPException, status

from app.data import models
from app.data.schemes.chat import ChatUsers, Chat
from app.data.schemes.message import MessageSend, Message
from app.data.schemes.user import UserInfo
from app.services.chat import ChatService, chat_service
from app.services.message import MessageService, message_service


class BadRequest(HTTPException):
    """Error occurred during request processing

    Status Code: status.HTTP_400_BAD_REQUEST
    Detail: passes from message parameter

    :param message: str - passed to exception details
    :raises HTTPException:
    """

    def __init__(
        self,
        message: str,
    ) -> None:
        status_code: int = status.HTTP_400_BAD_REQUEST
        super().__init__(status_code=status_code, detail=message)


class ChatManager:
    """ChatManager class for managing request related to chat actions.

    :Attributes:
        messages: message service injection
        chats: chat service injection

    :Methods:
        init: class initialization
        initiate_chat: creates new chat among of
            got users and send first message there
        retain_message: save got message
        get_messages: get all messages from the chat
        get_chats: get all chats of the user

    """

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
    ) -> Message:
        """Method creates new chat between users and pass to it sent message

        :param initiator: user which is initiate chat
        :param recipient: user which is addressee of message
        :param message_text: text of sent message
        :return: saved message from database
        """
        users = ChatUsers(user_ids=[initiator.id, recipient.id])
        chat = self.chats.add(users)
        message = MessageSend(
            text=message_text, chat_id=chat.id, owner_id=initiator.id
        )
        return self.messages.add(message)

    def retain_message(self, message: MessageSend) -> Message:
        """Retains new message and save to proposed chat

        :param message:
        :return: saved message from database
        """
        if not self.chats.get(message.owner_id, message.chat_id):
            raise BadRequest("Cannot send message to this chat")

        return self.messages.add(message)

    def get_messages(
        self, user: UserInfo, chat_id
    ) -> dict[int, models.Message]:
        """get all messages related to proposed chat from the database

        :param user: user which asks messages
        :param chat_id: proposed chat id
        :return: dictionary of messages
        """
        if not self.chats.get(user.id, chat_id):
            raise BadRequest("Cannot read messages from this chat")

        return self.messages.get_all(chat_id)

    def get_chats(self, user: UserInfo) -> dict[int, Chat]:
        """get all chats related to user from the database

        :param user: user which asks chats
        :return: dictionary of chats
        """
        return self.chats.get_all(user.id)


chat_manager = ChatManager()
