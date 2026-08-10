'use client';
import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ArrowRight, ArrowLeft, Wand2, Image as ImageIcon, Video, UploadCloud } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function ImageToVideoStudioPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);

  // Form State
  const [formData, setFormData] = useState({
    title: '',
    imagePrompt: '',
    motionPrompt: '',
    cameraMotion: 'Pan Right',
    duration: '5s'
  });

  const updateForm = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleGenerate = () => {
    setIsGenerating(true);
    setTimeout(() => {
      router.push('/projects/new-i2v-project');
    }, 2000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in pb-12">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-accent-purple to-accent-secondary mb-4 shadow-lg shadow-accent-purple/20">
          <ImageIcon size={32} className="text-white" />
        </div>
        <h1 className="text-4xl font-bold mb-2">Image to Video Studio</h1>
        <p className="text-text-secondary text-lg">Bring static images to life with advanced motion models.</p>
      </div>

      {/* Progress Wizard */}
      <div className="flex items-center justify-center mb-12">
        {[1, 2].map((i) => (
          <React.Fragment key={i}>
            <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm transition-colors ${
              step >= i ? 'bg-accent-primary text-white shadow-lg shadow-accent-primary/20' : 'bg-bg-secondary text-text-muted border border-white/10'
            }`}>
              {i}
            </div>
            {i < 2 && (
              <div className={`w-16 h-1 transition-colors ${
                step > i ? 'bg-accent-primary' : 'bg-bg-secondary border-y border-white/5'
              }`} />
            )}
          </React.Fragment>
        ))}
      </div>

      <Card className="p-8 border-white/10 bg-bg-card/80 backdrop-blur-xl relative overflow-hidden">
        {/* Step 1: The Image */}
        {step === 1 && (
          <div className="space-y-6 animate-slide-in">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <UploadCloud className="text-accent-purple" /> 1. Base Image
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Project Title</label>
                <Input 
                  placeholder="e.g. Cyberpunk Alley Animation" 
                  value={formData.title}
                  onChange={(e) => updateForm('title', e.target.value)}
                  className="text-lg py-6"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4">
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-2">Upload Image</label>
                  <div className="border-2 border-dashed border-white/10 rounded-xl p-8 flex flex-col items-center justify-center text-center bg-bg-primary hover:bg-white/5 transition-colors cursor-pointer h-48">
                    <UploadCloud size={32} className="text-text-muted mb-2" />
                    <span className="text-sm text-text-secondary">Drag & drop or click to upload</span>
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-2">Or Generate Image from Text</label>
                  <textarea 
                    placeholder="Describe the image you want to generate first..." 
                    value={formData.imagePrompt}
                    onChange={(e) => updateForm('imagePrompt', e.target.value)}
                    className="w-full h-48 bg-bg-primary border border-white/10 rounded-xl p-4 text-white focus:outline-none focus:ring-2 focus:ring-accent-purple focus:border-transparent transition-all resize-none"
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Step 2: Motion Settings */}
        {step === 2 && (
          <div className="space-y-6 animate-slide-in">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Video className="text-accent-secondary" /> 2. Motion Directing
            </h2>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-2">Motion Description (What happens?)</label>
                <textarea 
                  placeholder="e.g. Smoke billows from the vents, neon lights flicker, rain falls heavily..." 
                  value={formData.motionPrompt}
                  onChange={(e) => updateForm('motionPrompt', e.target.value)}
                  className="w-full h-24 bg-bg-primary border border-white/10 rounded-xl p-4 text-white focus:outline-none focus:ring-2 focus:ring-accent-secondary focus:border-transparent transition-all resize-none"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-2">Camera Motion</label>
                  <select 
                    className="w-full bg-bg-primary border border-white/10 rounded-xl p-3 text-white focus:outline-none focus:ring-2 focus:ring-accent-secondary"
                    value={formData.cameraMotion}
                    onChange={(e) => updateForm('cameraMotion', e.target.value)}
                  >
                    <option value="None / Static">None / Static</option>
                    <option value="Pan Right">Pan Right</option>
                    <option value="Pan Left">Pan Left</option>
                    <option value="Zoom In">Zoom In</option>
                    <option value="Zoom Out">Zoom Out</option>
                    <option value="Tilt Up">Tilt Up</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-2">Duration</label>
                  <select 
                    className="w-full bg-bg-primary border border-white/10 rounded-xl p-3 text-white focus:outline-none focus:ring-2 focus:ring-accent-secondary"
                    value={formData.duration}
                    onChange={(e) => updateForm('duration', e.target.value)}
                  >
                    <option value="5s">5 Seconds</option>
                    <option value="10s">10 Seconds (Standard)</option>
                    <option value="15s">15 Seconds</option>
                  </select>
                </div>
              </div>
            </div>

            <Button 
              className="w-full mt-6 py-6 text-lg bg-gradient-to-r from-accent-purple to-accent-secondary hover:opacity-90 transition-opacity border-0"
              disabled={!formData.title || isGenerating}
              onClick={handleGenerate}
            >
              {isGenerating ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Generating Animation...
                </span>
              ) : (
                <span className="flex items-center justify-center gap-2">
                  <Wand2 size={20} /> Animate Image
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
          
          {step < 2 && (
            <Button 
              className="gap-2 bg-white/10 hover:bg-white/20 text-white"
              onClick={() => setStep(s => Math.min(2, s + 1))}
              disabled={step === 1 && !formData.title}
            >
              Next Step <ArrowRight size={16} />
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
}
