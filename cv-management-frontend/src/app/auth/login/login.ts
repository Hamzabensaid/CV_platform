import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';
import { LoginRequest } from '../../models/user-model';

@Component({
  selector: 'app-login',
  templateUrl: './login.html',
  styleUrls: ['./login.css'],
  standalone: false
})
export class LoginComponent {
  loginUser: LoginRequest = { email: '', password: '' };
  error: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  login() {
    if (!this.loginUser.email || !this.loginUser.password) {
      this.error = 'Please fill in all fields';
      return;
    }

    this.authService.login(this.loginUser).subscribe({
      next: (res) => {
        if (res.access_token) { // FastAPI returns { "access_token": "...", "token_type": "bearer" }
          this.authService.setToken(res.access_token);
          this.router.navigate(['/cvs']); // redirect after login
        }
      },
      error: () => {
        this.error = 'Invalid credentials';
      }
    });
  }
}
