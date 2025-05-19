import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-saisie',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './saisie.component.html',
  styleUrls: ['./saisie.component.css']
})
export class SaisieComponent {
  constraints = '';
  preferences = '';

  items = [
    { name: 'Item 1', value: 'Value 1' },
    { name: 'Item 2', value: 'Value 2' },
    { name: 'Item 3', value: 'Value 3' }
  ];
formFields: any;

  onSubmit() {
    console.log('Contraintes:', this.constraints);
    console.log('Préférences:', this.preferences);
    console.log('Form submitted with items:', this.items);
  }
}
