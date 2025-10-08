import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { CvListComponent } from './cv-list/cv-list.component';
import { CvDetailComponent } from './cv-detail/cv-detail';
import { CvFormComponent } from './cv-form/cv-form';
import { LoginComponent } from './auth/login/login';
import { RegisterComponent } from './auth/register/register';
import { DashboardComponent } from './dashboard/dashboard';
import { UserListComponent } from './user-list/user-list';
import { AnalyticsComponent } from './analytics/analytics';



const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  
  { path: 'dashboard', component: DashboardComponent },
  { path: 'analytics', component: AnalyticsComponent },
  { path: 'cvs', component: CvListComponent },

  // New CV route must come BEFORE the id route
  { path: 'cvs/new', component: CvFormComponent }, 
  { path: 'cvs/:id', component: CvDetailComponent },

  { path: 'users', component: UserListComponent },
  { path: '**', redirectTo: '/cvs' }
];
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
