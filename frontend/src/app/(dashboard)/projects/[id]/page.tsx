'use client';
import React, { useEffect, useState } from 'react';
import { useParams, useSearchParams } from 'next/navigation';
import { Card } from '@/components/ui/card';
import { Tabs } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { ProgressBar } from '@/components/ui/progress-bar';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';
import { Project, Script, Scene } from '@/types';
import { Loader2, Film, AlignLeft, Clapperboard, Users, MonitorPlay, Save, CheckCircle2 } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

/* ── Inner Components for Tabs ── */

const ScriptEditor = ({ script, onSave }: { script: Script | null, onSave: (script: Script) => void }) => {
  const [content, setContent] = useState(script?.fullText || '');

  useEffect(() => {
    if (script?.fullText !== undefined) {
      setContent(script.fullText);
    }
  }, [script?.fullText]);

  if (!script) {
    return <div className="text-center p-8 text-text-muted">No script available yet.</div>;
  }

  return (
    <div className="space-y-4 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold">Screenplay</h3>
          <p className="text-sm text-text-muted">Edit the generated script before production.</p>
        </div>
        <Button onClick={() => onSave({ ...script, fullText: content })} size="sm" className="gap-2">
          <Save size={16} /> Save Changes
        </Button>
      </div>
      
      <div className="glass-static rounded-xl overflow-hidden border border-white/10">
        <textarea 
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full h-[600px] bg-transparent p-6 text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary/50 resize-y font-mono text-sm leading-relaxed"
          placeholder="INT. SCENE 1 - DAY..."
        />
      </div>
    </div>
  );
};

const SceneBreakdown = ({ scenes }: { scenes: Scene[] }) => {
  if (!scenes || scenes.length === 0) {
    return <div className="text-center p-8 text-text-muted">No scenes generated yet.</div>;
  }

  return (
    <div className="space-y-4 animate-fade-in">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-bold">Scene Breakdown</h3>
        <Button size="sm">Generate Images</Button>
      </div>

      <div className="space-y-4">
        {scenes.map((scene, idx) => (
          <div key={scene.id} className="glass-static rounded-xl p-4 border border-white/5 flex gap-4 hover:border-white/10 transition-colors">
            <div className="w-12 h-12 rounded-lg bg-bg-secondary flex flex-col items-center justify-center shrink-0 border border-white/10">
              <span className="text-xs text-text-muted font-bold">SCENE</span>
              <span className="text-lg font-bold text-accent-primary">{scene.orderIndex}</span>
            </div>
            
            <div className="flex-1 min-w-0">
              <h4 className="font-bold text-sm mb-1 truncate">{scene.title || `Scene ${idx + 1}`}</h4>
              <p className="text-sm text-text-secondary line-clamp-2 mb-2">{scene.description}</p>
              
              <div className="grid grid-cols-2 gap-4 mt-4 p-3 bg-bg-secondary/50 rounded-lg">
                <div>
                  <span className="text-xs text-text-muted font-semibold mb-1 block">VISUAL PROMPT</span>
                  <p className="text-xs text-text-primary line-clamp-2">{scene.visualPrompt || 'Auto-generated visual prompt will appear here.'}</p>
                </div>
                <div>
                  <span className="text-xs text-text-muted font-semibold mb-1 block">DIALOGUE / NARRATION</span>
                  <p className="text-xs text-text-primary line-clamp-2">{scene.dialogue || scene.narration || 'No dialogue.'}</p>
                </div>
              </div>
            </div>
            
            <div className="w-32 shrink-0 flex flex-col items-end justify-between">
              <Badge status={scene.status} />
              <div className="text-xs text-text-muted">{scene.durationSeconds}s</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};


/* ── Main Page Component ── */

export default function ProjectDetail() {
  const params = useParams();
  const searchParams = useSearchParams();
  const { toast } = useToast();
  
  const projectId = params?.id as string;
  const isGenerating = searchParams?.get('generating') === 'true';

  const [project, setProject] = useState<Project | null>(null);
  const [script, setScript] = useState<Script | null>(null);
  const [scenes, setScenes] = useState<Scene[]>([]);
  const [loading, setLoading] = useState(true);
  const [generationProgress, setGenerationProgress] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const p = await api.getProject(projectId);
        setProject(p);
        
        try {
          const s = await api.getScript(projectId);
          setScript(s);
          const sc = await api.getScenes(projectId);
          setScenes(sc);
        } catch (e) {
          // Script might not exist yet
          console.warn("Script/Scenes not found yet");
        }
      } catch (error) {
        toast.error('Error: Failed to load project details');
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Mock progress if generating
    if (isGenerating) {
      const interval = setInterval(() => {
        setGenerationProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval);
            return 100;
          }
          return prev + 5;
        });
      }, 500);
      return () => clearInterval(interval);
    }
  }, [projectId, isGenerating, toast]);

  const handleSaveScript = async (updatedScript: Script) => {
    try {
      const saved = await api.updateScript(updatedScript.id, updatedScript);
      setScript(saved);
      toast.success('Saved: Script saved successfully');
    } catch (e) {
      toast.error('Error: Failed to save script');
    }
  };

  if (loading) {
    return <div className="flex h-[500px] items-center justify-center"><Loader2 className="animate-spin text-accent-primary" size={32} /></div>;
  }

  if (!project) {
    return <div className="text-center p-10">Project not found.</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-purple-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-purple-500/20 shrink-0">
             <Film className="text-white" size={32} />
          </div>
          <div>
            <h1 className="text-3xl font-bold mb-2 tracking-tight">{project.title}</h1>
            <div className="flex gap-3 text-sm text-text-secondary items-center">
              <span className="capitalize font-medium">{project.contentType}</span>
              <span>•</span>
              <span>{project.durationSeconds}s</span>
              <span>•</span>
              <span className="capitalize">{project.resolution}</span>
              <span>•</span>
              <Badge status={project.status} />
            </div>
          </div>
        </div>
        <div className="w-64 bg-bg-secondary p-3 rounded-xl border border-white/5">
          <ProgressBar
          progress={isGenerating ? generationProgress : project.progressPercent}
          label={isGenerating ? "Generating Script..." : "Overall Progress"}
        /></div>
      </div>

      {isGenerating && generationProgress < 100 && (
        <Card className="p-8 text-center animate-pulse-glow border-accent-primary/50 bg-accent-primary/5">
          <Loader2 className="animate-spin mx-auto text-accent-primary mb-4" size={40} />
          <h3 className="text-xl font-bold mb-2 text-white">AI is writing your masterpiece...</h3>
          <p className="text-text-secondary max-w-md mx-auto">
            Our AI orchestrator is expanding your idea into a full script, creating character profiles, and breaking down scenes for visual generation.
          </p>
        </Card>
      )}

      {(!isGenerating || generationProgress === 100) && (
        <Card className="min-h-[600px] border-white/5 shadow-xl bg-bg-card/80 backdrop-blur-xl">
          <Tabs tabs={[
            { 
              id: 'overview', 
              label: 'Overview', 
              icon: <Film size={16} />,
              content: (
                <div className="p-4 space-y-6 animate-fade-in">
                   <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                     <div className="glass-static rounded-xl p-5 border border-white/5">
                        <h4 className="font-bold mb-4 text-accent-primary">Project Details</h4>
                        <dl className="space-y-3 text-sm">
                          <div className="flex justify-between"><dt className="text-text-muted">Genre</dt><dd className="capitalize text-white">{project.genre || 'N/A'}</dd></div>
                          <div className="flex justify-between"><dt className="text-text-muted">Target Audience</dt><dd className="capitalize text-white">{project.targetAudience || 'N/A'}</dd></div>
                          <div className="flex justify-between"><dt className="text-text-muted">Visual Style</dt><dd className="capitalize text-white">{project.visualStyle || 'N/A'}</dd></div>
                          <div className="flex justify-between"><dt className="text-text-muted">Voice</dt><dd className="capitalize text-white">{project.voicePreference || 'N/A'}</dd></div>
                          <div className="flex justify-between"><dt className="text-text-muted">Music</dt><dd className="capitalize text-white">{project.musicPreference || 'N/A'}</dd></div>
                        </dl>
                     </div>
                     <div className="glass-static rounded-xl p-5 border border-white/5">
                        <h4 className="font-bold mb-4 text-accent-gold">Financials & Usage</h4>
                        <dl className="space-y-3 text-sm">
                          <div className="flex justify-between"><dt className="text-text-muted">Estimated Cost</dt><dd className="font-mono text-white">${project.estimatedCost.toFixed(2)}</dd></div>
                          <div className="flex justify-between"><dt className="text-text-muted">Actual Cost</dt><dd className="font-mono text-white">${project.actualCost.toFixed(2)}</dd></div>
                          <div className="flex justify-between"><dt className="text-text-muted">Created</dt><dd className="text-white">{new Date(project.createdAt).toLocaleDateString()}</dd></div>
                        </dl>
                     </div>
                   </div>
                </div>
              ) 
            },
            { 
              id: 'script', 
              label: 'Script', 
              icon: <AlignLeft size={16} />,
              content: <div className="p-4"><ScriptEditor script={script} onSave={handleSaveScript} /></div> 
            },
            { 
              id: 'scenes', 
              label: 'Scenes', 
              icon: <Clapperboard size={16} />,
              content: <div className="p-4"><SceneBreakdown scenes={scenes} /></div> 
            },
            { 
              id: 'characters', 
              label: 'Characters', 
              icon: <Users size={16} />,
              content: <div className="p-4 text-center text-text-muted">Character models and LoRA references will appear here.</div> 
            },
            { 
              id: 'render', 
              label: 'Render Queue', 
              icon: <MonitorPlay size={16} />,
              content: <div className="p-4 text-center text-text-muted">Active GPU jobs will appear here.</div> 
            }
          ]} />
        </Card>
      )}
    </div>
  );
}
