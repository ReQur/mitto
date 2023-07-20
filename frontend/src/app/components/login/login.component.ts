import { Component } from '@angular/core';
import { AccountService } from 'src/app/services/account.service';
import { MatFormFieldModule } from '@angular/material/form-field';
import {UserInfo} from "../../models/user-info";
import {Subject, takeUntil} from "rxjs";

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


  login(): void {
    // @ts-ignore
    this.accountService.login(this.username, this.password).subscribe(token => {
      console.log(token);

    });
  }

}
