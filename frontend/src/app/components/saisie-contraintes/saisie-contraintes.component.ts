import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-saisie-contraintes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './saisie-contraintes.component.html',
  styleUrls: ['./saisie-contraintes.component.css']
})
export class SaisieContraintesComponent {
  items = [
    { name: 'Item 1', value: 'Value 1' },
    { name: 'Item 2', value: 'Value 2' },
    { name: 'Item 3', value: 'Value 3' }
  ];
formFields: any;

  onSubmit() {
    console.log('Form submitted with items:', this.items);
  }
}
