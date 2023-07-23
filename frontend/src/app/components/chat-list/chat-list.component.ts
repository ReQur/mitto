import { Component, OnInit } from '@angular/core';
import {ChatService} from "src/app/services/chat.service";
import {Chat} from "../../models/chat";
import {Observable, Subject, takeUntil} from "rxjs";
import {takeUntilDestroyed} from "@angular/core/rxjs-interop";

@Component({
  selector: 'app-chat-list',
  templateUrl: './chat-list.component.html',
  styleUrls: ['./chat-list.component.css'],
})
export class ChatListComponent implements OnInit {

  newMessageText: string = '';
  recipientId: string = '';

  chats$: Observable<Chat[]>
  constructor(private chatService: ChatService) {
    this.chats$ = this.chatService.chats.pipe(takeUntilDestroyed())
  }
  chats: Chat[] = []
  ngOnInit(): void {
    this.chats$.subscribe(chats => {
      this.chats = chats
    });
    this.chatService.reload();
  }


  getChats(): void {
    this.chatService.reload();
  }

  selectChat(id: number) {
    this.chatService.currentChatId = id
  }

  initiateChat(): void {
    this.chatService.initiateChat(Number(this.recipientId), this.newMessageText)
      // @ts-ignore
      .subscribe(message => {
        this.newMessageText = '';
        this.recipientId = '';
      });
  }

}
