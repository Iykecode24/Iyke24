'use client';
import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Share2, Youtube, Instagram, Twitter, Linkedin, CheckCircle2, Clock, Calendar, Plus } from 'lucide-react';
import { useRouter } from 'next/navigation';

const CONNECTED_ACCOUNTS = [
  { id: 'acc-1', platform: 'youtube', name: 'Iyke Studio Official', status: 'connected' },
  { id: 'acc-2', platform: 'instagram', name: '@iykestudio', status: 'connected' },
  { id: 'acc-3', platform: 'tiktok', name: '@iykestudio', status: 'disconnected' },
  { id: 'acc-4', platform: 'twitter', name: '@iyke_studio', status: 'connected' },
];

const RECENT_POSTS = [
  { id: 'post-1', video: 'The Last Horizon Trailer', platform: 'youtube', status: 'published', date: 'Today, 10:00 AM', views: '1.2K' },
  { id: 'post-2', video: 'Summer Sneaker Sale Ad', platform: 'instagram', status: 'scheduled', date: 'Tomorrow, 09:00 AM', views: '-' },
  { id: 'post-3', video: 'Tech News Update', platform: 'twitter', status: 'failed', date: 'Yesterday', views: '-', error: 'Token expired' },
];

export default function SocialPublishingPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState('overview');

  const getPlatformIcon = (platform: string, size = 20) => {
    switch(platform) {
      case 'youtube': return <Youtube size={size} className="text-red-500" />;
      case 'instagram': return <Instagram size={size} className="text-pink-500" />;
      case 'twitter': return <Twitter size={size} className="text-blue-400" />;
      case 'linkedin': return <Linkedin size={size} className="text-blue-700" />;
      case 'tiktok': return <div className="w-5 h-5 bg-white text-black flex items-center justify-center font-bold text-[10px] rounded">TT</div>;
      default: return <Share2 size={size} />;
    }
  };

  return (
    <div className="space-y-8 animate-fade-in pb-12">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold mb-1">Social Publishing</h1>
          <p className="text-text-secondary">Manage connected accounts and schedule your video posts.</p>
        </div>
        <Button className="gap-2 bg-gradient-to-r from-accent-primary to-accent-secondary text-white border-0">
          <Plus size={18} /> New Post
        </Button>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-white/10">
        {[
          { id: 'overview', label: 'Overview & Schedule' },
          { id: 'accounts', label: 'Connected Accounts' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.id 
                ? 'border-accent-primary text-white' 
                : 'border-transparent text-text-muted hover:text-white'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            <h2 className="text-xl font-bold text-white border-b border-white/10 pb-2">Recent & Scheduled Posts</h2>
            
            <div className="space-y-4">
              {RECENT_POSTS.map(post => (
                <Card key={post.id} className="p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-white/10 hover:border-white/20 transition-colors">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-lg bg-bg-secondary flex items-center justify-center shrink-0">
                      {getPlatformIcon(post.platform, 24)}
                    </div>
                    <div>
                      <h3 className="font-bold text-white text-base">{post.video}</h3>
                      <div className="flex items-center gap-3 text-xs text-text-secondary mt-1">
                        <span className="capitalize">{post.platform}</span>
                        <span>•</span>
                        <span className="flex items-center gap-1"><Calendar size={12} /> {post.date}</span>
                        {post.views !== '-' && (
                          <>
                            <span>•</span>
                            <span>{post.views} views</span>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-4 w-full md:w-auto justify-between md:justify-end">
                    <div>
                      {post.status === 'published' && <Badge status="published" />}
                      {post.status === 'scheduled' && (
                        <div className="px-2 py-1 rounded bg-accent-blue/20 text-accent-blue text-xs font-medium flex items-center gap-1 border border-accent-blue/30">
                          <Clock size={12} /> Scheduled
                        </div>
                      )}
                      {post.status === 'failed' && (
                        <div className="px-2 py-1 rounded bg-accent-red/20 text-accent-red text-xs font-medium flex items-center gap-1 border border-accent-red/30">
                          Failed: {post.error}
                        </div>
                      )}
                    </div>
                    <Button variant="ghost" className="text-xs px-2 h-8">Options</Button>
                  </div>
                </Card>
              ))}
            </div>
          </div>
          
          <div className="space-y-6">
            <Card className="p-6 bg-gradient-to-br from-bg-secondary to-bg-primary border-white/10">
              <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                <Share2 size={18} className="text-accent-primary" /> Quick Publish
              </h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-text-secondary mb-1">Select Video</label>
                  <select className="w-full bg-bg-primary border border-white/10 rounded-lg p-2 text-sm text-white focus:outline-none focus:ring-1 focus:ring-accent-primary">
                    <option>The Last Horizon Final (4K)</option>
                    <option>Startup Explainer v2</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-xs font-medium text-text-secondary mb-1">Caption</label>
                  <textarea 
                    className="w-full h-20 bg-bg-primary border border-white/10 rounded-lg p-2 text-sm text-white focus:outline-none focus:ring-1 focus:ring-accent-primary resize-none"
                    placeholder="Write a caption..."
                  />
                </div>
                
                <div>
                  <label className="block text-xs font-medium text-text-secondary mb-2">Platforms</label>
                  <div className="flex gap-2">
                    {CONNECTED_ACCOUNTS.filter(a => a.status === 'connected').map(acc => (
                      <button key={acc.id} className="w-10 h-10 rounded-full bg-bg-primary border border-white/10 flex items-center justify-center hover:border-accent-primary hover:bg-accent-primary/10 transition-colors" title={acc.name}>
                        {getPlatformIcon(acc.platform)}
                      </button>
                    ))}
                  </div>
                </div>
                
                <Button className="w-full bg-white text-black hover:bg-white/90">
                  Publish Now
                </Button>
              </div>
            </Card>
          </div>
        </div>
      )}

      {activeTab === 'accounts' && (
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-white border-b border-white/10 pb-2">Manage Connections</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {CONNECTED_ACCOUNTS.map(acc => (
              <Card key={acc.id} className="p-6 border-white/10 flex flex-col items-center text-center hover:border-white/20 transition-colors">
                <div className="w-16 h-16 rounded-full bg-bg-secondary flex items-center justify-center mb-4">
                  {getPlatformIcon(acc.platform, 32)}
                </div>
                <h3 className="font-bold text-white capitalize text-lg">{acc.platform}</h3>
                <p className="text-sm text-text-muted mb-6">{acc.status === 'connected' ? acc.name : 'Not Connected'}</p>
                
                {acc.status === 'connected' ? (
                  <Button variant="secondary" className="w-full text-text-secondary hover:text-white hover:bg-white/10 border-white/10 gap-2">
                    <CheckCircle2 size={16} className="text-accent-green" /> Connected
                  </Button>
                ) : (
                  <Button className="w-full bg-accent-primary hover:bg-accent-primary/90 text-white border-0 gap-2">
                    Connect Account
                  </Button>
                )}
              </Card>
            ))}
            
            <Card className="p-6 border-white/10 border-dashed flex flex-col items-center justify-center text-center cursor-pointer hover:border-accent-primary hover:bg-accent-primary/5 transition-colors group">
              <div className="w-16 h-16 rounded-full bg-bg-secondary group-hover:bg-accent-primary/20 flex items-center justify-center mb-4 transition-colors">
                <Plus size={32} className="text-text-muted group-hover:text-accent-primary" />
              </div>
              <h3 className="font-bold text-text-secondary group-hover:text-white transition-colors">Add Custom Integration</h3>
              <p className="text-xs text-text-muted mt-2">Webhook or API</p>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
}
