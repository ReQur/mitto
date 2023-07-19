import {HttpClient, HttpParams} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Observable, tap} from 'rxjs';
import { Token } from '../models/token';
import { UserInfo } from '../models/user-info';

@Injectable({
  providedIn: 'root'
})
export class AccountService {
  private API_URL = 'http://localhost:8000'; // Replace with your API url

  constructor(private http: HttpClient) { }

  login(username: string, password: string): Observable<Token> {
    let body = new HttpParams();
    body = body.set('username', username);
    body = body.set('password', password);

    return this.http.post<Token>(`${this.API_URL}/account/login`, body).pipe(
      tap(token => {
        this.access_token = token.access_token
      })
    );
  }

  get access_token(): string {
    return localStorage.getItem('access_token') ?? "none";
  }

  set access_token(access_token: string) {
    localStorage.setItem('access_token', access_token);
  }

  get user_info(): UserInfo {
    return JSON.parse(localStorage.getItem('user_info') ?? "{}");
  }

  set user_info(info: UserInfo) {
    localStorage.setItem('user_info', JSON.stringify(info));
  }

  getUserInfo(): Observable<UserInfo> {
    return this.http.get<UserInfo>(`${this.API_URL}/account/me`).pipe(
      tap(info => {
          this.user_info = info
        })
    );
  }

  refreshToken(): Observable<Token> {
    return this.http.get<Token>(`${this.API_URL}/account/refresh`).pipe(tap(token => {
      this.access_token = token.access_token
    }));
  }
}
