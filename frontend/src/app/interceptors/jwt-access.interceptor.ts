import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable } from 'rxjs';
import {AccountService} from "../services/account.service";

@Injectable()
export class JwtAccessInterceptor implements HttpInterceptor {
  constructor(private account: AccountService) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const accessToken = this.account.access_token;

    if (accessToken != '') {
      request = request.clone({
        setHeaders: { 'Authorization': `Bearer ${accessToken} ` },
      });
    }
    request = request.clone({
      setHeaders: { 'Content-Type': `application/x-www-form-urlencoded` },
      withCredentials: true
    });

    return next.handle(request);
  }
}
