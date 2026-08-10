import { create } from 'zustand';
import { User } from '../types';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, displayName: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
  updateProfile: (data: Partial<User>) => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  login: async (email, password) => {
    set({ isLoading: true });
    // mock login
    setTimeout(() => {
      set({
        user: { id: '1', email, displayName: 'Test User', role: 'admin', mfaEnabled: false, emailVerified: true, createdAt: new Date().toISOString() },
        isAuthenticated: true,
        isLoading: false
      });
    }, 1000);
  },
  signup: async (email, password, displayName) => {
    set({ isLoading: true });
    setTimeout(() => set({ isLoading: false }), 1000);
  },
  logout: () => {
    set({ user: null, isAuthenticated: false });
  },
  refreshToken: async () => {},
  updateProfile: async (data) => {
    set((state) => ({ user: state.user ? { ...state.user, ...data } : null }));
  }
}));
