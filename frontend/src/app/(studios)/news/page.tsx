'use client';
import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ArrowRight, ArrowLeft, Wand2, Newspaper, Radio, Globe } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function NewsStudioPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);

  // Form State
  const [formData, setFormData] = useState({
    title: '',
    articleUrl: '',
    topic: '',
    tone: 'Professional & Objective',
    anchorStyle: 'Modern Desk Anchor',
    duration: '2min'
  });

  const updateForm = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleGenerate = () => {
    setIsGenerating(true);
    setTimeout(() => {
      router.push('/projects/new-news-project');
    }, 2000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in pb-12">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-accent-primary to-accent-blue mb-4 shadow-lg shadow-accent-blue/20">
          <Newspaper size={32} className="text-white" />
        </div>
        <h1 className="text-4xl font-bold mb-2">News Video Studio</h1>
        <p className="text-text-secondary text-lg">Turn articles and topics into professional broadcast videos.</p>
      </div>

      {/* Progress Wizard */}
      <div className="flex items-center justify-center mb-12">
        {[1, 2, 3].map((i) => (
          <React.Fragment key={i}>
            <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm transition-colors ${
              step >= i ? 'bg-accent-primary text-white shadow-lg shadow-accent-primary/20' : 'bg-bg-secondary text-text-muted border border-white/10'
            }`}>
              {i}
            </div>
            {i < 3 && (
              <div className={`w-16 h-1 transition-colors ${
                step > i ? 'bg-accent-primary' : 'bg-bg-secondary border-y border-white/5'
              }`} />
            )}
          </React.Fragment>
        ))}
      </div>

      <Card className="p-8 border-white/10 bg-bg-card/80 backdrop-blur-xl relative overflow-hidden">
        {/* Step 1: Source Material */}
        {step === 1 && (
          <div className="space-y-6 animate-slide-in">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Globe className="text-accent-blue" /> 1. Source Material
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Headline / Project Title</label>
                <Input 
                  placeholder="e.g. Tech Giants Announce AI Breakthrough" 
                  value={formData.title}
                  onChange={(e) => updateForm('title', e.target.value)}
                  className="text-lg py-6"
                />
              </div>
              
              <div className="pt-4 border-t border-white/10 relative">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-bg-card px-3 text-xs text-text-muted uppercase font-bold tracking-wider">
                  Option A: URL
                </div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Article URL to Summarize</label>
                <Input 
                  placeholder="https://..." 
                  value={formData.articleUrl}
                  onChange={(e) => updateForm('articleUrl', e.target.value)}
                />
              </div>
              
              <div className="pt-4 border-t border-white/10 relative">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-bg-card px-3 text-xs text-text-muted uppercase font-bold tracking-wider">
                  Option B: Custom Topic
                </div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Paste Text or Topic Details</label>
                <textarea 
                  placeholder="Type the news content, press release, or bulletin notes here..." 
                  value={formData.topic}
                  onChange={(e) => updateForm('topic', e.target.value)}
                  className="w-full h-32 bg-bg-primary border border-white/10 rounded-xl p-4 text-white focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent transition-all resize-none"
                />
              </div>
            </div>
          </div>
        )}

        {/* Step 2: Format & Anchor */}
        {step === 2 && (
          <div className="space-y-6 animate-slide-in">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Radio className="text-accent-primary" /> 2. Broadcast Format
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">Editorial Tone</label>
                <div className="space-y-2">
                  {['Professional & Objective', 'Urgent Breaking News', 'Casual / Talk Show', 'Satirical'].map(tone => (
                    <button
                      key={tone}
                      onClick={() => updateForm('tone', tone)}
                      className={`w-full p-3 rounded-lg border text-left transition-all ${
                        formData.tone === tone 
                        ? 'border-accent-blue bg-accent-blue/10 text-white' 
                        : 'border-white/10 bg-bg-primary text-text-muted hover:border-white/20 hover:text-white'
                      }`}
                    >
                      {tone}
                    </button>
                  ))}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">Visual Anchor Style</label>
                <div className="space-y-2">
                  {['Modern Desk Anchor', 'On-Location Reporter', 'Documentary Voiceover (No Anchor)', 'Podcast Studio Setup'].map(style => (
                    <button
                      key={style}
                      onClick={() => updateForm('anchorStyle', style)}
                      className={`w-full p-3 rounded-lg border text-left transition-all ${
                        formData.anchorStyle === style 
                        ? 'border-accent-primary bg-accent-primary/10 text-white' 
                        : 'border-white/10 bg-bg-primary text-text-muted hover:border-white/20 hover:text-white'
                      }`}
                    >
                      {style}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Generation */}
        {step === 3 && (
          <div className="space-y-6 animate-slide-in">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Wand2 className="text-accent-primary" /> 3. Go Live
            </h2>
            
            <div className="bg-bg-primary p-6 rounded-xl border border-white/5 space-y-4">
              <h3 className="text-lg font-bold text-white border-b border-white/10 pb-2">Broadcast Summary</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div><span className="text-text-muted">Headline:</span> <span className="text-white font-medium">{formData.title || 'Untitled'}</span></div>
                <div><span className="text-text-muted">Tone:</span> <span className="text-white font-medium">{formData.tone}</span></div>
                <div><span className="text-text-muted">Format:</span> <span className="text-white font-medium">{formData.anchorStyle}</span></div>
                <div><span className="text-text-muted">Source:</span> <span className="text-white font-medium">{formData.articleUrl ? 'URL Import' : 'Custom Text'}</span></div>
              </div>
            </div>
            
            <Button 
              className="w-full py-6 text-lg bg-gradient-to-r from-accent-primary to-accent-blue hover:opacity-90 transition-opacity border-0"
              disabled={!formData.title || (!formData.articleUrl && !formData.topic) || isGenerating}
              onClick={handleGenerate}
            >
              {isGenerating ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Generating Broadcast Script & B-Roll...
                </span>
              ) : (
                <span className="flex items-center justify-center gap-2">
                  <Wand2 size={20} /> Create News Broadcast
                </span>
              )}
            </Button>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="flex justify-between mt-8 pt-6 border-t border-white/10">
          <Button 
            variant="ghost" 
            onClick={() => setStep(s => Math.max(1, s - 1))}
            className={step === 1 ? 'invisible' : 'flex gap-2'}
            disabled={isGenerating}
          >
            <ArrowLeft size={16} /> Back
          </Button>
          
          {step < 3 && (
            <Button 
              className="gap-2 bg-white/10 hover:bg-white/20 text-white"
              onClick={() => setStep(s => Math.min(3, s + 1))}
              disabled={step === 1 && (!formData.title || (!formData.articleUrl && !formData.topic))}
            >
              Next Step <ArrowRight size={16} />
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
}
