import { Component } from '@angular/core';
import { AccountService } from 'src/app/services/account.service';
import { MatFormFieldModule } from '@angular/material/form-field';
import {UserInfo} from "../../models/user-info";
import {Observable, Subject, takeUntil} from "rxjs";
import {takeUntilDestroyed} from "@angular/core/rxjs-interop";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  // @ts-ignore
  username: string;
  // @ts-ignore
  password: string;
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


  login(): void {
    // @ts-ignore
    this.accountService.login(this.username, this.password).subscribe(token => {
      console.log(token);

    });
  }

}
