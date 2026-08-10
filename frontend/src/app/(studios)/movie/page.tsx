'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { ProgressBar } from '@/components/ui/progress-bar';
import { Film, UserPlus, Music, Video, Sparkles, Loader2, DollarSign } from 'lucide-react';
import { api } from '@/lib/api';
import { ContentType } from '@/types';
import { useToast } from '@/hooks/use-toast';

export default function MovieStudioPage() {
  const router = useRouter();
  const { toast } = useToast();
  
  const [step, setStep] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);
  const totalSteps = 5;

  // Form State
  const [formData, setFormData] = useState({
    title: '',
    idea: '',
    genre: 'action',
    targetAudience: 'general',
    language: 'english',
    duration: 60, // seconds
    orientation: 'landscape',
    visualStyle: 'cinematic_realism',
    characterCount: 2,
    voicePreference: 'elevenlabs_premium',
    narratorVoiceId: 'auto',
    musicPreference: 'orchestral_epic',
    resolution: '1080p'
  });

  const handleNext = () => setStep(s => Math.min(s + 1, totalSteps));
  const handlePrev = () => setStep(s => Math.max(s - 1, 1));

  const handleChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      // 1. Create the Project
      const project = await api.createProject({
        title: formData.title || 'Untitled Masterpiece',
        contentType: ContentType.movie,
        genre: formData.genre,
        targetAudience: formData.targetAudience,
        language: formData.language,
        durationSeconds: formData.duration,
        orientation: formData.orientation,
        visualStyle: formData.visualStyle,
        voicePreference: formData.voicePreference,
        musicPreference: formData.musicPreference,
        resolution: formData.resolution
      });

      toast.success('Project Created: Your project has been saved. Generating script...');

      // Redirect to the project script view immediately so the user can watch it generate
      router.push(`/projects/${project.id}/script?generating=true`);
      
    } catch (error) {
      console.error('Failed to create project:', error);
      toast.error('Error: Failed to create project. Please try again.');
      setIsGenerating(false);
    }
  };

  const estimatedCost = ((formData.duration / 60) * 1.50).toFixed(2); // Mock calc: $1.50 per min

  return (
    <div className="max-w-4xl mx-auto py-8">
      <div className="mb-8 flex items-center gap-4">
        <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-purple-500/20">
          <Film className="text-white" size={28} />
        </div>
        <div>
          <h1 className="text-3xl font-bold mb-1">AI Movie Studio</h1>
          <p className="text-text-secondary">Transform your idea into a cinematic masterpiece</p>
        </div>
      </div>

      <div className="mb-8">
        <ProgressBar value={(step / totalSteps) * 100} label={`Step ${step} of ${totalSteps}`} />
      </div>

      <Card className="min-h-[500px] flex flex-col relative overflow-hidden animate-slide-up">
        {/* Background glow based on step */}
        <div className="absolute top-[-20%] right-[-10%] w-[500px] h-[500px] rounded-full bg-gradient-to-br from-purple-600/10 to-blue-600/10 blur-[100px] pointer-events-none" />

        <div className="flex-1 p-2 relative z-10">
          {/* STEP 1: Title & Idea */}
          {step === 1 && (
            <div className="space-y-6 animate-fade-in">
              <div className="flex items-center gap-2 mb-6">
                <Sparkles className="text-accent-primary" size={24} />
                <h2 className="text-2xl font-bold">The Core Concept</h2>
              </div>
              
              <Input 
                label="Movie Title" 
                placeholder="e.g. Echoes of Eternity" 
                value={formData.title}
                onChange={(e) => handleChange('title', e.target.value)}
                className="text-lg"
              />
              
              <Input 
                as="textarea" 
                label="Story Idea / Synopsis" 
                placeholder="Describe what happens in your movie. The more detail, the better the AI can craft the script..." 
                className="min-h-[200px] text-base"
                value={formData.idea}
                onChange={(e) => handleChange('idea', e.target.value)}
              />
              
              <Input 
                as="select" 
                label="Primary Genre" 
                value={formData.genre}
                onChange={(e) => handleChange('genre', e.target.value)}
                options={[
                  {label: 'Action & Adventure', value: 'action'},
                  {label: 'Science Fiction', value: 'scifi'},
                  {label: 'Drama', value: 'drama'},
                  {label: 'Horror / Thriller', value: 'horror'},
                  {label: 'Romantic Comedy', value: 'romcom'},
                  {label: 'Fantasy', value: 'fantasy'},
                  {label: 'Historical / Period', value: 'historical'}
                ]} 
              />
            </div>
          )}

          {/* STEP 2: Demographics & Format */}
          {step === 2 && (
            <div className="space-y-6 animate-fade-in">
              <div className="flex items-center gap-2 mb-6">
                <Video className="text-accent-secondary" size={24} />
                <h2 className="text-2xl font-bold">Format & Audience</h2>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Input 
                  as="select" 
                  label="Orientation" 
                  value={formData.orientation}
                  onChange={(e) => handleChange('orientation', e.target.value)}
                  options={[
                    {label: 'Landscape (16:9) - YouTube/TV', value: 'landscape'},
                    {label: 'Portrait (9:16) - TikTok/Reels', value: 'portrait'},
                    {label: 'Square (1:1) - Instagram', value: 'square'}
                  ]} 
                />
                
                <Input 
                  as="select" 
                  label="Target Duration" 
                  value={formData.duration}
                  onChange={(e) => handleChange('duration', Number(e.target.value))}
                  options={[
                    {label: '30 Seconds (Short/Trailer)', value: '30'},
                    {label: '1 Minute (Standard)', value: '60'},
                    {label: '3 Minutes (Short Film)', value: '180'},
                    {label: '5 Minutes (Mini Feature)', value: '300'}
                  ]} 
                />

                <Input 
                  as="select" 
                  label="Target Audience" 
                  value={formData.targetAudience}
                  onChange={(e) => handleChange('targetAudience', e.target.value)}
                  options={[
                    {label: 'General Audience', value: 'general'},
                    {label: 'Kids & Family', value: 'kids'},
                    {label: 'Teens / Young Adult', value: 'teens'},
                    {label: 'Mature / Adult', value: 'mature'}
                  ]} 
                />
                
                <Input 
                  as="select" 
                  label="Language" 
                  value={formData.language}
                  onChange={(e) => handleChange('language', e.target.value)}
                  options={[
                    {label: 'English', value: 'english'},
                    {label: 'Spanish', value: 'spanish'},
                    {label: 'French', value: 'french'},
                    {label: 'Japanese (Anime style)', value: 'japanese'}
                  ]} 
                />
              </div>

              <div className="pt-4">
                <Input 
                  as="select" 
                  label="Visual Style (Cinematography)" 
                  value={formData.visualStyle}
                  onChange={(e) => handleChange('visualStyle', e.target.value)}
                  options={[
                    {label: 'Cinematic Realism (Arri Alexa, 35mm)', value: 'cinematic_realism'},
                    {label: 'Dark & Gritty (Cyberpunk, Noir)', value: 'dark_gritty'},
                    {label: 'Vibrant & Stylized (Comic, Neon)', value: 'vibrant_stylized'},
                    {label: 'Vintage Film (Grainy, 70s)', value: 'vintage_film'}
                  ]} 
                />
              </div>
            </div>
          )}

          {/* STEP 3: Characters */}
          {step === 3 && (
            <div className="space-y-6 animate-fade-in">
              <div className="flex items-center gap-2 mb-6">
                <UserPlus className="text-accent-pink" size={24} />
                <h2 className="text-2xl font-bold">Cast & Characters</h2>
              </div>
              
              <p className="text-text-secondary mb-4">
                How many primary characters are in this story? The AI will generate consistent character profiles based on your script.
              </p>

              <div className="flex items-center justify-center py-10">
                <div className="flex items-center gap-6 bg-bg-secondary p-4 rounded-2xl border border-white/5">
                  <button 
                    onClick={() => handleChange('characterCount', Math.max(1, formData.characterCount - 1))}
                    className="w-12 h-12 rounded-full bg-white/5 hover:bg-white/10 flex items-center justify-center text-xl transition-colors"
                  >
                    -
                  </button>
                  <div className="text-4xl font-bold w-16 text-center">{formData.characterCount}</div>
                  <button 
                    onClick={() => handleChange('characterCount', Math.min(10, formData.characterCount + 1))}
                    className="w-12 h-12 rounded-full bg-white/5 hover:bg-white/10 flex items-center justify-center text-xl transition-colors"
                  >
                    +
                  </button>
                </div>
              </div>

              <div className="p-4 bg-accent-primary/10 border border-accent-primary/20 rounded-xl">
                <p className="text-sm text-accent-primary font-medium flex items-center gap-2">
                  <Sparkles size={16} />
                  Pro Tip: You can customize character appearances and upload face references after the script is generated.
                </p>
              </div>
            </div>
          )}

          {/* STEP 4: Audio & Production */}
          {step === 4 && (
            <div className="space-y-6 animate-fade-in">
              <div className="flex items-center gap-2 mb-6">
                <Music className="text-accent-green" size={24} />
                <h2 className="text-2xl font-bold">Audio & Rendering</h2>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <Input 
                    as="select" 
                    label="Voice Generation Engine" 
                    value={formData.voicePreference}
                    onChange={(e) => handleChange('voicePreference', e.target.value)}
                    options={[
                      {label: 'ElevenLabs Premium (Ultra-realistic)', value: 'elevenlabs_premium'},
                      {label: 'Standard TTS (Cost-effective)', value: 'standard_tts'},
                      {label: 'No Voices (Music/SFX only)', value: 'none'}
                    ]} 
                  />

                  {formData.voicePreference === 'elevenlabs_premium' && (
                    <Input 
                      as="select" 
                      label="Narrator Voice" 
                      value={formData.narratorVoiceId || ''}
                      onChange={(e) => handleChange('narratorVoiceId', e.target.value)}
                      options={[
                        { label: 'Auto-select based on script', value: 'auto' },
                        { label: 'Rachel (American Female)', value: 'v1' },
                        { label: 'Clyde (American Male)', value: 'v2' },
                        { label: 'Mimi (British Female)', value: 'v3' }
                      ]} 
                    />
                  )}
                </div>
                
                <Input 
                  as="select" 
                  label="Music Score" 
                  value={formData.musicPreference}
                  onChange={(e) => handleChange('musicPreference', e.target.value)}
                  options={[
                    {label: 'Epic Orchestral', value: 'orchestral_epic'},
                    {label: 'Tense Thriller / Ambient', value: 'ambient_tense'},
                    {label: 'Upbeat & Energetic', value: 'upbeat_energetic'},
                    {label: 'Melancholy / Emotional', value: 'emotional'}
                  ]} 
                />
              </div>

              <div className="pt-4">
                <h3 className="text-sm font-medium mb-3">Final Render Quality</h3>
                <div className="grid grid-cols-3 gap-4">
                  {['720p', '1080p', '4K'].map(res => (
                    <div 
                      key={res}
                      onClick={() => handleChange('resolution', res)}
                      className={`p-4 rounded-xl border text-center cursor-pointer transition-all ${
                        formData.resolution === res 
                          ? 'border-accent-primary bg-accent-primary/10 text-white shadow-glow-purple' 
                          : 'border-white/10 hover:border-white/30 text-text-muted'
                      }`}
                    >
                      <div className="text-xl font-bold mb-1">{res}</div>
                      <div className="text-xs">{res === '4K' ? 'Highest Cost' : res === '1080p' ? 'Recommended' : 'Fastest'}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* STEP 5: Review */}
          {step === 5 && (
            <div className="space-y-6 animate-fade-in">
              <div className="flex items-center gap-2 mb-6">
                <Film className="text-accent-gold" size={24} />
                <h2 className="text-2xl font-bold">Ready for Production</h2>
              </div>
              
              <div className="p-6 bg-bg-secondary rounded-2xl border border-white/5 space-y-4">
                <div>
                  <h3 className="text-sm text-text-muted">Title</h3>
                  <p className="text-lg font-semibold">{formData.title || 'Untitled'}</p>
                </div>
                <div>
                  <h3 className="text-sm text-text-muted">Synopsis</h3>
                  <p className="text-sm">{formData.idea || 'No synopsis provided.'}</p>
                </div>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-white/5">
                  <div>
                    <h3 className="text-xs text-text-muted">Genre</h3>
                    <p className="text-sm capitalize">{formData.genre}</p>
                  </div>
                  <div>
                    <h3 className="text-xs text-text-muted">Format</h3>
                    <p className="text-sm capitalize">{formData.duration}s · {formData.orientation}</p>
                  </div>
                  <div>
                    <h3 className="text-xs text-text-muted">Cast</h3>
                    <p className="text-sm">{formData.characterCount} Characters</p>
                  </div>
                  <div>
                    <h3 className="text-xs text-text-muted">Resolution</h3>
                    <p className="text-sm">{formData.resolution}</p>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between p-4 rounded-xl border border-accent-gold/30 bg-accent-gold/5">
                <div className="flex items-center gap-3">
                  <DollarSign className="text-accent-gold" />
                  <div>
                    <p className="font-semibold text-accent-gold">Estimated Rendering Cost</p>
                    <p className="text-xs text-text-muted">Based on GPU time and API usage</p>
                  </div>
                </div>
                <div className="text-2xl font-bold text-accent-gold">
                  ${estimatedCost}
                </div>
              </div>
            </div>
          )}
        </div>
        
        {/* Navigation Footer */}
        <div className="flex justify-between mt-8 pt-6 border-t border-white/10 relative z-10">
          <Button 
            variant="secondary" 
            onClick={handlePrev} 
            disabled={step === 1 || isGenerating}
          >
            Back
          </Button>
          <Button 
            onClick={step === totalSteps ? handleGenerate : handleNext}
            isLoading={isGenerating}
            className={step === totalSteps ? 'bg-gradient-to-r from-accent-primary to-accent-secondary' : ''}
          >
            {step === totalSteps ? 'Write Script & Breakdown' : 'Next Step'}
          </Button>
        </div>
      </Card>
    </div>
  );
}
