import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';   // 👈 import map
import { CV, JobDescription } from '../models/cv-model';

@Injectable({
  providedIn: 'root'
})
export class CvService {
  private apiUrl = 'http://localhost:8000/api/v1/cv';

  constructor(private http: HttpClient) {}

  getCVs(params?: any): Observable<CV[]> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== null && params[key] !== undefined) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get<any[]>(this.apiUrl, { params: httpParams }).pipe(
      map(cvs => cvs.map(cv => ({ ...cv, id: cv._id || cv.id })))
    );
  }

  getCV(id: string): Observable<CV> {
    return this.http.get<any>(`${this.apiUrl}/${id}`).pipe(
      map(cv => ({ ...cv, id: cv._id || cv.id }))
    );
  }

  // ✅ Alias for clarity (used in detail page)
  getCVById(id: string): Observable<CV> {
    return this.getCV(id);
  }

  createCV(cv: Partial<CV>): Observable<CV> {
    return this.http.post<any>(this.apiUrl, cv).pipe(
      map(newCv => ({ ...newCv, id: newCv._id || newCv.id }))
    );
  }

  updateCV(id: string, cv: Partial<CV>): Observable<CV> {
    return this.http.put<any>(`${this.apiUrl}/${id}`, cv).pipe(
      map(updated => ({ ...updated, id: updated._id || updated.id }))
    );
  }

  deleteCV(id: string): Observable<{ message: string; id: string }> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`).pipe(
      map(res => ({ ...res, id: res._id || res.id || id }))
    );
  }

  getTopSkills(limit = 10): Observable<{ skill: string; count: number }[]> {
    return this.http.get<{ skill: string; count: number }[]>(`${this.apiUrl}/analytics/skills`, {
      params: { limit }
    });
  }

  getTopLocations(limit = 10): Observable<{ location: string; count: number }[]> {
    return this.http.get<{ location: string; count: number }[]>(`${this.apiUrl}/analytics/locations`, {
      params: { limit }
    });
  }

  getEducationDistribution(): Observable<{ degree: string; count: number }[]> {
    return this.http.get<{ degree: string; count: number }[]>(`${this.apiUrl}/analytics/education`);
  }

  getExperienceStats(): Observable<{ min_years: number; max_years: number; avg_years: number }> {
    return this.http.get<{ min_years: number; max_years: number; avg_years: number }>(
      `${this.apiUrl}/analytics/experience`
    );
  }

  matchCandidates(job: JobDescription): Observable<CV[]> {
    return this.http.post<any[]>(`${this.apiUrl}/match`, job).pipe(
      map(cvs => cvs.map(cv => ({ ...cv, id: cv._id || cv.id })))
    );
  }

  getDashboard(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/dashboard`);
  }
}
