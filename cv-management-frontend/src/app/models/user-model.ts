export interface User {
  id?: string;
  full_name: string;
  email: string;
  role?: string;        // optional: default 'candidate'
  password?: string;    // only sent to backend
  created_at?: string;
  token?: string;       // JWT token returned by backend
}

// --- Interfaces for Auth requests ---

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  full_name: string;
  email: string;
  password: string;
}
