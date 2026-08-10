import { create } from 'zustand';
import { Project } from '../types';

interface ProjectState {
  projects: Project[];
  currentProject: Project | null;
  isLoading: boolean;
  fetchProjects: (filters?: any) => Promise<void>;
  createProject: (data: Partial<Project>) => Promise<void>;
  updateProject: (id: string, data: Partial<Project>) => Promise<void>;
  deleteProject: (id: string) => Promise<void>;
  setCurrentProject: (project: Project | null) => void;
}

export const useProjectStore = create<ProjectState>((set) => ({
  projects: [],
  currentProject: null,
  isLoading: false,
  fetchProjects: async () => {
    set({ isLoading: true });
    setTimeout(() => set({ projects: [], isLoading: false }), 500);
  },
  createProject: async (data) => {},
  updateProject: async (id, data) => {},
  deleteProject: async (id) => {},
  setCurrentProject: (project) => set({ currentProject: project })
}));
