import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.html',
  styleUrls: ['./user-list.css'],
  standalone: false
})
export class UserListComponent implements OnInit {
  users: any[] = [];
  searchTerm: string = '';
  selectedRole: string = '';
  allRoles: string[] = [];
  loading = true;
  error = '';

  currentPage: number = 1;
  pageSize: number = 5;

  constructor(public authService: AuthService) {}

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.authService.getUsers().subscribe({
      next: data => {
        this.users = data;
        this.loading = false;
        this.allRoles = Array.from(new Set(this.users.map(u => u.role)));
      },
      error: () => {
        this.error = 'Failed to load users';
        this.loading = false;
      }
    });
  }

  filteredUsers(): any[] {
    return this.users.filter(u => {
      const matchesSearch =
        !this.searchTerm ||
        u.full_name?.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        u.email?.toLowerCase().includes(this.searchTerm.toLowerCase());
      const matchesRole = !this.selectedRole || u.role === this.selectedRole;
      return matchesSearch && matchesRole;
    });
  }

  paginatedUsers(): any[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.filteredUsers().slice(start, start + this.pageSize);
  }

  totalPages(): number {
    return Math.ceil(this.filteredUsers().length / this.pageSize) || 1;
  }

  nextPage() {
    if (this.currentPage < this.totalPages()) this.currentPage++;
  }

  prevPage() {
    if (this.currentPage > 1) this.currentPage--;
  }

  editUser(userId: string) {
    this.authService.editUser(userId);
  }

  deleteUser(userId: string) {
    if (confirm('Are you sure you want to delete this user?')) {
      this.authService.deleteUser(userId);
      this.users = this.users.filter(u => u.id !== userId);
    }
  }

  exportSingleUser(user: any) {
    const headers = ['Full Name', 'Email', 'Role'];
    const rows = [[user.full_name || '', user.email || '', user.role || '']];
    let csvContent = headers.join(',') + '\n';
    rows.forEach(r => csvContent += r.join(',') + '\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.setAttribute('download', `${user.full_name || 'user'}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}
