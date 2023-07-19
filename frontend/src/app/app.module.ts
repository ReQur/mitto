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


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    UserInfoComponent,
    RefreshTokenComponent,
    MainPageComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule,
    InterceptorsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
