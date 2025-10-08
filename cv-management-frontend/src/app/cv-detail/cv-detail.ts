import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CvService } from '../services/cv';
import { CV } from '../models/cv-model';
import { AuthService } from '../services/auth';

@Component({
  selector: 'app-cv-detail',
  templateUrl: './cv-detail.html',
  styleUrls: ['./cv-detail.css'],
  standalone: false
})
export class CvDetailComponent implements OnInit {
  cv?: CV;
  loading = true;
  error = '';

  // Collapsible state
  showSkills = true;
  showEducation = true;
  showExperience = true;
  showLanguages = true;
  showProjects = true;
  showCertifications = true;

  constructor(
    private route: ActivatedRoute,
    private cvService: CvService,
    private router: Router,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (!id) {
      this.error = 'CV ID missing';
      this.loading = false;
      return;
    }

    this.cvService.getCVById(id).subscribe({
      next: (data: CV) => {
        this.cv = {
          ...data,
          skills: data.skills || [],
          education: data.education || [],
          experience: data.experience || [],
          languages: data.languages || [],
          projects: data.projects || [],
          certifications: data.certifications || []
        };
        this.loading = false;
      },
      error: err => {
        this.error = 'Failed to load CV details';
        console.error(err);
        this.loading = false;
      }
    });
  }

  editCV(): void {
    if (!this.cv?.id) return alert('CV ID missing');
    this.router.navigate(['/cvs', this.cv.id, 'edit']);
  }

  deleteCV(): void {
    if (!this.cv?.id) return alert('CV ID missing');
    if (!confirm('Are you sure you want to delete this CV?')) return;

    this.cvService.deleteCV(this.cv.id).subscribe({
      next: () => this.router.navigate(['/cvs']),
      error: err => alert(err.message || 'Failed to delete CV')
    });
  }

  sendEmail(): void {
    if (!this.cv?.email) return;
    window.location.href = `mailto:${this.cv.email}`;
  }

  downloadPDF(): void {
    alert('PDF download feature to be implemented!');
  }

  addNote(): void {
    const note = prompt('Add a note for this CV:');
    if (note) alert('Note saved: ' + note);
  }

  exportCV(): void {
    if (!this.cv) return;

    const headers = ['Full Name', 'Email', 'Location', 'Phone', 'Skills', 'Education', 'Experience', 'Languages'];
    const rows = [[
      this.cv.full_name || '',
      this.cv.email || '',
      this.cv.location || '',
      this.cv.phone || '',
      (this.cv.skills || []).join(', '),
      (this.cv.education || []).map(e => `${e.degree} at ${e.school} (${e.year || 'N/A'})`).join('; '),
      (this.cv.experience || []).map(ex => `${ex.title} at ${ex.company} (${ex.years || 'N/A'} years)`).join('; '),
      (this.cv.languages || []).map(l => `${l.name || l} (${l.level || 'N/A'})`).join(', ')
    ]];

    let csvContent = headers.join(',') + '\n';
    rows.forEach(r => csvContent += r.join(',') + '\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.setAttribute('download', `${this.cv.full_name || 'cv'}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}
