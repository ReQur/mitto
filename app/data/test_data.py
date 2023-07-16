from app.data.models import Message, Chat, User

message1 = Message(id=1, chat_id=1, owner_id=1, text="Hello, how are you?")
message2 = Message(
    id=2, chat_id=1, owner_id=2, text="I'm fine, thanks for asking!"
)
message3 = Message(id=3, chat_id=2, owner_id=3, text="Hey there, what's up?")
message4 = Message(
    id=4, chat_id=2, owner_id=4, text="Not much, just hanging out."
)

chat1 = Chat(id=1, user_ids=[1, 2], messages=[message1, message2])
chat2 = Chat(id=2, user_ids=[3, 4], messages=[message3, message4])

user1 = User(
    email="user1@example.com",
    username="user1",
    password="password1",
    id=1,
    is_active=True,
    chats=[chat1],
)
user2 = User(
    email="user2@example.com",
    username="user2",
    password="password2",
    id=2,
    is_active=True,
    chats=[chat1],
)
user3 = User(
    email="user3@example.com",
    username=None,
    password="password3",
    id=3,
    is_active=True,
    chats=[chat2],
)
user4 = User(
    email="user4@example.com",
    username="user4",
    password="password4",
    id=4,
    is_active=True,
    chats=[chat2],
)

users = {user.id: user for user in [user1, user2, user3, user4]}

chats = {chat.id: chat for chat in [chat1, chat2]}

messages = {
    message.id: message for message in [message1, message2, message3, message4]
}

test_data = {
    "users": users,
    "chats": chats,
    "messages": messages,
}
