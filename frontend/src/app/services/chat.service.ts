import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {Message, MessageSend} from "../models/message";
import {Chat} from "../models/chat";

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  private apiUrl = 'http://localhost:8000';  // Change this to your actual API URL

  constructor(private http: HttpClient) { }

  set current_chat_id(id: number) {
    localStorage.setItem('current_chat_id', id.toString());
  }

  get current_chat_id(): number {
    return Number(localStorage.getItem('current_chat_id'));
  }
  getChats(): Observable<Chat[]> {
    return this.http.get<Chat[]>(`${this.apiUrl}/chat/`);
  }

  getMessages(chatId: number): Observable<Message[]> {
    return this.http.get<Message[]>(`${this.apiUrl}/chat/${chatId}/messages`);
  }

  sendMessage(chatId: number, ownerId: number, text: string): Observable<Message> {
    return this.http.post<Message>(`${this.apiUrl}/chat/send-message`, {
      "text": text,
      "chat_id": chatId,
      "owner_id": ownerId
    });
  }

  initiateChat(recipientId: number, text: string): Observable<Message> {
    return this.http.post<Message>(`${this.apiUrl}/chat/initiate/${recipientId}`, {"text": text});
  }

}
