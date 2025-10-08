import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, FormControl, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { CvService } from '../services/cv';

@Component({
  selector: 'app-cv-form',
  templateUrl: './cv-form.html',
  styleUrls: ['./cv-form.css'],
  standalone: false
})
export class CvFormComponent implements OnInit {
  cvForm!: FormGroup;
  loading = false;
  error = '';
  isEdit = false;

  locations = ['New York, USA', 'London, UK', 'Paris, France', 'Berlin, Germany'];
  educationLevels = ['High School', 'Bachelor', 'Master', 'PhD'];

  constructor(
    private fb: FormBuilder,
    private cvService: CvService,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.cvForm = this.fb.group({
      full_name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      phone: ['', Validators.required],
      location: ['', Validators.required],
      skills: this.fb.array([this.fb.control('', Validators.required)]),
      education: this.fb.array([this.createEducationGroup()]),
      experience: this.fb.array([this.createExperienceGroup()]),
      languages: this.fb.array([this.fb.control('', Validators.required)]),
      cv_file: [null]
    });

    const cvId = this.route.snapshot.paramMap.get('id');
    if (cvId) {
      this.isEdit = true;
      this.loadCV(cvId);
    }
  }

  // ----------------- Getters -----------------
  get skillsArray(): FormArray { return this.cvForm.get('skills') as FormArray; }
  get educationArray(): FormArray { return this.cvForm.get('education') as FormArray; }
  get experienceArray(): FormArray { return this.cvForm.get('experience') as FormArray; }
  get languagesArray(): FormArray { return this.cvForm.get('languages') as FormArray; }

  // ----------------- Groups -----------------
  createEducationGroup(): FormGroup {
    return this.fb.group({
      degree: ['', Validators.required],
      school: ['', Validators.required],
      level: ['', Validators.required],
      year: ['', Validators.required]
    });
  }

  createExperienceGroup(): FormGroup {
    return this.fb.group({
      title: ['', Validators.required],
      company: ['', Validators.required],
      years: ['', Validators.required],
      technologies: this.fb.array([this.fb.control('')])
    });
  }

  // ----------------- Mutations -----------------
  addSkill() { this.skillsArray.push(this.fb.control('', Validators.required)); }
  removeSkill(i: number) { this.skillsArray.removeAt(i); }

  addEducation() { this.educationArray.push(this.createEducationGroup()); }
  removeEducation(i: number) { this.educationArray.removeAt(i); }

  addExperience() { this.experienceArray.push(this.createExperienceGroup()); }
  removeExperience(i: number) { this.experienceArray.removeAt(i); }

  addLanguage() { this.languagesArray.push(this.fb.control('', Validators.required)); }
  removeLanguage(i: number) { this.languagesArray.removeAt(i); }

  addTechnology(expIndex: number) {
    const techArray = this.getTechnologiesArray(expIndex);
    techArray.push(this.fb.control(''));
  }

  removeTechnology(expIndex: number, techIndex: number) {
    const techArray = this.getTechnologiesArray(expIndex);
    techArray.removeAt(techIndex);
  }

  getTechnologiesArray(expIndex: number): FormArray {
    return this.experienceArray.at(expIndex).get('technologies') as FormArray;
  }

  // ----------------- File -----------------
  onFileChange(event: any) {
    if (event.target.files.length) {
      this.cvForm.patchValue({ cv_file: event.target.files[0] });
    }
  }

  // ----------------- API -----------------
  loadCV(id: string) {
    this.cvService.getCV(id).subscribe({
      next: cv => this.cvForm.patchValue(cv),
      error: err => console.error(err)
    });
  }

  onSubmit() {
    if (this.cvForm.invalid) {
      this.error = 'Please fill all required fields';
      return;
    }

    this.loading = true;

    const action = this.isEdit
      ? this.cvService.updateCV(this.route.snapshot.paramMap.get('id')!, this.cvForm.value)
      : this.cvService.createCV(this.cvForm.value);

    action.subscribe({
      next: () => {
        this.loading = false;
        this.router.navigate(['/cvs']);
      },
      error: err => {
        this.loading = false;
        this.error = err.message || 'Failed to save CV';
      }
    });
  }

  // ----------------- Extra -----------------
  resetForm() {
    this.cvForm.reset();
    this.skillsArray.clear();
    this.educationArray.clear();
    this.experienceArray.clear();
    this.languagesArray.clear();
    this.addSkill();
    this.addEducation();
    this.addExperience();
    this.addLanguage();
  }

  exportJSON() {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(this.cvForm.value, null, 2));
    const a = document.createElement('a');
    a.href = dataStr;
    a.download = "cv.json";
    a.click();
  }

  exportPDF() {
    alert('PDF export feature coming soon 🚀');
  }
}
