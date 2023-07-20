import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { UserInfoComponent } from './components/user-info/user-info.component';
import { RefreshTokenComponent } from './components/refresh-token/refresh-token.component';
import { FormsModule } from "@angular/forms";
import { AppRoutingModule } from "./app-routing.module";
import {HttpClientModule} from "@angular/common/http";
import {InterceptorsModule} from "./interceptors/interceptor.module";
import { MainPageComponent } from './pages/main-page/main-page.component';
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import {MatButtonModule} from "@angular/material/button";
import {MatCardModule} from "@angular/material/card";
import { ChatListComponent } from './components/chat-list/chat-list.component';
import { ChatComponent } from './components/chat/chat.component';
import {MatListModule} from "@angular/material/list";
import { LogoutComponent } from './components/logout/logout.component';


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    UserInfoComponent,
    RefreshTokenComponent,
    MainPageComponent,
    ChatListComponent,
    ChatComponent,
    LogoutComponent
  ],
    imports: [
        BrowserModule,
        FormsModule,
        AppRoutingModule,
        HttpClientModule,
        InterceptorsModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        MatCardModule,
        MatListModule,
    ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
