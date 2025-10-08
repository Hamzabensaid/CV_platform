import { Component, OnInit } from '@angular/core';
import { CvService } from '../services/cv';
import { CV } from '../models/cv-model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-cv-list',
  templateUrl: './cv-list.component.html',
  styleUrls: ['./cv-list.component.css'],
  standalone: false
})
export class CvListComponent implements OnInit {
  cvs: CV[] = [];
  loading = true;
  error = '';

  // Filters
  searchTerm: string = '';
  selectedSkill: string = '';
  selectedLocation: string = '';
  allSkills: string[] = [];
  allLocations: string[] = [];

  // Pagination
  currentPage: number = 1;
  pageSize: number = 5;

  // Sorting
  sortField: keyof CV | '' = '';
  sortDirection: 'asc' | 'desc' = 'asc';

  constructor(private cvService: CvService, private router: Router) {}

  ngOnInit(): void {
    this.loadCVs();
  }

  loadCVs(): void {
    this.cvService.getCVs().subscribe({
      next: data => {
        this.cvs = data;
        this.loading = false;

        // Collect unique skills and locations
        this.allSkills = Array.from(new Set(this.cvs.flatMap(cv => cv.skills || [])));
        this.allLocations = Array.from(new Set(this.cvs.map(cv => cv.location || '').filter(loc => loc)));
      },
      error: err => {
        this.error = 'Failed to load CVs';
        console.error(err);
        this.loading = false;
      }
    });
  }

  // Filtering + Sorting
  filteredCVs(): CV[] {
    let result = this.cvs.filter(cv => {
      const matchesSearch =
        !this.searchTerm ||
        cv.full_name?.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        cv.email?.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        cv.skills?.some(skill => skill.toLowerCase().includes(this.searchTerm.toLowerCase()));

      const matchesSkill = !this.selectedSkill || cv.skills?.includes(this.selectedSkill);
      const matchesLocation = !this.selectedLocation || cv.location === this.selectedLocation;

      return matchesSearch && matchesSkill && matchesLocation;
    });

    // Sorting
    if (this.sortField) {
      result = result.sort((a: any, b: any) => {
        const valueA = (a[this.sortField] || '').toString().toLowerCase();
        const valueB = (b[this.sortField] || '').toString().toLowerCase();

        if (valueA < valueB) return this.sortDirection === 'asc' ? -1 : 1;
        if (valueA > valueB) return this.sortDirection === 'asc' ? 1 : -1;
        return 0;
      });
    }

    return result;
  }

  // Sorting toggle
  sortBy(field: keyof CV): void {
    if (this.sortField === field) {
      this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortField = field;
      this.sortDirection = 'asc';
    }
  }

  // Pagination
  paginatedCVs(): CV[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.filteredCVs().slice(start, start + this.pageSize);
  }

  totalPages(): number {
    return Math.ceil(this.filteredCVs().length / this.pageSize) || 1;
  }

  nextPage() {
    if (this.currentPage < this.totalPages()) this.currentPage++;
  }

  prevPage() {
    if (this.currentPage > 1) this.currentPage--;
  }

  // Navigation actions
  addNewCV() {
    this.router.navigate(['/cvs/new']);
  }

  viewCV(cv: CV) {
    if (cv.id) this.router.navigate(['/cvs', cv.id]);
    else alert('This CV cannot be opened because it has no ID.');
  }

  deleteCV(id: string) {
    if (confirm('Are you sure you want to delete this CV?')) {
      this.cvService.deleteCV(id).subscribe(() => {
        this.cvs = this.cvs.filter(c => c.id !== id);
      });
    }
  }

  exportSingleCV(cv: CV) {
    const headers = ['Full Name', 'Email', 'Location', 'Skills'];
    const rows = [[
      cv.full_name || '',
      cv.email || '',
      cv.location || '',
      (cv.skills || []).join(', ')
    ]];

    let csvContent = headers.join(',') + '\n';
    rows.forEach(r => csvContent += r.join(',') + '\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.setAttribute('download', `${cv.full_name || 'cv'}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}
