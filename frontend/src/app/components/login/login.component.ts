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
}
