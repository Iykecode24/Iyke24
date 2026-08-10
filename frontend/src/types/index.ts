export enum UserRole {
  admin = 'admin',
  creator = 'creator',
  editor = 'editor',
  viewer = 'viewer'
}

export enum ContentType {
  movie = 'movie',
  cartoon = 'cartoon',
  explainer = 'explainer',
  news = 'news',
  image_to_video = 'image_to_video',
  advertisement = 'advertisement'
}

export enum ProjectStatus {
  draft = 'draft',
  planning = 'planning',
  scriptwriting = 'scriptwriting',
  character_creation = 'character_creation',
  storyboarding = 'storyboarding',
  voice_generation = 'voice_generation',
  scene_generation = 'scene_generation',
  lip_sync = 'lip_sync',
  editing = 'editing',
  upscaling = 'upscaling',
  rendering = 'rendering',
  uploading = 'uploading',
  published = 'published',
  failed = 'failed'
}

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

export interface Script {
  id: string;
  projectId: string;
  title: string;
  logline?: string;
  synopsis?: string;
  fullText?: string;
  genre?: string;
  status: string;
  createdAt: string;
  updatedAt: string;
}
export interface Scene {
  id: string;
  projectId: string;
  scriptId: string;
  orderIndex: number;
  title?: string;
  description?: string;
  visualPrompt?: string;
  dialogue?: string;
  narration?: string;
  status: ProjectStatus;
  durationSeconds?: number;
  createdAt: string;
  updatedAt: string;
}
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
