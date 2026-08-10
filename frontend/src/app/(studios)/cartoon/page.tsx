'use client';
import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Sparkles, ArrowRight, ArrowLeft, Wand2, Star, Target } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function CartoonStudioPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);

  // Form State
  const [formData, setFormData] = useState({
    title: '',
    idea: '',
    targetAudience: 'Toddlers (2-4)',
    educationalTheme: 'None',
    animationStyle: '3D Pixar Style',
    duration: '5min',
    mainCharacter: ''
  });

  const updateForm = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleGenerate = () => {
    setIsGenerating(true);
    // Simulate API call for Project creation
    setTimeout(() => {
      // Navigate to project detail on success
      router.push('/projects/new-cartoon-project');
    }, 2000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in pb-12">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-accent-primary to-accent-pink mb-4 shadow-lg shadow-accent-pink/20">
          <Star size={32} className="text-white" />
        </div>
        <h1 className="text-4xl font-bold mb-2">Children's Cartoon Studio</h1>
        <p className="text-text-secondary text-lg">Create enchanting, age-appropriate animated shows.</p>
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
        {/* Step 1: The Magic Idea */}
        {step === 1 && (
          <div className="space-y-6 animate-slide-in">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Sparkles className="text-accent-pink" /> 1. The Magic Idea
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Show Title</label>
                <Input 
                  placeholder="e.g. The Adventures of Pip" 
                  value={formData.title}
                  onChange={(e) => updateForm('title', e.target.value)}
                  className="text-lg py-6"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Story Concept</label>
                <textarea 
                  placeholder="A brave little squirrel tries to find the biggest acorn in the magic forest..." 
                  value={formData.idea}
                  onChange={(e) => updateForm('idea', e.target.value)}
                  className="w-full h-32 bg-bg-primary border border-white/10 rounded-xl p-4 text-white focus:outline-none focus:ring-2 focus:ring-accent-pink focus:border-transparent transition-all resize-none"
                />
              </div>
            </div>
          </div>
        )}

        {/* Step 2: Target & Theme */}
        {step === 2 && (
          <div className="space-y-6 animate-slide-in">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Target className="text-accent-blue" /> 2. Audience & Theme
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">Age Group</label>
                <div className="space-y-2">
                  {['Toddlers (2-4)', 'Preschool (4-6)', 'Kids (7-10)'].map(age => (
                    <button
                      key={age}
                      onClick={() => updateForm('targetAudience', age)}
                      className={`w-full p-3 rounded-lg border text-left transition-all ${
                        formData.targetAudience === age 
                        ? 'border-accent-blue bg-accent-blue/10 text-white' 
                        : 'border-white/10 bg-bg-primary text-text-muted hover:border-white/20 hover:text-white'
                      }`}
                    >
                      {age}
                    </button>
                  ))}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">Educational Theme</label>
                <div className="space-y-2">
                  {['None', 'Letters & Numbers', 'Social Emotional', 'Science & Nature'].map(theme => (
                    <button
                      key={theme}
                      onClick={() => updateForm('educationalTheme', theme)}
                      className={`w-full p-3 rounded-lg border text-left transition-all ${
                        formData.educationalTheme === theme 
                        ? 'border-accent-pink bg-accent-pink/10 text-white' 
                        : 'border-white/10 bg-bg-primary text-text-muted hover:border-white/20 hover:text-white'
                      }`}
                    >
                      {theme}
                    </button>
                  ))}
                </div>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1">Visual Style</label>
              <select 
                className="w-full bg-bg-primary border border-white/10 rounded-xl p-3 text-white focus:outline-none focus:ring-2 focus:ring-accent-blue"
                value={formData.animationStyle}
                onChange={(e) => updateForm('animationStyle', e.target.value)}
              >
                <option value="3D Pixar Style">3D Pixar Style</option>
                <option value="2D Flat Vector">2D Flat Vector</option>
                <option value="Watercolor Illustration">Watercolor Illustration</option>
                <option value="Stop Motion Clay">Stop Motion Clay</option>
              </select>
            </div>
          </div>
        )}

        {/* Step 3: Magic Generator */}
        {step === 3 && (
          <div className="space-y-6 animate-slide-in">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Wand2 className="text-accent-primary" /> 3. Create the Magic
            </h2>
            
            <div className="bg-bg-primary p-6 rounded-xl border border-white/5 space-y-4">
              <h3 className="text-lg font-bold text-white border-b border-white/10 pb-2">Production Summary</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div><span className="text-text-muted">Title:</span> <span className="text-white font-medium">{formData.title || 'Untitled'}</span></div>
                <div><span className="text-text-muted">Style:</span> <span className="text-white font-medium">{formData.animationStyle}</span></div>
                <div><span className="text-text-muted">Audience:</span> <span className="text-white font-medium">{formData.targetAudience}</span></div>
                <div><span className="text-text-muted">Education:</span> <span className="text-white font-medium">{formData.educationalTheme}</span></div>
              </div>
              <div>
                <span className="text-text-muted block mb-1">Story Concept:</span>
                <p className="text-white text-sm line-clamp-3 italic">"{formData.idea}"</p>
              </div>
            </div>
            
            <Button 
              className="w-full py-6 text-lg bg-gradient-to-r from-accent-primary to-accent-pink hover:opacity-90 transition-opacity border-0"
              disabled={!formData.title || !formData.idea || isGenerating}
              onClick={handleGenerate}
            >
              {isGenerating ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Generating Cartoon Pipeline...
                </span>
              ) : (
                <span className="flex items-center justify-center gap-2">
                  <Wand2 size={20} /> Create Cartoon Script & Storyboard
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
              disabled={step === 1 && (!formData.title || !formData.idea)}
            >
              Next Step <ArrowRight size={16} />
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
}
