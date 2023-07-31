-- Заполнение таблицы users
INSERT INTO users (email, username, password, is_active)
VALUES
('user1@example.com', 'user1', 'password1', true),
('user2@example.com', 'user2', 'password2', true),
( 'user3@example.com', NULL, 'password3', true),
( 'user4@example.com', 'user4', 'password4', true);

-- Заполнение таблицы chat
INSERT INTO chat (is_active)
VALUES
(true),
(true);

-- Заполнение таблицы user_chat
INSERT INTO user_chat (user_id, chat_id)
VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 2);

-- Заполнение таблицы message
INSERT INTO message (text, owner_id, chat_id)
VALUES
('Hello, how are you?', 1, 1),
('I''m fine, thanks for asking!', 2, 1),
('Hey there, what''s up?', 3, 2),
('Not much, just hanging out.', 4, 2);
