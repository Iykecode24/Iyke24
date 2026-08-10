import { useProjectStore } from '@/stores/project-store';
import { useEffect } from 'react';

export const useProjects = (filters?: any) => {
  const { projects, isLoading, fetchProjects, createProject, updateProject, deleteProject } = useProjectStore();

  useEffect(() => {
    fetchProjects(filters);
  }, [filters, fetchProjects]);

  return { projects, isLoading, createProject, updateProject, deleteProject };
};
