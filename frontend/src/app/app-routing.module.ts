import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { UserInfoComponent } from './components/user-info/user-info.component';
import { RefreshTokenComponent } from './components/refresh-token/refresh-token.component';
import { MainPageComponent } from "./pages/main-page/main-page.component";

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' }, // Redirect to `login` by default
  { path: 'login', component: LoginComponent },
  { path: 'me', component: UserInfoComponent },
  { path: 'refresh', component: RefreshTokenComponent },
  { path: 'main-page', component: MainPageComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
