'use client';
import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Search, Filter, Play, Plus, Mic, Settings2, Users } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

// Mock data for voices
const MOCK_VOICES = [
  { id: 'v1', name: 'Rachel', accent: 'American', gender: 'Female', useCase: 'Narration', previewUrl: '#' },
  { id: 'v2', name: 'Clyde', accent: 'American', gender: 'Male', useCase: 'Conversational', previewUrl: '#' },
  { id: 'v3', name: 'Mimi', accent: 'British', gender: 'Female', useCase: 'Animation', previewUrl: '#' },
  { id: 'v4', name: 'Fin', accent: 'Irish', gender: 'Male', useCase: 'Video Games', previewUrl: '#' },
  { id: 'v5', name: 'Bella', accent: 'Australian', gender: 'Female', useCase: 'News', previewUrl: '#' },
  { id: 'v6', name: 'Antoni', accent: 'American', gender: 'Male', useCase: 'Narration', previewUrl: '#' },
];

export default function VoiceLibraryPage() {
  const { toast } = useToast();
  const [searchQuery, setSearchQuery] = useState('');
  const [playingId, setPlayingId] = useState<string | null>(null);

  const handlePlay = (id: string) => {
    if (playingId === id) {
      setPlayingId(null);
    } else {
      setPlayingId(id);
      // Mock playback timeout
      setTimeout(() => setPlayingId(null), 3000);
    }
  };

  const handleAssign = (voiceName: string) => {
    toast.success(`Voice Selected: ${voiceName} has been selected. You can now assign it to a character.`);
  };

  const filteredVoices = MOCK_VOICES.filter(v => 
    v.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
    v.accent.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-8 animate-fade-in max-w-6xl mx-auto py-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Mic className="text-white" size={28} />
          </div>
          <div>
            <h1 className="text-3xl font-bold mb-1">Voice Library</h1>
            <p className="text-text-secondary">Browse, preview, and assign ElevenLabs voices to your characters.</p>
          </div>
        </div>
        <Button className="gap-2">
          <Plus size={18} /> Clone Voice
        </Button>
      </div>

      <div className="flex flex-col md:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" size={18} />
          <input 
            type="text"
            placeholder="Search voices by name, accent, or use case..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-bg-secondary border border-white/10 rounded-xl py-3 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-transparent transition-all"
          />
        </div>
        <Button variant="secondary" className="gap-2">
          <Filter size={18} /> Filter
        </Button>
        <Button variant="secondary" className="gap-2">
          <Settings2 size={18} /> Voice Settings
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-6">
        {filteredVoices.map(voice => (
          <Card key={voice.id} className="group overflow-hidden flex flex-col hover:-translate-y-1 transition-all duration-300">
            <div className="p-5 flex-1 flex flex-col relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-accent-primary/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 group-hover:bg-accent-primary/10 transition-colors" />
              
              <div className="flex justify-between items-start mb-4 relative z-10">
                <div>
                  <h3 className="font-bold text-xl text-white group-hover:text-accent-primary transition-colors mb-1">{voice.name}</h3>
                  <div className="text-xs text-text-muted flex gap-2">
                    <span className="flex items-center gap-1"><Badge status="default">{voice.accent}</Badge></span>
                    <span className="flex items-center gap-1"><Badge status="default">{voice.gender}</Badge></span>
                  </div>
                </div>
                <button 
                  onClick={() => handlePlay(voice.id)}
                  className={`w-12 h-12 rounded-full flex items-center justify-center transition-all ${
                    playingId === voice.id 
                      ? 'bg-accent-primary text-white shadow-glow-purple scale-95' 
                      : 'bg-white/5 hover:bg-white/10 text-white'
                  }`}
                >
                  <Play size={20} className={playingId === voice.id ? 'animate-pulse' : 'ml-1'} />
                </button>
              </div>
              
              <p className="text-sm text-text-secondary mb-6 flex-1 relative z-10">
                Recommended for <strong className="text-white/80">{voice.useCase}</strong>. 
                A high-quality, expressive voice suitable for professional content creation.
              </p>
              
              <div className="flex gap-3 mt-auto relative z-10">
                <Button 
                  variant="secondary" 
                  className="flex-1 text-sm h-10 gap-2"
                  onClick={() => handleAssign(voice.name)}
                >
                  <Users size={16} /> Assign to Character
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>
      
      {filteredVoices.length === 0 && (
        <div className="py-20 text-center text-text-secondary">
          No voices found matching your search.
        </div>
      )}
    </div>
  );
}
