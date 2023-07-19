export interface Message {
  chat_id: number;
  owner_id: number;
  text: string;
  id: number;
}

export interface MessageSend {
  chat_id: number;
  owner_id: number;
  text: string;
}
