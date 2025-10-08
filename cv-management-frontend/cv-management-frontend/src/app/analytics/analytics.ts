import { Component, OnInit } from '@angular/core';
import { CvService } from '../services/cv';
import { DashboardData, SkillCount, LocationCount, EducationCount, ExperienceStats } from '../models/cv-model';

@Component({
  selector: 'app-analytics',
  templateUrl: './analytics.html',
  styleUrls: ['./analytics.css'],
  standalone:false
})
export class AnalyticsComponent implements OnInit {

  loading = true;
  error = '';

  totalCVs = 0;
  recentCVs: any[] = [];

  topSkills: SkillCount[] = [];
  topLocations: LocationCount[] = [];
  educationDistribution: EducationCount[] = [];
  experienceStats: ExperienceStats = { min_years: 0, max_years: 0, avg_years: 0 };

  constructor(private cvService: CvService) {}

  ngOnInit(): void {
    this.fetchDashboard();
  }

  fetchDashboard() {
    this.loading = true;
    this.cvService.getDashboard().subscribe({
      next: (data: DashboardData) => {
        this.totalCVs = data.total_cvs;
        this.recentCVs = data.recent;
        this.topSkills = data.top_skills;
        this.topLocations = data.top_locations;
        this.educationDistribution = data.education_distribution;
        this.experienceStats = data.experience_levels;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load analytics';
        console.error(err);
        this.loading = false;
      }
    });
  }

  // Calculate width % for horizontal bars
  getBarWidth(count: number, max: number): string {
    return max ? `${(count / max) * 100}%` : '0%';
  }

  // Get max value in an array of {count: number}
  getMaxCount(items: { count: number }[]): number {
    return items.length ? Math.max(...items.map(i => i.count)) : 0;
  }
}
