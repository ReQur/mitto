import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {HTTP_INTERCEPTORS} from "@angular/common/http";
import {JwtAccessInterceptor} from "./jwt-access.interceptor";



@NgModule({
  declarations: [],
  imports: [CommonModule],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: JwtAccessInterceptor,
      multi: true,
    },
  ],
})
export class InterceptorsModule {}
