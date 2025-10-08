// ---------------- CV / Candidate Interfaces -----------------
export interface Education {
  degree: string;
  school: string;
  year?: number;
}

export interface Experience {
  title: string;
  company: string;
  years?: number;
  technologies?: string[]; // Optional: tech used in this experience
}

export interface Language {
  name: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced' | 'Native';
}

export interface Project {
  name: string;
  link?: string; // e.g., GitHub, portfolio, demo link
}

export interface Certification {
  name: string;
  icon?: string; // Optional icon class for display
}

export interface CV {
  id?: string;
  full_name: string;
  email: string;
  phone?: string;
  location?: string;
  education?: Education[];
  experience?: Experience[];
  skills?: string[];
  languages?: Language[];
  projects?: Project[];
  certifications?: Certification[];
  created_at?: string;
  updated_at?: string;
}

export interface JobDescription {
  skills: string[];
  min_experience?: number;
  top_n?: number;
}

// ---------------- Dashboard / Analytics Interfaces -----------------
export interface SkillCount {
  skill: string;
  count: number;
}

export interface LocationCount {
  location: string;
  count: number;
}

export interface EducationCount {
  degree: string;
  count: number;
}

export interface ExperienceStats {
  min_years: number;
  max_years: number;
  avg_years: number;
}

export interface DashboardData {
  total_cvs: number;
  recent: CV[];
  top_skills: SkillCount[];
  top_locations: LocationCount[];
  education_distribution: EducationCount[];
  skills_distribution: SkillCount[];
  experience_levels: ExperienceStats;
}
