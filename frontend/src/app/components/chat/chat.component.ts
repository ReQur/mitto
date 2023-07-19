import { Component, OnInit, Input } from '@angular/core';
import { ChatService } from "src/app/services/chat.service";
import { AccountService } from "src/app/services/account.service";
import {Message} from "../../models/message";

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  messages: Message[] = [];
  newMessageText: string = '';

  constructor(private chatService: ChatService, private accountService: AccountService) { }

  ngOnInit(): void {
    this.getMessages();
  }

  getMessages(): void {
    this.chatService.getMessages(this.chatService.current_chat_id).subscribe(messages => this.messages = messages);
  }

  sendMessage(): void {
    this.chatService.sendMessage(this.chatService.current_chat_id, this.accountService.user_info.id, this.newMessageText)
      // @ts-ignore
      .subscribe(message => {
        this.messages.push(message);
        this.newMessageText = '';
      });
  }
}
