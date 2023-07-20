import {Message} from "./message";

export interface Chat {
  user_ids: [number];
  messages: Message[];
  id: number;
}
