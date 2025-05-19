import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  imports: [CommonModule, FormsModule] // Added FormsModule for [(ngModel)] support
})
export class RegisterComponent {
  formFields = [
    { name: 'email', label: 'Email', type: 'email', value: '' },
    { name: 'nom', label: 'Nom', type: 'text', value: '' },
    { name: 'prenom', label: 'Prénom', type: 'text', value: '' },
    { name: 'date_naiss', label: 'Date de naissance', type: 'date', value: '' },
    { name: 'password', label: 'Mot de passe', type: 'password', value: '' },
    { name: 'confirm_password', label: 'Confirmer le mot de passe', type: 'password', value: '' }
  ];
  messages: any;

  onSubmit() {
    console.log('Formulaire soumis', this.formFields);
  }
}
