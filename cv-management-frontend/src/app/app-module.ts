import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


import { AppRoutingModule } from './app-routing-module';
import { App } from './app';

import { CvListComponent } from './cv-list/cv-list.component';
import { CvDetailComponent } from './cv-detail/cv-detail';
import { LoginComponent } from './auth/login/login';
import { RegisterComponent } from './auth/register/register';
import { CvFormComponent } from './cv-form/cv-form';
import { DashboardComponent } from './dashboard/dashboard';
import { UserListComponent } from './user-list/user-list';
import { AnalyticsComponent } from './analytics/analytics';

@NgModule({
  declarations: [
    App,
    CvListComponent,
    CvDetailComponent,
    LoginComponent,
    RegisterComponent,
    CvFormComponent,
    DashboardComponent,
    UserListComponent,
    AnalyticsComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    
    
  ],
  providers: [],
  bootstrap: [App]
})
export class AppModule {}
