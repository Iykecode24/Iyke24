'use client';

import React, { useState } from 'react';

type Platform = 'youtube' | 'tiktok' | 'meta' | 'linkedin' | 'x';

interface PlatformData {
  id: Platform;
  name: string;
  icon: string;
  status: 'connected' | 'disconnected';
  accountName?: string;
  permissions: string[];
  color: string;
  borderColor: string;
}

const mockPlatforms: PlatformData[] = [
  {
    id: 'youtube',
    name: 'YouTube',
    icon: '▶️',
    status: 'connected',
    accountName: 'Iyke Productions',
    permissions: ['Manage your YouTube videos', 'View your YouTube account'],
    color: 'bg-red-500/10 text-red-400',
    borderColor: 'border-red-500/30'
  },
  {
    id: 'tiktok',
    name: 'TikTok',
    icon: '🎵',
    status: 'connected',
    accountName: '@iyke_studio',
    permissions: ['Upload videos to TikTok', 'Read profile info'],
    color: 'bg-zinc-800/50 text-white',
    borderColor: 'border-zinc-700'
  },
  {
    id: 'meta',
    name: 'Meta (FB & IG)',
    icon: '📘',
    status: 'disconnected',
    permissions: ['Manage pages', 'Publish as page', 'Instagram basic posting'],
    color: 'bg-blue-500/10 text-blue-400',
    borderColor: 'border-blue-500/30'
  },
  {
    id: 'linkedin',
    name: 'LinkedIn',
    icon: '💼',
    status: 'disconnected',
    permissions: ['Create posts', 'Manage organization pages'],
    color: 'bg-blue-700/10 text-blue-400',
    borderColor: 'border-blue-700/30'
  },
  {
    id: 'x',
    name: 'X (Twitter)',
    icon: '🐦',
    status: 'disconnected',
    permissions: ['Read and write tweets', 'Access user profile'],
    color: 'bg-gray-800/50 text-gray-300',
    borderColor: 'border-gray-600'
  }
];

export default function ConnectedAccountsPage() {
  const [platforms, setPlatforms] = useState(mockPlatforms);
  const [activeModal, setActiveModal] = useState<PlatformData | null>(null);

  const handleDisconnect = (id: Platform) => {
    setPlatforms(platforms.map(p => p.id === id ? { ...p, status: 'disconnected', accountName: undefined } : p));
  };

  const handleConnectConsent = (platform: PlatformData) => {
    // In a real app, this would redirect to OAuth after consent
    setPlatforms(platforms.map(p => p.id === platform.id ? { ...p, status: 'connected', accountName: 'New Account' } : p));
    setActiveModal(null);
  };

  return (
    <div className="min-h-screen bg-bg-primary text-text-primary p-6 md:p-12">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl md:text-4xl font-bold mb-2 gradient-text">Connected Accounts</h1>
        <p className="text-text-secondary mb-10">Manage your social media integrations and OAuth permissions.</p>

        <div className="grid gap-6 stagger-children">
          {platforms.map((platform) => (
            <div key={platform.id} className={`glass p-6 rounded-2xl border ${platform.borderColor} flex flex-col md:flex-row justify-between items-start md:items-center gap-6 transition-all duration-300 hover:shadow-lg`}>
              <div className="flex items-center gap-4">
                <div className={`w-14 h-14 rounded-full flex items-center justify-center text-2xl ${platform.color} border ${platform.borderColor}`}>
                  {platform.icon}
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white">{platform.name}</h2>
                  {platform.status === 'connected' ? (
                    <div className="flex flex-col gap-1 mt-1">
                      <span className="text-sm font-medium text-accent-green flex items-center gap-1">
                        <span className="w-2 h-2 rounded-full bg-accent-green animate-pulse"></span>
                        Connected as {platform.accountName}
                      </span>
                      <span className="text-xs text-text-muted">Permissions: {platform.permissions.join(', ')}</span>
                    </div>
                  ) : (
                    <span className="text-sm text-text-secondary mt-1 block">Not connected</span>
                  )}
                </div>
              </div>

              <div>
                {platform.status === 'connected' ? (
                  <button 
                    onClick={() => handleDisconnect(platform.id)}
                    className="px-5 py-2.5 rounded-lg border border-red-500/50 text-red-400 hover:bg-red-500/10 transition-colors text-sm font-semibold"
                  >
                    Disconnect
                  </button>
                ) : (
                  <button 
                    onClick={() => setActiveModal(platform)}
                    className="px-5 py-2.5 rounded-lg bg-accent-primary hover:bg-accent-secondary text-white transition-colors text-sm font-semibold shadow-lg shadow-accent-primary/20"
                  >
                    Connect
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Pre-connection OAuth consent notice modal */}
      {activeModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="glass p-8 rounded-2xl max-w-lg w-full border border-white/10 shadow-2xl animate-slide-up relative">
            <button 
              onClick={() => setActiveModal(null)}
              className="absolute top-4 right-4 text-text-muted hover:text-white transition-colors"
            >
              ✕
            </button>
            <div className="flex items-center gap-4 mb-6">
              <div className={`w-12 h-12 rounded-full flex items-center justify-center text-2xl ${activeModal.color} border ${activeModal.borderColor}`}>
                {activeModal.icon}
              </div>
              <h3 className="text-2xl font-bold text-white">Connect {activeModal.name}</h3>
            </div>
            
            <p className="text-text-secondary mb-6 leading-relaxed">
              Before we redirect you to {activeModal.name}, please review the permissions we are requesting. We only ask for what's strictly necessary to publish your content.
            </p>

            <div className="bg-bg-secondary p-4 rounded-xl border border-white/5 mb-6">
              <h4 className="text-sm font-semibold text-white mb-3 uppercase tracking-wider">Requested Permissions:</h4>
              <ul className="space-y-2">
                {activeModal.permissions.map((perm, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-text-secondary">
                    <span className="text-accent-primary mt-0.5">✓</span>
                    {perm}
                  </li>
                ))}
              </ul>
            </div>

            <div className="text-xs text-text-muted mb-8 space-y-2">
              <p>By connecting, you agree to the {activeModal.name} Terms of Service and our <a href="/privacy-policy" target="_blank" className="text-accent-secondary hover:underline">Privacy Policy</a>.</p>
              <p>You can revoke these permissions at any time from your settings or directly within your {activeModal.name} account.</p>
            </div>

            <div className="flex justify-end gap-4">
              <button 
                onClick={() => setActiveModal(null)}
                className="px-5 py-2.5 rounded-lg border border-white/10 text-text-secondary hover:text-white hover:bg-white/5 transition-colors text-sm font-semibold"
              >
                Cancel
              </button>
              <button 
                onClick={() => handleConnectConsent(activeModal)}
                className="px-5 py-2.5 rounded-lg bg-accent-primary hover:bg-accent-secondary text-white transition-colors text-sm font-semibold shadow-lg shadow-accent-primary/20"
              >
                Proceed to {activeModal.name}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
