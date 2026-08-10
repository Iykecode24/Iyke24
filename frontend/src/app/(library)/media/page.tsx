'use client';
import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Search, Filter, Play, Music, Image as ImageIcon, Video, Download, Share2, MoreVertical, Film } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

const MOCK_MEDIA = [
  {
    id: 'media-1',
    title: 'Final Render - The Last Horizon',
    type: 'final_video',
    projectTitle: 'The Last Horizon',
    duration: '2:15',
    resolution: '4K',
    size: '1.2 GB',
    thumbnailUrl: '',
    createdAt: '2 hours ago'
  },
  {
    id: 'media-2',
    title: 'Scene 4 - Dialogue (Elena)',
    type: 'audio',
    projectTitle: 'The Last Horizon',
    duration: '0:12',
    resolution: null,
    size: '1.4 MB',
    thumbnailUrl: '',
    createdAt: '1 day ago'
  },
  {
    id: 'media-3',
    title: 'Cyberpunk City Skyline',
    type: 'image',
    projectTitle: 'Neon Nights',
    duration: null,
    resolution: '1920x1080',
    size: '4.5 MB',
    thumbnailUrl: '',
    createdAt: '2 days ago'
  },
  {
    id: 'media-4',
    title: 'Explainer Background Music',
    type: 'audio',
    projectTitle: 'Startup Explainer',
    duration: '1:30',
    resolution: null,
    size: '8.2 MB',
    thumbnailUrl: '',
    createdAt: '3 days ago'
  },
  {
    id: 'media-5',
    title: 'Scene 1 Raw Output',
    type: 'video_clip',
    projectTitle: 'The Last Horizon',
    duration: '0:05',
    resolution: '1080p',
    size: '45 MB',
    thumbnailUrl: '',
    createdAt: '4 days ago'
  }
];

export default function MediaLibraryPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState('all');

  const getMediaIcon = (type: string) => {
    switch(type) {
      case 'final_video': return <Film className="text-accent-secondary" />;
      case 'video_clip': return <Video className="text-accent-blue" />;
      case 'audio': return <Music className="text-accent-gold" />;
      case 'image': return <ImageIcon className="text-accent-purple" />;
      default: return <Film />;
    }
  };

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold mb-1">Media Library</h1>
          <p className="text-text-secondary">All your generated videos, audio, images, and final renders.</p>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" size={18} />
          <input 
            type="text"
            placeholder="Search media by title or project..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-bg-secondary border border-white/10 rounded-xl py-2.5 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-transparent transition-all"
          />
        </div>
        <Button variant="secondary" className="gap-2">
          <Filter size={18} /> Filter
        </Button>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-white/10 overflow-x-auto hide-scrollbar">
        {[
          { id: 'all', label: 'All Media' },
          { id: 'videos', label: 'Final Videos' },
          { id: 'clips', label: 'Raw Clips' },
          { id: 'audio', label: 'Audio & Music' },
          { id: 'images', label: 'Images' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${
              activeTab === tab.id 
                ? 'border-accent-primary text-white' 
                : 'border-transparent text-text-muted hover:text-white'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {MOCK_MEDIA.map(media => (
          <Card key={media.id} className="group overflow-hidden flex flex-col hover:-translate-y-1 transition-all duration-300 p-0 border-white/10">
            {/* Media Preview Area */}
            <div className="h-40 bg-bg-primary relative flex items-center justify-center border-b border-white/5">
              {/* Fallback Icon */}
              <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center">
                {getMediaIcon(media.type)}
              </div>
              
              {/* Play overlay for video/audio */}
              {['final_video', 'video_clip', 'audio'].includes(media.type) && (
                <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity backdrop-blur-sm">
                  <button className="w-12 h-12 rounded-full bg-accent-primary flex items-center justify-center text-white shadow-lg shadow-accent-primary/20 hover:scale-110 transition-transform">
                    <Play size={20} className="ml-1" />
                  </button>
                </div>
              )}
              
              {/* Duration Badge */}
              {media.duration && (
                <div className="absolute bottom-2 right-2 px-2 py-0.5 rounded bg-black/70 text-[10px] font-mono text-white backdrop-blur">
                  {media.duration}
                </div>
              )}
              
              {/* Resolution Badge */}
              {media.resolution && (
                <div className="absolute top-2 right-2 px-2 py-0.5 rounded bg-black/70 text-[10px] font-bold text-white backdrop-blur border border-white/10">
                  {media.resolution}
                </div>
              )}
            </div>
            
            <div className="p-4 flex-1 flex flex-col">
              <h3 className="font-bold text-sm text-white line-clamp-1 mb-1 group-hover:text-accent-primary transition-colors" title={media.title}>
                {media.title}
              </h3>
              <div className="text-xs text-text-muted mb-4">
                Project: {media.projectTitle}
              </div>
              
              <div className="flex justify-between items-center mt-auto text-xs text-text-secondary">
                <span>{media.size}</span>
                <span>{media.createdAt}</span>
              </div>
              
              {/* Action Bar (revealed on hover) */}
              <div className="flex gap-2 mt-4 pt-3 border-t border-white/5 opacity-0 group-hover:opacity-100 transition-opacity">
                <Button variant="secondary" className="flex-1 py-1 h-auto text-xs gap-1">
                  <Download size={14} /> Download
                </Button>
                {media.type === 'final_video' && (
                  <Button variant="secondary" className="flex-1 py-1 h-auto text-xs gap-1 text-accent-secondary">
                    <Share2 size={14} /> Publish
                  </Button>
                )}
                <Button variant="secondary" className="px-2 py-1 h-auto shrink-0">
                  <MoreVertical size={14} />
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
