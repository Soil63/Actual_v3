import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  imports: [CommonModule, FormsModule] // Added FormsModule for [(ngModel)] support
})
export class LoginComponent {
  messages: string[] = [];
  user = { isAuthenticated: false }; // Example user structure
  formFields = [
    { name: 'email', label: 'Email', type: 'email', value: '' },
    { name: 'password', label: 'Mot de passe', type: 'password', value: '' }
  ];

  onSubmit() {
    // Logic for login submission
    console.log('Form submitted', this.formFields);
  }
}
