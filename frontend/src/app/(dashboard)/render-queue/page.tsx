'use client';
import React from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { RefreshCw, Play, XCircle, Clock, Server, Film, AlertCircle } from 'lucide-react';

const MOCK_JOBS = [
  {
    id: 'job-1',
    projectId: 'proj-1',
    projectTitle: 'The Last Horizon',
    jobType: 'video_generation',
    status: 'rendering',
    progress: 45,
    gpuType: 'RTX 4090',
    startedAt: '10 mins ago',
    estimatedTimeLeft: '~15 mins'
  },
  {
    id: 'job-2',
    projectId: 'proj-2',
    projectTitle: 'Startup Explainer',
    jobType: 'audio_mixing',
    status: 'processing_audio',
    progress: 80,
    gpuType: 'CPU',
    startedAt: '2 mins ago',
    estimatedTimeLeft: '~30 secs'
  },
  {
    id: 'job-3',
    projectId: 'proj-3',
    projectTitle: 'Neon Nights',
    jobType: 'export',
    status: 'completed',
    progress: 100,
    gpuType: 'RTX A6000',
    startedAt: '1 hour ago',
    estimatedTimeLeft: 'None'
  },
  {
    id: 'job-4',
    projectId: 'proj-4',
    projectTitle: 'Kids Story Ep 5',
    jobType: 'video_generation',
    status: 'failed',
    progress: 12,
    gpuType: 'RTX 3090',
    startedAt: '2 hours ago',
    errorMessage: 'CUDA out of memory error during frame synthesis.'
  }
];

export default function RenderQueuePage() {
  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold mb-1">Render Queue</h1>
          <p className="text-text-secondary">Monitor your active AI generation and export jobs.</p>
        </div>
        <div className="flex gap-3">
          <Button variant="secondary" className="gap-2">
            <RefreshCw size={16} /> Refresh
          </Button>
          <Button className="gap-2 bg-accent-primary hover:bg-accent-primary/90 text-white">
            <Play size={16} /> Start Paused Jobs
          </Button>
        </div>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-4 bg-bg-secondary/50 border-white/5">
          <div className="text-text-muted text-sm mb-1">Active Jobs</div>
          <div className="text-2xl font-bold text-white flex items-center gap-2">
            <RefreshCw size={20} className="text-accent-secondary animate-spin-slow" /> 2
          </div>
        </Card>
        <Card className="p-4 bg-bg-secondary/50 border-white/5">
          <div className="text-text-muted text-sm mb-1">Active GPUs</div>
          <div className="text-2xl font-bold text-white flex items-center gap-2">
            <Server size={20} className="text-accent-purple" /> 1
          </div>
        </Card>
        <Card className="p-4 bg-bg-secondary/50 border-white/5">
          <div className="text-text-muted text-sm mb-1">Completed Today</div>
          <div className="text-2xl font-bold text-white">14</div>
        </Card>
        <Card className="p-4 bg-bg-secondary/50 border-white/5">
          <div className="text-text-muted text-sm mb-1">Failed Jobs</div>
          <div className="text-2xl font-bold text-accent-red">1</div>
        </Card>
      </div>

      <div className="space-y-4">
        <h2 className="text-xl font-bold text-white border-b border-white/10 pb-2">Active & Recent Jobs</h2>
        
        {MOCK_JOBS.map((job) => (
          <Card key={job.id} className="p-0 overflow-hidden border-white/10 group">
            <div className="p-5 flex flex-col md:flex-row gap-6 items-center">
              {/* Job Info */}
              <div className="flex-1 w-full flex items-start gap-4">
                <div className="w-12 h-12 rounded-lg bg-bg-primary border border-white/10 flex items-center justify-center shrink-0">
                  <Film size={24} className={job.status === 'rendering' ? 'text-accent-secondary' : 'text-text-muted'} />
                </div>
                <div>
                  <h3 className="font-bold text-white text-lg">{job.projectTitle}</h3>
                  <div className="flex items-center gap-3 text-sm text-text-secondary mt-1">
                    <span className="uppercase tracking-wider text-[10px] bg-white/5 px-2 py-0.5 rounded border border-white/10">{job.jobType.replace('_', ' ')}</span>
                    <span className="flex items-center gap-1"><Server size={12} /> {job.gpuType}</span>
                    <span className="flex items-center gap-1"><Clock size={12} /> {job.startedAt}</span>
                  </div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="flex-1 w-full md:max-w-md">
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-white capitalize">{job.status.replace('_', ' ')}</span>
                  <span className="font-mono text-accent-primary">{job.progress}%</span>
                </div>
                <div className="w-full h-2 bg-bg-primary rounded-full overflow-hidden border border-white/5">
                  <div 
                    className={`h-full rounded-full transition-all duration-500 ease-out ${
                      job.status === 'failed' ? 'bg-accent-red' : 
                      job.status === 'completed' ? 'bg-accent-green' : 
                      'bg-gradient-to-r from-accent-primary to-accent-secondary relative overflow-hidden'
                    }`}
                    style={{ width: `${job.progress}%` }}
                  >
                    {/* Animated shine effect for active jobs */}
                    {['rendering', 'processing_audio'].includes(job.status) && (
                      <div className="absolute inset-0 -translate-x-full animate-shimmer bg-gradient-to-r from-transparent via-white/30 to-transparent"></div>
                    )}
                  </div>
                </div>
                {job.status === 'failed' && job.errorMessage && (
                  <div className="mt-2 text-xs text-accent-red flex items-center gap-1">
                    <AlertCircle size={12} /> {job.errorMessage}
                  </div>
                )}
                {['rendering', 'processing_audio'].includes(job.status) && (
                  <div className="mt-2 text-xs text-text-muted text-right">
                    ETA: {job.estimatedTimeLeft}
                  </div>
                )}
              </div>

              {/* Actions */}
              <div className="flex gap-2 w-full md:w-auto justify-end">
                {['rendering', 'processing_audio'].includes(job.status) ? (
                  <Button variant="danger" className="p-2 h-auto" title="Cancel Job">
                    <XCircle size={18} />
                  </Button>
                ) : job.status === 'failed' ? (
                  <Button variant="secondary" className="text-xs" title="Retry Job">
                    <RefreshCw size={14} className="mr-1" /> Retry
                  </Button>
                ) : (
                  <Button variant="secondary" className="text-xs">
                    View Project
                  </Button>
                )}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
