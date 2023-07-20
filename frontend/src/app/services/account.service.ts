import {HttpClient, HttpParams} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {BehaviorSubject, Observable, tap} from 'rxjs';
import { Token } from '../models/token';
import { UserInfo } from '../models/user-info';

@Injectable({
  providedIn: 'root'
})
export class AccountService {
  private API_URL = 'http://localhost:8000'; // Replace with your API url
  private _userInfo: BehaviorSubject<UserInfo> = new BehaviorSubject<UserInfo>(this.retrieveUserInfo());

  constructor(private http: HttpClient) { }

  get userInfo(): Observable<UserInfo> {
    return this._userInfo.asObservable();
  }

  login(username: string, password: string): Observable<Token> {
    let body = new HttpParams();
    body = body.set('username', username);
    body = body.set('password', password);

    return this.http.post<Token>(`${this.API_URL}/account/login`, body,
      {headers: {'Content-Type': `application/x-www-form-urlencoded`}}
    ).pipe(
      tap(token => {
        this.access_token = token.access_token
        this.reload()
      })
    );
  }

  get access_token(): string {
    return localStorage.getItem('access_token') ?? "none";
  }

  set access_token(access_token: string) {
    localStorage.setItem('access_token', access_token);
  }

  private retrieveUserInfo(): UserInfo {
    return JSON.parse(localStorage.getItem('user_info') ?? "{}");
  }

  reload(): void {
    this.getUserInfo().subscribe(info => {
      localStorage.setItem('user_info', JSON.stringify(info));
      this._userInfo.next(info);
    })
  }


  getUserInfo(): Observable<UserInfo> {
    return this.http.get<UserInfo>(`${this.API_URL}/account/me`);
  }

  refreshToken(): Observable<Token> {
    return this.http.get<Token>(`${this.API_URL}/account/refresh`,
      {headers: {'Content-Type': `application/x-www-form-urlencoded`}}
    ).pipe(tap(token => {
      this.access_token = token.access_token
    }));
  }
}
