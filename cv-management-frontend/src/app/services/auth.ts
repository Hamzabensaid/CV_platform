import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/v1'; // base path
  private currentUserSubject = new BehaviorSubject<any>(null);

  constructor(public http: HttpClient) {
    if (this.isBrowser()) {
      const storedUser = localStorage.getItem('currentUser');
      if (storedUser) {
        this.currentUserSubject.next(JSON.parse(storedUser));
      }
    }
  }

  private isBrowser(): boolean {
    return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
  }

  // ---- Login
  login(data: { email: string; password: string }): Observable<any> {
    const body = new HttpParams()
      .set('username', data.email) // FastAPI OAuth2 expects "username"
      .set('password', data.password);

    return this.http.post<any>(`${this.apiUrl}/login`, body, {
      headers: new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' })
    }).pipe(
      tap(res => {
        this.setToken(res.access_token);
        this.fetchProfile().subscribe();
      })
    );
  }

  // ---- Register
  register(data: { full_name: string; email: string; password: string }): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/register`, data);
  }

  // ---- Token management
  setToken(token: string) {
    if (this.isBrowser()) {
      localStorage.setItem('token', token);
    }
  }

  getToken(): string | null {
    return this.isBrowser() ? localStorage.getItem('token') : null;
  }

  logout() {
    if (this.isBrowser()) {
      localStorage.removeItem('token');
      localStorage.removeItem('currentUser');
    }
    this.currentUserSubject.next(null);
  }

  // ---- Current user
  fetchProfile(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/me`, {
      headers: new HttpHeaders({ 'Authorization': `Bearer ${this.getToken()}` })
    }).pipe(
      tap(user => {
        if (this.isBrowser()) {
          localStorage.setItem('currentUser', JSON.stringify(user));
        }
        this.currentUserSubject.next(user);
      })
    );
  }

  get currentUser() {
    return this.currentUserSubject.asObservable();
  }

  // ---- Get all users
  getUsers(skip: number = 0, limit: number = 10): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/users`, {
      headers: new HttpHeaders({ 'Authorization': `Bearer ${this.getToken()}` }),
      params: new HttpParams().set('skip', skip.toString()).set('limit', limit.toString())
    });
  }

  // ---- Placeholder edit/delete methods
  editUser(userId: string) {
    alert('Edit user: ' + userId);
  }

  deleteUser(userId: string) {
    if (!confirm('Are you sure you want to delete this user?')) return;
    alert('Delete user: ' + userId);
  }
}
