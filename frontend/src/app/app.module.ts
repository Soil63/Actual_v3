import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { HomeComponent } from './components/home/home.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { EspacePersoComponent } from './components/espace-perso/espace-perso.component';
import { MessagerieComponent } from './components/messagerie/messagerie.component';
import { ModifBenevComponent } from './components/modif-benev/modif-benev.component';

@NgModule({
  declarations: [],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule, // Import HttpClientModule for communication with the back-end
    FormsModule, // Added FormsModule for template-driven forms
    LoginComponent, // Import LoginComponent as it is standalone
    AppComponent, // Import AppComponent as it is standalone
    HomeComponent, // Import HomeComponent as it is standalone
    RegisterComponent, // Import RegisterComponent as it is standalone
    EspacePersoComponent, // Import EspacePersoComponent as it is standalone
    MessagerieComponent, // Import MessagerieComponent as it is standalone
    ModifBenevComponent // Import ModifBenevComponent as it is standalone
  ],
  providers: [],
  // Removed bootstrap array as AppComponent is a standalone component
})
export class AppModule { }