'use client';
import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  Share2, Youtube, Instagram, Twitter, Linkedin, Facebook, 
  Plus, RefreshCw, Unlink, Settings, AlertTriangle, CheckCircle2,
  Users, Eye, MousePointerClick, Link as LinkIcon
} from 'lucide-react';

const ACCOUNTS = [
  { 
    id: 'yt-1', 
    platform: 'youtube', 
    accountName: 'iyke.studio@gmail.com',
    channels: [
      { id: 'c-1', name: 'Iyke Studio Official', type: 'Brand Channel', subs: '12.5K', isDefault: true, status: 'active' },
      { id: 'c-2', name: 'Iyke Personal', type: 'Personal Channel', subs: '450', isDefault: false, status: 'active' }
    ]
  },
  { 
    id: 'li-1', 
    platform: 'linkedin', 
    accountName: 'iyke-admin',
    channels: [
      { id: 'c-3', name: 'Iyke Content Studio', type: 'Company Page', subs: '3.2K', isDefault: true, status: 'active' },
      { id: 'c-4', name: 'Iyke Founder', type: 'Personal Profile', subs: '8.1K', isDefault: false, status: 'active' }
    ]
  },
  { 
    id: 'tt-1', 
    platform: 'tiktok', 
    accountName: 'iyke.studio.tt',
    channels: [
      { id: 'c-5', name: '@iykestudio', type: 'Creator Account', subs: '45.2K', isDefault: true, status: 'token_expired' }
    ]
  }
];

export default function ChannelManagerPage() {
  const [showFallbackModal, setShowFallbackModal] = useState(false);
  const [fallbackUrl, setFallbackUrl] = useState('');
  const [fallbackPlatform, setFallbackPlatform] = useState('youtube');

  const getPlatformIcon = (platform: string, size = 20) => {
    switch(platform) {
      case 'youtube': return <Youtube size={size} className="text-red-500" />;
      case 'instagram': return <Instagram size={size} className="text-pink-500" />;
      case 'twitter': return <Twitter size={size} className="text-blue-400" />;
      case 'linkedin': return <Linkedin size={size} className="text-blue-700" />;
      case 'facebook': return <Facebook size={size} className="text-blue-600" />;
      case 'tiktok': return <div className="w-5 h-5 bg-white text-black flex items-center justify-center font-bold text-[10px] rounded">TT</div>;
      default: return <Share2 size={size} />;
    }
  };

  return (
    <div className="space-y-8 animate-fade-in pb-12">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold mb-1">Channel Manager</h1>
          <p className="text-text-secondary">Discover and manage publishing destinations across your connected social accounts.</p>
        </div>
        <div className="flex gap-3">
          <Button variant="secondary" className="gap-2" onClick={() => setShowFallbackModal(true)}>
            <LinkIcon size={16} /> Manual URL Fallback
          </Button>
          <Button className="gap-2 bg-gradient-to-r from-accent-primary to-accent-secondary text-white border-0">
            <Plus size={18} /> Connect New Account
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-8">
        {ACCOUNTS.map(account => (
          <Card key={account.id} className="border-white/10 overflow-hidden bg-bg-card/50">
            {/* Account Header */}
            <div className="p-4 bg-bg-secondary/50 border-b border-white/5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded bg-bg-primary flex items-center justify-center border border-white/10">
                  {getPlatformIcon(account.platform, 24)}
                </div>
                <div>
                  <h2 className="font-bold text-white text-lg capitalize">{account.platform} Connection</h2>
                  <p className="text-xs text-text-muted flex items-center gap-2">
                    Authenticated as: <span className="text-text-secondary font-mono">{account.accountName}</span>
                  </p>
                </div>
              </div>
              <div className="flex gap-2">
                <Button variant="secondary" size="sm" className="h-8 gap-1 text-xs">
                  <RefreshCw size={12} /> Sync Channels
                </Button>
                <Button variant="danger" size="sm" className="h-8 gap-1 text-xs">
                  <Unlink size={12} /> Disconnect
                </Button>
              </div>
            </div>

            {/* Discovered Channels/Pages */}
            <div className="p-0">
              <div className="px-4 py-3 bg-white/5 text-xs font-bold text-text-muted uppercase tracking-wider grid grid-cols-12 gap-4 items-center border-b border-white/5">
                <div className="col-span-5">Destination / Page</div>
                <div className="col-span-2 text-center">Audience</div>
                <div className="col-span-2 text-center">Status</div>
                <div className="col-span-3 text-right">Actions</div>
              </div>

              {account.channels.map(channel => (
                <div key={channel.id} className="px-4 py-4 grid grid-cols-12 gap-4 items-center border-b border-white/5 hover:bg-white/5 transition-colors group">
                  <div className="col-span-5 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-bg-secondary to-bg-primary border border-white/10 flex items-center justify-center shrink-0 shadow-inner">
                      <span className="font-bold text-white text-sm">{channel.name.charAt(0)}</span>
                    </div>
                    <div>
                      <div className="font-bold text-white text-sm flex items-center gap-2">
                        {channel.name}
                        {channel.isDefault && <Badge variant="default" className="text-[10px] h-4 py-0 px-1.5 bg-accent-primary text-white border-0">Default</Badge>}
                      </div>
                      <div className="text-xs text-text-muted mt-0.5">{channel.type}</div>
                    </div>
                  </div>
                  
                  <div className="col-span-2 flex flex-col items-center justify-center">
                    <span className="text-white text-sm font-medium">{channel.subs}</span>
                    <span className="text-[10px] text-text-muted flex items-center gap-1"><Users size={10} /> Followers</span>
                  </div>

                  <div className="col-span-2 flex justify-center">
                    {channel.status === 'active' ? (
                      <div className="px-2 py-1 rounded-full bg-accent-green/10 text-accent-green text-[11px] font-medium flex items-center gap-1 border border-accent-green/20">
                        <CheckCircle2 size={12} /> Active
                      </div>
                    ) : (
                      <div className="px-2 py-1 rounded-full bg-accent-red/10 text-accent-red text-[11px] font-medium flex items-center gap-1 border border-accent-red/20">
                        <AlertTriangle size={12} /> Token Expired
                      </div>
                    )}
                  </div>

                  <div className="col-span-3 flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    {!channel.isDefault && (
                      <Button variant="secondary" size="sm" className="h-7 text-xs">Set Default</Button>
                    )}
                    <Button variant="secondary" size="sm" className="h-7 w-7 p-0"><Settings size={14} /></Button>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        ))}
      </div>

      {/* Manual Fallback Modal (Simulated) */}
      {showFallbackModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-md p-6 bg-bg-card border-white/10 shadow-2xl">
            <h2 className="text-xl font-bold text-white mb-2">Manual Channel Fallback</h2>
            <p className="text-sm text-text-secondary mb-6">If a platform's API doesn't expose your channel, you can map it manually via its public URL. We will verify ownership during the next publishing cycle.</p>
            
            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Platform</label>
                <select 
                  className="w-full bg-bg-primary border border-white/10 rounded-lg p-3 text-white focus:outline-none focus:ring-2 focus:ring-accent-primary"
                  value={fallbackPlatform}
                  onChange={(e) => setFallbackPlatform(e.target.value)}
                >
                  <option value="youtube">YouTube</option>
                  <option value="facebook">Facebook Page</option>
                  <option value="instagram">Instagram</option>
                  <option value="tiktok">TikTok</option>
                  <option value="linkedin">LinkedIn Company</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Public URL</label>
                <Input 
                  placeholder="https://www.youtube.com/@channel" 
                  value={fallbackUrl}
                  onChange={(e) => setFallbackUrl(e.target.value)}
                />
              </div>
            </div>
            
            <div className="flex justify-end gap-3">
              <Button variant="ghost" onClick={() => setShowFallbackModal(false)}>Cancel</Button>
              <Button className="bg-accent-primary text-white hover:bg-accent-primary/90" onClick={() => setShowFallbackModal(false)}>
                Verify & Add Destination
              </Button>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
