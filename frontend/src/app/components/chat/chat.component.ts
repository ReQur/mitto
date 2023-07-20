import { Component, OnInit, Input } from '@angular/core';
import { ChatService } from "src/app/services/chat.service";
import { AccountService } from "src/app/services/account.service";
import {Message} from "../../models/message";
import {Subject, takeUntil} from "rxjs";
import {Chat} from "../../models/chat";

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  currentChat?: Chat
  newMessageText: string = '';

  private unsubscribe$ = new Subject<void>();

  constructor(private chatService: ChatService, private accountService: AccountService) { }
  ngOnInit(): void {
    this.chatService.currentChat.pipe(
      takeUntil(this.unsubscribe$)
    ).subscribe(currentChat => {
      if (currentChat) {
        this.currentChat =  currentChat;
      }
    });
    this.chatService.reload();
  }

  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }


  sendMessage(): void {
    if (this.currentChat){
      this.chatService.sendMessage(this.currentChat.id, this.accountService.user_info.id, this.newMessageText)
        // @ts-ignore
        .subscribe(message => {
          this.newMessageText = '';
        });
    }
  }
}
