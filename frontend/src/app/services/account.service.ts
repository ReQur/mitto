import {HttpClient, HttpParams} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {BehaviorSubject, distinctUntilChanged, map, Observable, ReplaySubject, tap} from 'rxjs';
import { Token } from '../models/token';
import { UserInfo } from '../models/user-info';

@Injectable({
  providedIn: 'root'
})
export class AccountService {
  private API_URL = 'http://localhost:8000'; // Replace with your API url
  private _userInfo: BehaviorSubject<UserInfo> = new BehaviorSubject<UserInfo>(this.retrieveUserInfo());
  private isAuthedSource$ = new ReplaySubject<boolean>(1);

  readonly isAuthed$: Observable<boolean> = this.isAuthedSource$.asObservable().pipe(distinctUntilChanged());
  readonly isNotAuthed$: Observable<boolean> = this.isAuthed$.pipe(map((state) => !state));


  constructor(private http: HttpClient) {
    if (this.access_token != "none"){
      this.isAuthedSource$.next(true);
      this.reload();
    }
    else {
      this.isAuthedSource$.next(false);
    }
  }

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
        this.isAuthedSource$.next(true);
      })
    );
  }

  logout(): void {
    localStorage.clear()
    this.isAuthedSource$.next(false);
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
