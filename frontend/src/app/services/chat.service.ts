import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {BehaviorSubject, combineLatest, map, Observable, take, takeUntil, tap} from 'rxjs';
import {Message, MessageSend} from "../models/message";
import {Chat} from "../models/chat";
import {AccountService} from "./account.service";

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private _chats: BehaviorSubject<Chat[]> = new BehaviorSubject<Chat[]>([]);
  private _currentChatId: BehaviorSubject<number> = new BehaviorSubject<number>(this.retrieveChatId());

  get chats(): Observable<Chat[]> {
    return this._chats.asObservable();
  }

  get currentChat(): Observable<Chat | undefined> {
    return combineLatest([this._chats, this._currentChatId]).pipe(
      map(([chats, currentChatId]) => chats.find(chat => chat.id === currentChatId))
    );
  }

  set currentChatId(id: number) {
    localStorage.setItem('current_chat_id', id.toString());
    this._currentChatId.next(id);
  }

  private apiUrl = 'http://localhost:8000';  // Change this to your actual API URL


  constructor(private http: HttpClient, private accountService: AccountService) {
    this.accountService.userInfo.subscribe(_ => {
      this.reload();
      this.chats.subscribe( _chat => {
          this.currentChatId = _chat[0].id ?? -1
        }
      )
    });
    this.accountService.isNotAuthed$.subscribe(() => {
      this.clear()
    })
  }


  reload(): void {
    this.getChats().subscribe(c => {
      c.forEach((_chat) => {
         this.getMessages(_chat.id).subscribe(messages => {
             _chat.messages = messages;
           })
      })
      this._chats.next(c);
    })
  }

  clear(): void {
    this._chats.next([])
  }

  private retrieveChatId(): number {
    return Number(localStorage.getItem('current_chat_id')) || 0;
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
    }).pipe(
      tap(_ => {
        this.reload()
      })
    );
  }

  initiateChat(recipientId: number, text: string): Observable<Message> {
    return this.http.post<Message>(`${this.apiUrl}/chat/initiate/${recipientId}`, {"text": text}).pipe(
      tap(_ => {
        this.reload()
      })
    );
  }

}
