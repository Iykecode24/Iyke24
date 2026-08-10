import { Project, ContentType, ProjectStatus, User, UserRole, Script, Scene } from '@/types';

const toCamel = (str: string) => str.replace(/([-_][a-z])/ig, ($1) => $1.toUpperCase().replace('-', '').replace('_', ''));
const isObject = (o: any) => o === Object(o) && !Array.isArray(o) && typeof o !== 'function' && o !== null;

const keysToCamel = (o: any): any => {
  if (isObject(o)) {
    const n: Record<string, any> = {};
    Object.keys(o).forEach((k) => {
      n[toCamel(k)] = keysToCamel(o[k]);
    });
    return n;
  } else if (Array.isArray(o)) {
    return o.map((i) => keysToCamel(i));
  }
  return o;
};

const toSnake = (str: string) => str.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);
const keysToSnake = (o: any): any => {
  if (isObject(o)) {
    const n: Record<string, any> = {};
    Object.keys(o).forEach((k) => {
      n[toSnake(k)] = keysToSnake(o[k]);
    });
    return n;
  } else if (Array.isArray(o)) {
    return o.map((i) => keysToSnake(i));
  }
  return o;
};

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

export class ApiClient {
  private baseUrl: string;

  constructor() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    if (!apiUrl && process.env.NODE_ENV === 'production') {
      throw new Error('NEXT_PUBLIC_API_URL environment variable is required in production.');
    }
    this.baseUrl = apiUrl || 'http://localhost:8000/api/v1';
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    // In a real app, you'd get the token from cookies or localStorage
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    if (options.body && typeof options.body === 'string') {
      try {
        const parsed = JSON.parse(options.body);
        options.body = JSON.stringify(keysToSnake(parsed));
      } catch (e) {
        // Not a JSON string
      }
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      let errorMessage = 'An error occurred';
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch (e) {
        // Fallback to status text
        errorMessage = response.statusText;
      }
      throw new ApiError(response.status, errorMessage);
    }

    // For 204 No Content
    if (response.status === 204) {
      return {} as T;
    }

    const data = await response.json();
    return keysToCamel(data) as T;
  }

  // --- Auth ---
  async login(email: string, password: string): Promise<{ access_token: string, user: User }> {
    // Mock login for now since backend might not be fully wired up yet
    return {
      access_token: 'mock-token',
      user: {
        id: 'user-123',
        email,
        displayName: 'Iyke Enukaora',
        role: UserRole.admin,
        mfaEnabled: false,
        emailVerified: true,
        createdAt: new Date().toISOString()
      }
    };
  }

  async getProfile(): Promise<User> {
    return this.request<User>('/auth/me');
  }

  // --- Projects ---
  async getProjects(): Promise<{ items: Project[], total: number }> {
    try {
      return await this.request<{ items: Project[], total: number }>('/projects');
    } catch (error) {
      // Return mock data if backend fails
      return { items: [], total: 0 };
    }
  }

  async getProject(id: string): Promise<Project> {
    return this.request<Project>(`/projects/${id}`);
  }

  async createProject(data: Partial<Project>): Promise<Project> {
    try {
      return await this.request<Project>('/projects', {
        method: 'POST',
        body: JSON.stringify(data),
      });
    } catch (error) {
      console.warn("Backend not ready, returning mock project");
      // Mock return
      return {
        id: `proj-${Date.now()}`,
        ...data,
        status: ProjectStatus.scriptwriting,
        progressPercent: 0,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      } as Project;
    }
  }

  // --- Scripts ---
  async getScript(projectId: string): Promise<Script> {
    return this.request<Script>(`/projects/${projectId}/script`);
  }

  async generateScript(projectId: string): Promise<Script> {
    return this.request<Script>(`/projects/${projectId}/script/generate`, {
      method: 'POST'
    });
  }

  async updateScript(scriptId: string, data: Partial<Script>): Promise<Script> {
    return this.request<Script>(`/scripts/${scriptId}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  // --- Scenes ---
  async getScenes(projectId: string): Promise<Scene[]> {
    return this.request<Scene[]>(`/projects/${projectId}/scenes`);
  }
}

export const api = new ApiClient();
