import { useAuthStore } from '@/stores/auth-store';
import { useEffect } from 'react';

export const useAuth = () => {
  const { user, isAuthenticated, isLoading, login, logout, signup, refreshToken } = useAuthStore();

  useEffect(() => {
    // Attempt silent refresh on mount if not authenticated
    if (!isAuthenticated) {
      refreshToken().catch(() => {});
    }
  }, [isAuthenticated, refreshToken]);

  return { user, isAuthenticated, isLoading, login, logout, signup };
};
