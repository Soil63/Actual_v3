import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';
  nb_benevoles: number = 0; // Ajout de la propriété avec une valeur par défaut

  constructor() {
    // Vous pouvez initialiser nb_benevoles dynamiquement ici si nécessaire
    this.nb_benevoles = 10; // Exemple de valeur
  }
}
