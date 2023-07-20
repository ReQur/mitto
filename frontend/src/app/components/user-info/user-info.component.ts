import { Component, OnInit } from '@angular/core';
import { AccountService } from 'src/app/services/account.service';
import { UserInfo } from 'src/app/models/user-info';
import {Subject, takeUntil} from "rxjs";

@Component({
  selector: 'app-user-info',
  templateUrl: './user-info.component.html',
  styleUrls: ['./user-info.component.css']
})
export class UserInfoComponent implements OnInit {
  currentUser?: UserInfo;

  private unsubscribe$ = new Subject<void>();


  constructor(private accountService: AccountService) { }

  ngOnInit(): void {
    this.accountService.userInfo.pipe(
      takeUntil(this.unsubscribe$)
    ).subscribe(currentUser => {
      if (currentUser) {
        this.currentUser =  currentUser;
      }
    });
    this.accountService.reload();
  }

  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }
}
