import { Component, OnInit, Input } from '@angular/core';
import { ChatService } from "src/app/services/chat.service";
import { AccountService } from "src/app/services/account.service";
import {Message} from "../../models/message";
import {Observable, Subject, takeUntil} from "rxjs";
import {Chat} from "../../models/chat";
import {UserInfo} from "../../models/user-info";
import {takeUntilDestroyed} from "@angular/core/rxjs-interop";

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  currentChat?: Chat
  currentUser?: UserInfo;
  newMessageText: string = '';

  private chat$ = new Observable<Chat | undefined>
  private user$ = new Observable<UserInfo>
  private isNotAuthed$ = new Observable<boolean>

  constructor(private chatService: ChatService, private accountService: AccountService) {
    this.chat$ = this.chatService.currentChat.pipe(takeUntilDestroyed())
    this.user$ = this.accountService.userInfo.pipe(takeUntilDestroyed())
    this.isNotAuthed$ = this.accountService.isNotAuthed$.pipe(takeUntilDestroyed())
  }
  ngOnInit(): void {
    this.chat$.subscribe(chat => {
      if (chat) {
        this.currentChat =  chat;
      }
    });
    this.user$.subscribe(user => {
      if (user) {
        this.currentUser =  user;
      }
    });
    this.isNotAuthed$.subscribe(_ => {
      this.currentChat = undefined
    });
    this.chatService.reload();
  }

  sendMessage(): void {
    if (this.currentChat && this.currentUser){
      this.chatService.sendMessage(this.currentChat.id, this.currentUser.id, this.newMessageText)
        // @ts-ignore
        .subscribe(message => {
          this.newMessageText = '';
        });
    }

  }
}
