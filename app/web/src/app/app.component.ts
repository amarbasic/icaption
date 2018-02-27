import { Component } from '@angular/core';
import { AuthService } from './services/auth/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styles: []
})
export class AppComponent {

  constructor(private authService: AuthService) {
  }

  authenticated() {
    return this.authService.authenticated();
  }
}
