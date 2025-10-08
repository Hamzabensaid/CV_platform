import { Component, OnInit } from '@angular/core';
import { CvService } from '../services/cv';
import { CV } from '../models/cv-model';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css'],
  standalone: false
})
export class DashboardComponent implements OnInit {
  loading = true;
  error = '';

  dashboard: any = {};
  cvs: CV[] = [];

  topSkills: { skill: string; count: number }[] = [];
  topLocations: { location: string; count: number }[] = [];
  educationDistribution: { degree: string; count: number }[] = [];
  experienceStats: { min_years: number; max_years: number; avg_years: number } = { min_years: 0, max_years: 0, avg_years: 0 };

  constructor(
    private cvService: CvService,
    private router: Router,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
    this.loadDashboard();
    this.loadCVs();
    this.loadAnalytics();
  }

  loadDashboard() {
    this.cvService.getDashboard().subscribe({
      next: data => this.dashboard = data,
      error: err => this.error = err.message || 'Failed to load dashboard'
    });
  }

  loadCVs() {
    this.cvService.getCVs().subscribe({
      next: data => this.cvs = data,
      error: err => this.error = err.message || 'Failed to load CVs',
      complete: () => this.loading = false
    });
  }

  loadAnalytics() {
    this.cvService.getTopSkills().subscribe({
      next: data => this.topSkills = data,
      error: err => this.error = err.message || 'Failed to load top skills'
    });

    this.cvService.getTopLocations().subscribe({
      next: data => this.topLocations = data,
      error: err => this.error = err.message || 'Failed to load top locations'
    });

    this.cvService.getEducationDistribution().subscribe({
      next: data => this.educationDistribution = data,
      error: err => this.error = err.message || 'Failed to load education distribution'
    });

    this.cvService.getExperienceStats().subscribe({
      next: data => this.experienceStats = data,
      error: err => this.error = err.message || 'Failed to load experience stats'
    });
  }

  viewCV(id?: string) {
    if (!id) return alert('CV ID missing');
    this.router.navigate(['/cvs', id]);
  }

  editCV(id?: string) {
    if (!id) return alert('CV ID missing');
    this.router.navigate(['/cvs', id, 'edit']);
  }

  deleteCV(id?: string) {
    if (!id) return alert('CV ID missing');
    if (!confirm('Are you sure you want to delete this CV?')) return;

    this.cvService.deleteCV(id).subscribe({
      next: () => this.cvs = this.cvs.filter(cv => cv.id !== id),
      error: err => alert(err.message || 'Failed to delete CV')
    });
  }
}
