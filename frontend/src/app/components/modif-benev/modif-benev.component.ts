import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-modif-benev',
  templateUrl: './modif-benev.component.html',
  styleUrls: ['./modif-benev.component.css'],
  imports: [CommonModule, FormsModule] // Added FormsModule for [(ngModel)] support
})
export class ModifBenevComponent {
  formFields = [
    { name: 'nom', label: 'Nom', type: 'text', value: '' },
    { name: 'prenom', label: 'Prénom', type: 'text', value: '' },
    { name: 'email', label: 'Email', type: 'email', value: '' },
    { name: 'date_naiss', label: 'Date de naissance', type: 'date', value: '' },
    { name: 'phone_number', label: 'Numéro de téléphone', type: 'text', value: '' },
    { name: 'address', label: 'Adresse', type: 'text', value: '' }
  ];

  onSubmit() {
    console.log('Formulaire soumis', this.formFields);
  }
}
