import { Component } from '@angular/core';
import { AccountService } from 'src/app/services/account.service';

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

  constructor(private accountService: AccountService) { }

  login(): void {
    // @ts-ignore
    this.accountService.login(this.username, this.password).subscribe(token => {
      console.log(token);

    });
  }

  get authorized(): boolean {
    return this.accountService.access_token != ''
  }

  get user_email(): string {
    return this.accountService.user_info.email
  }


}
