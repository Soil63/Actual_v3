import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-messagerie',
  templateUrl: './messagerie.component.html',
  styleUrls: ['./messagerie.component.css'],
  imports: [CommonModule, FormsModule] // Added FormsModule for [(ngModel)] support
})
export class MessagerieComponent {
  messages = [
    { sender: 'User1', content: 'Bonjour, comment ça va ?', timestamp: new Date() },
    { sender: 'User2', content: 'Je voulais te parler du projet.', timestamp: new Date() }
  ];

  newMessage = '';

  sendMessage() {
    if (this.newMessage.trim()) {
      this.messages.push({
        sender: 'Moi',
        content: this.newMessage,
        timestamp: new Date()
      });
      this.newMessage = '';
    }
  }
}
