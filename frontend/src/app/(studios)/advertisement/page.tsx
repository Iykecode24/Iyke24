'use client';
import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ArrowRight, ArrowLeft, Wand2, Megaphone, ShoppingBag, Target } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function AdStudioPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);

  // Form State
  const [formData, setFormData] = useState({
    title: '',
    productDescription: '',
    platform: 'Instagram Reels',
    callToAction: 'Shop Now',
    tone: 'High-Energy'
  });

  const updateForm = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleGenerate = () => {
    setIsGenerating(true);
    setTimeout(() => {
      router.push('/projects/new-ad-project');
    }, 2000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in pb-12">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-accent-gold to-accent-red mb-4 shadow-lg shadow-accent-gold/20">
          <Megaphone size={32} className="text-white" />
        </div>
        <h1 className="text-4xl font-bold mb-2">Advertisement Studio</h1>
        <p className="text-text-secondary text-lg">Generate high-converting product ads for social media.</p>
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
        {/* Step 1: Product */}
        {step === 1 && (
          <div className="space-y-6 animate-slide-in">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <ShoppingBag className="text-accent-gold" /> 1. Product Details
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Campaign Title</label>
                <Input 
                  placeholder="e.g. Summer Sneaker Sale" 
                  value={formData.title}
                  onChange={(e) => updateForm('title', e.target.value)}
                  className="text-lg py-6"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">What are we selling?</label>
                <textarea 
                  placeholder="Describe your product, its key benefits, and why people need it..." 
                  value={formData.productDescription}
                  onChange={(e) => updateForm('productDescription', e.target.value)}
                  className="w-full h-32 bg-bg-primary border border-white/10 rounded-xl p-4 text-white focus:outline-none focus:ring-2 focus:ring-accent-gold focus:border-transparent transition-all resize-none"
                />
              </div>
            </div>
          </div>
        )}

        {/* Step 2: Target & Format */}
        {step === 2 && (
          <div className="space-y-6 animate-slide-in">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Target className="text-accent-red" /> 2. Strategy & Platform
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">Platform Format</label>
                <div className="space-y-2">
                  {['Instagram Reels', 'TikTok Video', 'YouTube Shorts', 'Facebook Feed (Square)'].map(platform => (
                    <button
                      key={platform}
                      onClick={() => updateForm('platform', platform)}
                      className={`w-full p-3 rounded-lg border text-left transition-all ${
                        formData.platform === platform 
                        ? 'border-accent-gold bg-accent-gold/10 text-white' 
                        : 'border-white/10 bg-bg-primary text-text-muted hover:border-white/20 hover:text-white'
                      }`}
                    >
                      {platform}
                    </button>
                  ))}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">Ad Vibe</label>
                <div className="space-y-2">
                  {['High-Energy / Urgent', 'UGC Style (User Generated)', 'Cinematic & Premium', 'Funny / Meme'].map(tone => (
                    <button
                      key={tone}
                      onClick={() => updateForm('tone', tone)}
                      className={`w-full p-3 rounded-lg border text-left transition-all ${
                        formData.tone === tone 
                        ? 'border-accent-red bg-accent-red/10 text-white' 
                        : 'border-white/10 bg-bg-primary text-text-muted hover:border-white/20 hover:text-white'
                      }`}
                    >
                      {tone}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">Call to Action</label>
              <Input 
                placeholder="e.g. Shop Now, Learn More, Swipe Up" 
                value={formData.callToAction}
                onChange={(e) => updateForm('callToAction', e.target.value)}
              />
            </div>
          </div>
        )}

        {/* Step 3: Generation */}
        {step === 3 && (
          <div className="space-y-6 animate-slide-in">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Wand2 className="text-accent-primary" /> 3. Generate Campaign
            </h2>
            
            <div className="bg-bg-primary p-6 rounded-xl border border-white/5 space-y-4">
              <h3 className="text-lg font-bold text-white border-b border-white/10 pb-2">Campaign Summary</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div><span className="text-text-muted">Campaign:</span> <span className="text-white font-medium">{formData.title || 'Untitled'}</span></div>
                <div><span className="text-text-muted">Platform:</span> <span className="text-white font-medium">{formData.platform}</span></div>
                <div><span className="text-text-muted">Vibe:</span> <span className="text-white font-medium">{formData.tone}</span></div>
                <div><span className="text-text-muted">CTA:</span> <span className="text-white font-medium">{formData.callToAction}</span></div>
              </div>
            </div>
            
            <Button 
              className="w-full py-6 text-lg bg-gradient-to-r from-accent-gold to-accent-red hover:opacity-90 transition-opacity border-0 text-white"
              disabled={!formData.title || !formData.productDescription || isGenerating}
              onClick={handleGenerate}
            >
              {isGenerating ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Generating Ad Concepts & Visuals...
                </span>
              ) : (
                <span className="flex items-center justify-center gap-2">
                  <Wand2 size={20} /> Create Ad Campaign
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
              disabled={step === 1 && (!formData.title || !formData.productDescription)}
            >
              Next Step <ArrowRight size={16} />
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
}
