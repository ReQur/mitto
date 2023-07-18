import { Component, OnInit } from '@angular/core';
import { AccountService } from 'src/app/services/account.service';
import { UserInfo } from 'src/app/models/user-info';

@Component({
  selector: 'app-user-info',
  templateUrl: './user-info.component.html',
  styleUrls: ['./user-info.component.css']
})
export class UserInfoComponent implements OnInit {
  // @ts-ignore
  userInfo: UserInfo;

  constructor(private accountService: AccountService) { }

  ngOnInit(): void {
    this.accountService.getUserInfo().subscribe(userInfo => {
      this.userInfo = userInfo;
    });
  }
}
