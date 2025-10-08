import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';
import { RegisterRequest } from '../../models/user-model';

@Component({
  selector: 'app-register',
  templateUrl: './register.html',
  styleUrls: ['./register.css'],
  standalone: false
})
export class RegisterComponent {
  registerUser: RegisterRequest = { full_name: '', email: '', password: '' };
  error: string = '';
  success: string = '';
  showPassword = false; // toggle password visibility

  constructor(private authService: AuthService, private router: Router) {}

  togglePassword() {
    this.showPassword = !this.showPassword;
  }

  register() {
    this.error = '';
    this.success = '';

    if (!this.registerUser.full_name || !this.registerUser.email || !this.registerUser.password) {
      this.error = 'Please fill in all fields';
      return;
    }

    this.authService.register(this.registerUser).subscribe({
      next: (res) => {
        if (res.id) {
          this.success = 'Registration successful! Redirecting to login...';
          setTimeout(() => this.router.navigate(['/login']), 1500);
        }
      },
      error: (err) => {
        this.error = err?.error?.detail || 'Registration failed. Please try again.';
      }
    });
  }
}
