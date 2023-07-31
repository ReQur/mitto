CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    username VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE chat (
    id SERIAL PRIMARY KEY,
    is_active BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE user_chat (
    user_id INTEGER REFERENCES users(id),
    chat_id INTEGER REFERENCES chat(id),
    PRIMARY KEY(user_id, chat_id)
);

CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    text VARCHAR(4000) NOT NULL,
    owner_id INTEGER REFERENCES users(id),
    chat_id INTEGER REFERENCES chat(id)
);

CREATE TABLE token (
    id SERIAL PRIMARY KEY,
    token VARCHAR(256) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true
);