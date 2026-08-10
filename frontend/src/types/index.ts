export type UserRole = 'admin' | 'creator' | 'editor' | 'viewer';
export type ContentType = 'movie' | 'cartoon' | 'explainer' | 'news' | 'image_to_video' | 'advertisement';
export type ProjectStatus = 'draft' | 'planning' | 'scriptwriting' | 'character_creation' | 'storyboarding' | 'voice_generation' | 'scene_generation' | 'lip_sync' | 'editing' | 'upscaling' | 'rendering' | 'uploading' | 'published' | 'failed';

export interface User {
  id: string;
  email: string;
  displayName: string;
  role: UserRole;
  mfaEnabled: boolean;
  emailVerified: boolean;
  avatarUrl?: string;
  createdAt: string;
}

export interface Project {
  id: string;
  userId: string;
  title: string;
  contentType: ContentType;
  genre: string;
  targetAudience: string;
  language: string;
  durationSeconds: number;
  resolution: string;
  orientation: string;
  visualStyle: string;
  status: ProjectStatus;
  progressPercent: number;
  estimatedCost: number;
  actualCost: number;
  thumbnailUrl?: string;
  createdAt: string;
  updatedAt: string;
}

export interface Script {}
export interface Scene {}
export interface Character {}
export interface CharacterReference {}
export interface Voice {}
export interface RenderJob {}
export interface GpuInstance {}
export interface ModelRegistryEntry {}
export interface ApiIntegration {}
export interface SocialAccount {}
export interface CostEstimate {}
export interface Notification {
  id: string;
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  read: boolean;
  createdAt: string;
}

export interface Toast {
  id: string;
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
}
export interface ApiError {
  message: string;
  code: string;
}
export interface SuccessResponse {
  success: boolean;
  message?: string;
}

export interface MovieInput {}
export interface CartoonInput {}
export interface ExplainerInput {}
export interface NewsInput {}
export interface ImageToVideoInput {}
export interface AdvertisementInput {}
