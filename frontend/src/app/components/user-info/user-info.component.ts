import { Component, OnInit } from '@angular/core';
import { AccountService } from 'src/app/services/account.service';
import { UserInfo } from 'src/app/models/user-info';
import {Observable, Subject, takeUntil} from "rxjs";
import {takeUntilDestroyed} from "@angular/core/rxjs-interop";

@Component({
  selector: 'app-user-info',
  templateUrl: './user-info.component.html',
  styleUrls: ['./user-info.component.css']
})
export class UserInfoComponent implements OnInit {
  currentUser?: UserInfo;

  private user$ = new Observable<UserInfo>


  constructor(private accountService: AccountService) {
    this.user$ = this.accountService.userInfo.pipe(takeUntilDestroyed())
  }

  ngOnInit(): void {
    this.user$.subscribe(user => {
      if (user) {
        this.currentUser =  user;
      }
    });
    this.accountService.reload();
  }

}
