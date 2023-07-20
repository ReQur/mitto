import { Component } from '@angular/core';
import {AccountService} from "../../services/account.service";

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.css']
})
export class MainPageComponent {
  constructor(public accountService: AccountService) {
  }
}
