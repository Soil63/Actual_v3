import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  nbBenevoles = 42; // Exemple de données
}
/*import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'] // Corrected 'styleUrl' to 'styleUrls' for proper Angular syntax
})
export class HomeComponent {

}*/
