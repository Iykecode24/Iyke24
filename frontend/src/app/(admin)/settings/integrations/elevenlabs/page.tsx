'use client';
import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import { CheckCircle, AlertCircle, Save, Key, Settings, Mic } from 'lucide-react';

export default function ElevenLabsSettingsPage() {
  const { toast } = useToast();
  const [isSaving, setIsSaving] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'error'>('connected');
  
  const [config, setConfig] = useState({
    apiKey: 'sk_12345**************************98765',
    defaultModel: 'eleven_multilingual_v2',
    enableSync: true,
  });

  const [stats, setStats] = useState({
    availableVoices: 45,
    customVoices: 12,
    characterLimit: 100000,
    characterCount: 45200,
  });

  const handleSave = async () => {
    setIsSaving(true);
    // Mock save
    await new Promise(r => setTimeout(r, 1000));
    toast.success('Settings Saved: ElevenLabs configuration updated successfully.');
    setIsSaving(false);
  };

  const handleTestConnection = async () => {
    setIsTesting(true);
    // Mock test
    await new Promise(r => setTimeout(r, 1500));
    setConnectionStatus('connected');
    toast.success('Connection Successful: Successfully connected to ElevenLabs API.');
    setIsTesting(false);
  };

  return (
    <div className="max-w-4xl mx-auto py-8 animate-fade-in space-y-8">
      <div className="flex items-center gap-4 mb-8">
        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-neutral-800 to-neutral-900 flex items-center justify-center border border-white/10 shadow-lg">
          <Mic className="text-white" size={24} />
        </div>
        <div>
          <h1 className="text-3xl font-bold mb-1 flex items-center gap-3">
            ElevenLabs Integration
            {connectionStatus === 'connected' && <Badge status="published">Connected</Badge>}
            {connectionStatus === 'error' && <Badge status="draft">Error</Badge>}
            {connectionStatus === 'disconnected' && <Badge status="draft">Disconnected</Badge>}
          </h1>
          <p className="text-text-secondary">Configure voice synthesis models and synchronize your voice library.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2 space-y-6">
          <Card className="p-6 space-y-6">
            <div className="flex items-center gap-2 mb-4 border-b border-white/5 pb-4">
              <Key className="text-accent-primary" size={20} />
              <h2 className="text-xl font-semibold">API Configuration</h2>
            </div>
            
            <div className="space-y-4">
              <Input
                label="API Key"
                type="password"
                value={config.apiKey}
                onChange={(e) => setConfig({ ...config, apiKey: e.target.value })}
                placeholder="sk_..."
              />
              <p className="text-sm text-text-muted">
                Your API key is stored securely and never exposed to the frontend directly.
              </p>
            </div>

            <div className="flex gap-4 pt-2">
              <Button onClick={handleSave} isLoading={isSaving} className="gap-2">
                <Save size={18} /> Save Config
              </Button>
              <Button onClick={handleTestConnection} isLoading={isTesting} variant="secondary" className="gap-2">
                <Settings size={18} /> Test Connection
              </Button>
            </div>
          </Card>

          <Card className="p-6 space-y-6">
            <div className="flex items-center gap-2 mb-4 border-b border-white/5 pb-4">
              <Settings className="text-accent-secondary" size={20} />
              <h2 className="text-xl font-semibold">Default Preferences</h2>
            </div>
            
            <div className="space-y-4">
              <Input
                as="select"
                label="Default Model"
                value={config.defaultModel}
                onChange={(e) => setConfig({ ...config, defaultModel: e.target.value })}
                options={[
                  { label: 'Eleven Multilingual v2', value: 'eleven_multilingual_v2' },
                  { label: 'Eleven Monolingual v1', value: 'eleven_monolingual_v1' },
                  { label: 'Eleven Turbo v2', value: 'eleven_turbo_v2' }
                ]}
              />
              
              <div className="flex items-center gap-3 pt-2">
                <input 
                  type="checkbox" 
                  id="enableSync" 
                  checked={config.enableSync}
                  onChange={(e) => setConfig({ ...config, enableSync: e.target.checked })}
                  className="w-5 h-5 rounded bg-bg-secondary border-white/20 text-accent-primary focus:ring-accent-primary focus:ring-offset-bg-primary"
                />
                <label htmlFor="enableSync" className="text-sm text-text-secondary cursor-pointer">
                  Automatically sync newly created voices from ElevenLabs
                </label>
              </div>
            </div>
          </Card>
        </div>

        <div className="space-y-6">
          <Card className="p-6 bg-gradient-to-br from-bg-secondary to-bg-primary border-accent-primary/20">
            <h3 className="font-semibold mb-4 text-white">Usage & Quotas</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-text-secondary">Characters Used</span>
                  <span className="font-medium text-white">
                    {stats.characterCount.toLocaleString()} / {stats.characterLimit.toLocaleString()}
                  </span>
                </div>
                <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-accent-primary transition-all duration-1000"
                    style={{ width: `${(stats.characterCount / stats.characterLimit) * 100}%` }}
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4 pt-4 border-t border-white/5">
                <div>
                  <p className="text-2xl font-bold text-white">{stats.availableVoices}</p>
                  <p className="text-xs text-text-muted">Premade Voices</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-accent-secondary">{stats.customVoices}</p>
                  <p className="text-xs text-text-muted">Custom Clones</p>
                </div>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <h3 className="font-semibold mb-3 text-white flex items-center gap-2">
              <AlertCircle size={16} className="text-accent-gold" /> Need Help?
            </h3>
            <p className="text-sm text-text-secondary mb-4">
              To find your API key, sign in to your ElevenLabs account, click on your profile icon in the bottom left, and select Profile.
            </p>
            <Button variant="secondary" className="w-full text-sm">View Documentation</Button>
          </Card>
        </div>
      </div>
    </div>
  );
}
