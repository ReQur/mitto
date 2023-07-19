import { Component, OnInit } from '@angular/core';
import {ChatService} from "src/app/services/chat.service";
import {Chat} from "../../models/chat";

@Component({
  selector: 'app-chat-list',
  templateUrl: './chat-list.component.html',
  styleUrls: ['./chat-list.component.css']
})
export class ChatListComponent implements OnInit {
  chats: Chat[] = []

  newMessageText: string = '';
  recipientId: string = '';

  constructor(private chatService: ChatService) { }

  ngOnInit(): void {
    this.getChats();
  }

  getChats(): void {
    this.chatService.getChats().subscribe(chats => this.chats = chats);
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
