'use client';
import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  Server, Cpu, Activity, Play, Square, Trash2, Power, 
  Database, RefreshCw, AlertTriangle, Key, Terminal, ExternalLink,
  Download, Wrench, Eraser, HardDrive
} from 'lucide-react';

const MOCK_PODS = [
  { id: '1qaz2wsx3edc', name: 'Render-Node-01', gpu: 'RTX 4090 (24GB)', status: 'RUNNING', cost: '$0.74/hr', uptime: '4h 12m' },
  { id: '9okm8ijn7uhb', name: 'ComfyUI-Worker', gpu: 'A100 (80GB)', status: 'STOPPED', cost: '$1.89/hr', uptime: '-' },
  { id: '5tgb6yhn7ujm', name: 'Video-Upscaler', gpu: 'RTX 4090 (24GB)', status: 'RUNNING', cost: '$0.74/hr', uptime: '1h 05m' }
];

const MOCK_VOLUMES = [
  { id: 'vol-1234', name: 'Model-Storage-Main', used: 320, total: 500, datacenter: 'EU-RO-1' },
  { id: 'vol-5678', name: 'Cache-Volume', used: 45, total: 100, datacenter: 'US-TX-1' }
];

export default function GpuPage() {
  const [apiKey, setApiKey] = useState('********************************');
  const [isSyncing, setIsSyncing] = useState(false);

  const handleSync = () => {
    setIsSyncing(true);
    setTimeout(() => setIsSyncing(false), 1500);
  };

  return (
    <div className="space-y-8 animate-fade-in pb-12">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold mb-1">GPU Infrastructure</h1>
          <p className="text-text-secondary">Manage your RunPod instances, serverless endpoints, and network volumes.</p>
        </div>
        <div className="flex gap-3">
          <Button variant="secondary" className="gap-2" onClick={handleSync} disabled={isSyncing}>
            <RefreshCw size={16} className={isSyncing ? 'animate-spin' : ''} /> Sync Status
          </Button>
          <Button className="gap-2 bg-gradient-to-r from-accent-purple to-accent-blue text-white border-0">
            <Server size={18} /> Provision New Pod
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-6 bg-bg-card/50 border-white/10 flex items-center gap-4">
          <div className="p-4 rounded-xl bg-accent-blue/10 text-accent-blue border border-accent-blue/20">
            <Activity size={24} />
          </div>
          <div>
            <div className="text-sm text-text-muted">Total Active Pods</div>
            <div className="text-2xl font-bold text-white">2 <span className="text-sm font-normal text-text-secondary">/ 5 Limit</span></div>
          </div>
        </Card>
        
        <Card className="p-6 bg-bg-card/50 border-white/10 flex items-center gap-4">
          <div className="p-4 rounded-xl bg-accent-purple/10 text-accent-purple border border-accent-purple/20">
            <Cpu size={24} />
          </div>
          <div>
            <div className="text-sm text-text-muted">Current Burn Rate</div>
            <div className="text-2xl font-bold text-white">$1.48<span className="text-sm font-normal text-text-secondary">/hr</span></div>
          </div>
        </Card>

        <Card className="p-6 bg-bg-card/50 border-white/10 flex items-center gap-4">
          <div className="p-4 rounded-xl bg-accent-green/10 text-accent-green border border-accent-green/20">
            <Power size={24} />
          </div>
          <div>
            <div className="text-sm text-text-muted">API Connection</div>
            <div className="text-2xl font-bold text-white flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-accent-green shadow-[0_0_10px_rgba(34,197,94,0.5)]"></div>
              Healthy
            </div>
          </div>
        </Card>
      </div>

      {/* RunPod API Key Configuration */}
      <Card className="border-white/10 bg-bg-card/30 overflow-hidden">
        <div className="p-4 border-b border-white/10 bg-white/5 flex items-center gap-2">
          <Key size={18} className="text-text-muted" />
          <h2 className="font-bold text-white">RunPod Authentication</h2>
        </div>
        <div className="p-6 flex items-end gap-4 max-w-2xl">
          <div className="flex-1 space-y-2">
            <label className="text-sm font-medium text-text-secondary">API Key</label>
            <Input 
              type="password" 
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="font-mono bg-bg-primary/50"
            />
          </div>
          <Button variant="secondary">Update Key</Button>
          <Button variant="outline" className="gap-2">
            Test Connection <ExternalLink size={14} />
          </Button>
        </div>
      </Card>

      {/* Active GPU Pods */}
      <Card className="border-white/10 bg-bg-card/50 overflow-hidden">
        <div className="p-4 border-b border-white/10 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Terminal size={18} className="text-text-muted" />
            <h2 className="font-bold text-white text-lg">Active GPU Pods</h2>
          </div>
        </div>
        
        <div className="p-0">
          <div className="px-6 py-3 bg-white/5 text-xs font-bold text-text-muted uppercase tracking-wider grid grid-cols-12 gap-4 items-center border-b border-white/5">
            <div className="col-span-3">Pod ID / Name</div>
            <div className="col-span-3">GPU Type</div>
            <div className="col-span-2 text-center">Status</div>
            <div className="col-span-2 text-center">Uptime / Cost</div>
            <div className="col-span-2 text-right">Actions</div>
          </div>

          {MOCK_PODS.map(pod => (
            <div key={pod.id} className="px-6 py-4 grid grid-cols-12 gap-4 items-center border-b border-white/5 hover:bg-white/5 transition-colors group">
              <div className="col-span-3">
                <div className="font-bold text-white text-sm">{pod.name}</div>
                <div className="text-xs text-text-muted font-mono mt-0.5">{pod.id}</div>
              </div>
              
              <div className="col-span-3 flex items-center gap-2">
                <Cpu size={14} className="text-text-secondary" />
                <span className="text-sm text-text-primary">{pod.gpu}</span>
              </div>

              <div className="col-span-2 flex justify-center">
                {pod.status === 'RUNNING' ? (
                  <Badge className="bg-accent-green/10 text-accent-green border-accent-green/20 gap-1 font-medium">
                    <div className="w-1.5 h-1.5 rounded-full bg-accent-green animate-pulse"></div> RUNNING
                  </Badge>
                ) : (
                  <Badge className="bg-white/5 text-text-secondary border-white/10 gap-1 font-medium">
                    <Square size={10} className="fill-current" /> STOPPED
                  </Badge>
                )}
              </div>

              <div className="col-span-2 text-center">
                <div className="text-sm font-medium text-white">{pod.uptime}</div>
                <div className="text-[10px] text-text-muted">{pod.cost}</div>
              </div>

              <div className="col-span-2 flex justify-end gap-2 opacity-100 md:opacity-0 md:group-hover:opacity-100 transition-opacity">
                {pod.status === 'STOPPED' ? (
                  <Button variant="secondary" size="sm" className="h-8 px-2 text-accent-green hover:text-accent-green hover:bg-accent-green/10"><Play size={14} /></Button>
                ) : (
                  <Button variant="secondary" size="sm" className="h-8 px-2 text-accent-red hover:text-accent-red hover:bg-accent-red/10"><Square size={14} /></Button>
                )}
                <Button variant="danger" size="sm" className="h-8 px-2"><Trash2 size={14} /></Button>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Network Volumes */}
      <Card className="border-white/10 bg-bg-card/50 overflow-hidden">
        <div className="p-4 border-b border-white/10 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Database size={18} className="text-text-muted" />
            <h2 className="font-bold text-white text-lg">Network Volumes</h2>
          </div>
          <Button variant="secondary" size="sm" className="h-8 text-xs">Create Volume</Button>
        </div>
        
        <div className="p-0">
          <div className="px-6 py-3 bg-white/5 text-xs font-bold text-text-muted uppercase tracking-wider grid grid-cols-12 gap-4 items-center border-b border-white/5">
            <div className="col-span-4">Volume Name</div>
            <div className="col-span-3">Volume ID</div>
            <div className="col-span-2">Datacenter</div>
            <div className="col-span-2 text-center">Size</div>
            <div className="col-span-1 text-right">Actions</div>
          </div>

          {MOCK_VOLUMES.map(vol => (
            <div key={vol.id} className="px-6 py-4 grid grid-cols-12 gap-4 items-center border-b border-white/5 hover:bg-white/5 transition-colors">
              <div className="col-span-4 font-bold text-white text-sm">{vol.name}</div>
              <div className="col-span-3 text-sm text-text-muted font-mono">{vol.id}</div>
              <div className="col-span-2 text-sm text-text-primary">{vol.datacenter}</div>
              <div className="col-span-2 flex flex-col gap-1">
                <div className="flex justify-between text-[10px] text-text-muted">
                  <span>{vol.used}GB Used</span>
                  <span>{vol.total}GB Total</span>
                </div>
                <div className="w-full bg-white/10 rounded-full h-1.5">
                  <div className={`h-1.5 rounded-full ${vol.used / vol.total > 0.8 ? 'bg-accent-red' : 'bg-accent-blue'}`} style={{ width: `${(vol.used / vol.total) * 100}%` }}></div>
                </div>
              </div>
              <div className="col-span-1 flex justify-end">
                <Button variant="ghost" size="sm" className="h-8 w-8 p-0 text-accent-red hover:bg-accent-red/10 hover:text-accent-red"><Trash2 size={14} /></Button>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* System Maintenance */}
      <Card className="border-white/10 bg-bg-card/50 overflow-hidden">
        <div className="p-4 border-b border-white/10 flex items-center gap-2">
          <HardDrive size={18} className="text-text-muted" />
          <h2 className="font-bold text-white text-lg">System Maintenance</h2>
        </div>
        <div className="p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Button variant="outline" className="h-auto py-4 flex flex-col items-center gap-2 hover:bg-accent-blue/10 hover:text-accent-blue hover:border-accent-blue/50 transition-colors">
            <Download size={24} />
            <span className="font-medium">Install Core Models</span>
          </Button>
          <Button variant="outline" className="h-auto py-4 flex flex-col items-center gap-2 hover:bg-accent-purple/10 hover:text-accent-purple hover:border-accent-purple/50 transition-colors">
            <RefreshCw size={24} />
            <span className="font-medium">Update ComfyUI</span>
          </Button>
          <Button variant="outline" className="h-auto py-4 flex flex-col items-center gap-2 hover:bg-accent-yellow/10 hover:text-accent-yellow hover:border-accent-yellow/50 transition-colors">
            <Eraser size={24} />
            <span className="font-medium">Clean Cache</span>
          </Button>
          <Button variant="outline" className="h-auto py-4 flex flex-col items-center gap-2 hover:bg-accent-red/10 hover:text-accent-red hover:border-accent-red/50 transition-colors">
            <Wrench size={24} />
            <span className="font-medium">Repair Installation</span>
          </Button>
        </div>
      </Card>
      
      <div className="bg-accent-yellow/10 border border-accent-yellow/20 rounded-lg p-4 flex gap-3 text-accent-yellow/90">
        <AlertTriangle size={20} className="shrink-0" />
        <div className="text-sm">
          <strong>Cost Warning:</strong> Iyke Content Studio uses an automated watchdog worker to terminate idle GPU instances after 15 minutes of inactivity. However, Network Volumes incur continuous storage costs regardless of whether a Pod is running.
        </div>
      </div>
    </div>
  );
}
