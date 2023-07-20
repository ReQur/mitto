import { Component, OnInit } from '@angular/core';
import {ChatService} from "src/app/services/chat.service";
import {Chat} from "../../models/chat";
import {Subject, takeUntil} from "rxjs";

@Component({
  selector: 'app-chat-list',
  templateUrl: './chat-list.component.html',
  styleUrls: ['./chat-list.component.css']
})
export class ChatListComponent implements OnInit {
  private unsubscribe$ = new Subject<void>();

  newMessageText: string = '';
  recipientId: string = '';

  constructor(private chatService: ChatService) { }
  chats: Chat[] = []
  ngOnInit(): void {
    this.chatService.chats.pipe(
      takeUntil(this.unsubscribe$)
    ).subscribe(chats => {
      this.chats = chats
    });
  }

  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  getChats(): void {
    this.chatService.reload();
  }

  selectChat(id: number) {
    this.chatService.current_chat_id = id
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
