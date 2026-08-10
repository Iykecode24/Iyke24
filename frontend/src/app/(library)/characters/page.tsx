'use client';
import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Search, Plus, Filter, User, MoreVertical, Sparkles, Mic } from 'lucide-react';
import { Character } from '@/types';
import { Modal } from '@/components/ui/modal';

// Mock data for the UI
const MOCK_VOICES = [
  { id: 'v1', name: 'Rachel (American Female)' },
  { id: 'v2', name: 'Clyde (American Male)' },
  { id: 'v3', name: 'Mimi (British Female)' }
];
const MOCK_CHARACTERS: Character[] = [
  {
    id: 'char-1',
    userId: 'user-1',
    name: 'Elena Vance',
    description: 'A tough, cynical detective with a heart of gold.',
    age: 35,
    gender: 'Female',
    role: 'Protagonist',
    appearance: 'Short dark hair, piercing green eyes, athletic build, usually wearing a leather jacket.',
    consistencyScore: 0.95,
    isLibrary: true,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  },
  {
    id: 'char-2',
    userId: 'user-1',
    name: 'Dr. Aris Thorne',
    description: 'Brilliant but eccentric quantum physicist.',
    age: 50,
    gender: 'Male',
    role: 'Supporting',
    appearance: 'Messy silver hair, wire-rimmed glasses, slightly stooped posture, wearing a lab coat or tweed jacket.',
    consistencyScore: 0.88,
    isLibrary: true,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
];

export default function CharactersLibraryPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newChar, setNewChar] = useState({ name: '', description: '', voiceId: '' });
  
  const handleSaveCharacter = () => {
    setIsModalOpen(false);
    // Add toast or mock save
  };

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold mb-1">Character Library</h1>
          <p className="text-text-secondary">Manage your consistent AI characters across all projects.</p>
        </div>
        <Button className="gap-2" onClick={() => setIsModalOpen(true)}>
          <Plus size={18} /> New Character
        </Button>
      </div>

      <div className="flex flex-col md:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" size={18} />
          <input 
            type="text"
            placeholder="Search characters by name, role, or description..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-bg-secondary border border-white/10 rounded-xl py-2.5 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-transparent transition-all"
          />
        </div>
        <Button variant="secondary" className="gap-2">
          <Filter size={18} /> Filter
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {MOCK_CHARACTERS.map(char => (
          <Card key={char.id} className="group overflow-hidden flex flex-col hover:-translate-y-1 transition-all duration-300">
            {/* Character Thumbnail / References Preview */}
            <div className="h-48 bg-gradient-to-br from-bg-secondary to-bg-primary border-b border-white/5 relative flex items-center justify-center">
              {/* Replace with actual character reference image later */}
              <div className="w-20 h-20 rounded-full bg-white/5 flex items-center justify-center border border-white/10">
                <User size={32} className="text-text-muted" />
              </div>
              <div className="absolute top-3 right-3">
                <button className="w-8 h-8 rounded-full bg-black/40 backdrop-blur flex items-center justify-center text-text-secondary hover:text-white transition-colors">
                  <MoreVertical size={16} />
                </button>
              </div>
              {char.consistencyScore && char.consistencyScore > 0.9 && (
                <div className="absolute top-3 left-3 px-2 py-1 rounded-md bg-accent-green/20 border border-accent-green/30 backdrop-blur flex items-center gap-1">
                  <Sparkles size={12} className="text-accent-green" />
                  <span className="text-[10px] font-bold text-accent-green">High Consistency</span>
                </div>
              )}
            </div>
            
            <div className="p-5 flex-1 flex flex-col">
              <div className="mb-2">
                <h3 className="font-bold text-lg text-white group-hover:text-accent-primary transition-colors">{char.name}</h3>
                <div className="text-xs text-text-muted">{char.age}yo • {char.gender} • {char.role}</div>
              </div>
              
              <p className="text-sm text-text-secondary line-clamp-3 mb-4 flex-1">
                {char.appearance}
              </p>
              
              <div className="flex gap-2 mt-auto">
                <Badge status={char.isLibrary ? 'published' : 'draft'} />
              </div>
            </div>
          </Card>
        ))}
        
        {/* Create New Card */}
        <button 
          onClick={() => setIsModalOpen(true)}
          className="h-full min-h-[320px] rounded-2xl border-2 border-dashed border-white/10 flex flex-col items-center justify-center gap-4 text-text-muted hover:text-white hover:border-accent-primary/50 hover:bg-accent-primary/5 transition-all group"
        >
          <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center group-hover:bg-accent-primary/20 transition-colors">
            <Plus size={24} className="group-hover:text-accent-primary" />
          </div>
          <div className="text-center">
            <h3 className="font-bold mb-1">Create Character</h3>
            <p className="text-sm text-text-secondary">Train a new consistent character</p>
          </div>
        </button>
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Create New Character">
        <div className="space-y-4">
          <Input 
            label="Character Name" 
            placeholder="e.g. John Doe" 
            value={newChar.name}
            onChange={(e) => setNewChar({ ...newChar, name: e.target.value })}
          />
          <Input 
            label="Description / Personality" 
            as="textarea"
            placeholder="Describe the character..." 
            value={newChar.description}
            onChange={(e) => setNewChar({ ...newChar, description: e.target.value })}
          />
          <div className="space-y-2">
            <label className="text-sm font-medium text-white flex items-center gap-2">
              <Mic size={16} className="text-accent-primary" /> ElevenLabs Voice
            </label>
            <Input 
              as="select"
              value={newChar.voiceId}
              onChange={(e) => setNewChar({ ...newChar, voiceId: e.target.value })}
              options={[
                { label: 'Select a voice...', value: '' },
                ...MOCK_VOICES.map(v => ({ label: v.name, value: v.id }))
              ]}
            />
            <p className="text-xs text-text-muted">Choose a consistent voice for this character.</p>
          </div>
          <div className="pt-4 flex justify-end gap-2">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>Cancel</Button>
            <Button onClick={handleSaveCharacter}>Save Character</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
