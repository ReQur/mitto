import { Component } from '@angular/core';
import { AccountService } from 'src/app/services/account.service';
import { Token } from 'src/app/models/token';

@Component({
  selector: 'app-refresh-token',
  templateUrl: './refresh-token.component.html',
  styleUrls: ['./refresh-token.component.css']
})
export class RefreshTokenComponent {
  // @ts-ignore
  token: Token;

  constructor(private accountService: AccountService) { }

  refreshToken(): void {
    this.accountService.refreshToken().subscribe(token => {
      this.token = token;
      // Here you would normally store the new token
    });
  }
}
