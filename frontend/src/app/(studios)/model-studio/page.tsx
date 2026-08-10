'use client';
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Camera, Calendar, Play, Settings, Users, Video, Clock, CheckCircle, Activity, Music, Share2, Plus } from 'lucide-react';
import Image from 'next/image';

export default function AIModelStudio() {
  const [activeTab, setActiveTab] = useState('create');
  
  return (
    <div className="min-h-screen bg-bg-primary text-text-primary p-8 ml-[60px] lg:ml-64 transition-all duration-300">
      
      {/* Header */}
      <header className="mb-10 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3">
            <Camera className="text-accent-purple" size={32} />
            AI Model Studio
          </h1>
          <p className="text-text-secondary mt-2">
            Create highly realistic modeling/lifestyle videos using strictly authorized AI models.
          </p>
        </div>
        <div className="flex gap-4">
          <button className="bg-white/5 border border-white/10 px-4 py-2 rounded-lg text-sm font-medium hover:bg-white/10 transition-colors">
            Manage Models
          </button>
          <button className="bg-accent-purple hover:bg-accent-blue px-4 py-2 rounded-lg text-sm font-medium text-white shadow-btn-glow transition-all">
            + Create Campaign
          </button>
        </div>
      </header>

      {/* Main Tabs */}
      <div className="flex gap-8 mb-8 border-b border-white/10">
        {[
          { id: 'create', label: 'Create New Clip', icon: Play },
          { id: 'models', label: 'My Models', icon: Users },
          { id: 'production', label: "Today's Production", icon: Video },
          { id: 'automation', label: 'Automation', icon: Settings },
          { id: 'calendar', label: 'Content Calendar', icon: Calendar },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 pb-4 px-2 border-b-2 transition-all ${
              activeTab === tab.id 
                ? 'border-accent-purple text-accent-purple' 
                : 'border-transparent text-text-secondary hover:text-white'
            }`}
          >
            <tab.icon size={18} />
            <span className="font-semibold text-sm">{tab.label}</span>
          </button>
        ))}
      </div>

      {/* ── SECTION 1: CREATE NEW CLIP ── */}
      {activeTab === 'create' && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          <div className="glass-card rounded-2xl p-8 max-w-4xl">
            <h2 className="text-xl font-bold mb-6 flex items-center gap-2"><Play size={20} className="text-accent-purple"/> Manual Generation</h2>
            
            <div className="grid grid-cols-2 gap-6 mb-8">
              <div className="space-y-2">
                <label className="text-xs font-semibold text-text-muted uppercase tracking-wider">Select Model</label>
                <select className="w-full bg-bg-secondary border border-white/10 rounded-xl px-4 py-3 text-sm focus:border-accent-purple outline-none">
                  <option>Emma (Fashion / Lifestyle)</option>
                  <option>James (Urban / Fitness)</option>
                  <option>Sarah (Travel / Vlogs)</option>
                </select>
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-text-muted uppercase tracking-wider">Activity</label>
                <select className="w-full bg-bg-secondary border border-white/10 rounded-xl px-4 py-3 text-sm focus:border-accent-purple outline-none">
                  <option>Walking through the city</option>
                  <option>Morning coffee</option>
                  <option>Dance to Music</option>
                </select>
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-text-muted uppercase tracking-wider">Environment</label>
                <input type="text" placeholder="e.g. Sunny street in Tokyo" className="w-full bg-bg-secondary border border-white/10 rounded-xl px-4 py-3 text-sm focus:border-accent-purple outline-none" />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-text-muted uppercase tracking-wider">Wardrobe</label>
                <input type="text" placeholder="e.g. Winter coat and scarf" className="w-full bg-bg-secondary border border-white/10 rounded-xl px-4 py-3 text-sm focus:border-accent-purple outline-none" />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-text-muted uppercase tracking-wider">Duration</label>
                <select className="w-full bg-bg-secondary border border-white/10 rounded-xl px-4 py-3 text-sm focus:border-accent-purple outline-none">
                  <option>50 Seconds (Default)</option>
                  <option>15 Seconds</option>
                  <option>30 Seconds</option>
                  <option>60 Seconds</option>
                </select>
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-text-muted uppercase tracking-wider">Publishing Destination</label>
                <select className="w-full bg-bg-secondary border border-white/10 rounded-xl px-4 py-3 text-sm focus:border-accent-purple outline-none">
                  <option>YouTube Shorts (9:16)</option>
                  <option>Instagram Reels (9:16)</option>
                  <option>TikTok (9:16)</option>
                </select>
              </div>
            </div>

            <div className="space-y-2 mb-8">
              <label className="text-xs font-semibold text-text-muted uppercase tracking-wider">One-Instruction Production (AI Director)</label>
              <textarea 
                rows={3} 
                className="w-full bg-bg-secondary border border-white/10 rounded-xl px-4 py-3 text-sm focus:border-accent-purple outline-none resize-none"
                placeholder="e.g. Create a 50-second video of Model 04 spending an afternoon in downtown Toronto..."
              ></textarea>
            </div>

            <button className="w-full bg-accent-purple hover:bg-accent-blue py-4 rounded-xl font-bold text-white shadow-btn-glow transition-all">
              GENERATE VIDEO
            </button>
          </div>
        </motion.div>
      )}

      {/* ── SECTION 2: MY MODELS ── */}
      {activeTab === 'models' && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          
          <div className="glass-card rounded-2xl flex flex-col items-center justify-center p-8 border-dashed border-2 border-white/20 hover:border-accent-purple transition-colors cursor-pointer group min-h-[300px]">
            <Plus size={48} className="text-white/20 group-hover:text-accent-purple transition-colors mb-4" />
            <span className="font-semibold text-text-secondary group-hover:text-white transition-colors">Add New Model</span>
          </div>

          {[1, 2, 3].map((i) => (
            <div key={i} className="glass-card rounded-2xl overflow-hidden group">
              <div className="aspect-[3/4] bg-bg-secondary relative">
                {/* Placeholder for Model Portrait */}
                <div className="absolute inset-0 flex items-center justify-center text-white/10">
                  <Camera size={48} />
                </div>
              </div>
              <div className="p-5">
                <div className="flex justify-between items-center mb-2">
                  <h3 className="font-bold text-lg">Model 0{i}</h3>
                  <span className="bg-accent-purple/20 text-accent-purple text-xs px-2 py-1 rounded-md font-bold">18+ Verified</span>
                </div>
                <div className="text-xs text-text-secondary mb-4 space-y-1">
                  <p>12 Videos Produced</p>
                  <p>Last used: 2 days ago</p>
                </div>
                <button className="w-full bg-white/10 hover:bg-white/20 py-2 rounded-lg text-sm font-semibold transition-colors">
                  Create Clip
                </button>
              </div>
            </div>
          ))}
        </motion.div>
      )}

      {/* ── SECTION 3: TODAY'S PRODUCTION ── */}
      {activeTab === 'production' && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
          {[
            { model: 'Emma', activity: 'Morning coffee at café', status: 'Rendering', progress: 45, score: '-', time: '10:00 AM' },
            { model: 'James', activity: 'Gym workout', status: 'Quality Check', progress: 100, score: '92/100', time: '2:00 PM' },
            { model: 'Sarah', activity: 'Beach sunset walk', status: 'Scheduled', progress: 0, score: '-', time: '6:30 PM' },
          ].map((prod, i) => (
            <div key={i} className="glass-card rounded-xl p-5 flex items-center justify-between">
              <div className="flex items-center gap-4 w-1/3">
                <div className="w-12 h-12 rounded-lg bg-bg-secondary border border-white/10"></div>
                <div>
                  <h4 className="font-bold">{prod.model}</h4>
                  <p className="text-xs text-text-secondary">{prod.activity}</p>
                </div>
              </div>
              
              <div className="w-1/4">
                <div className="flex justify-between text-xs font-medium mb-1">
                  <span className="text-accent-purple">{prod.status}</span>
                  <span>{prod.progress}%</span>
                </div>
                <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden">
                  <div className="h-full bg-accent-purple" style={{ width: `${prod.progress}%` }}></div>
                </div>
              </div>

              <div className="w-1/6 text-center">
                <p className="text-xs text-text-muted uppercase tracking-wider">Quality Score</p>
                <p className="font-bold text-sm">{prod.score}</p>
              </div>

              <div className="w-1/6 text-right">
                <p className="text-xs text-text-muted uppercase tracking-wider">Scheduled Post</p>
                <p className="font-bold text-sm flex items-center justify-end gap-1"><Clock size={12}/> {prod.time}</p>
              </div>
            </div>
          ))}
        </motion.div>
      )}

      {/* ── SECTION 4: AUTOMATION ── */}
      {activeTab === 'automation' && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="grid grid-cols-2 gap-8">
          <div className="glass-card rounded-2xl p-8 space-y-6">
            <h2 className="text-xl font-bold flex items-center gap-2"><Activity size={20} className="text-accent-purple"/> Autonomous Director Rules</h2>
            
            <div className="flex items-center justify-between p-4 bg-bg-secondary rounded-xl border border-white/5">
              <div>
                <h4 className="font-bold">Autonomous Production</h4>
                <p className="text-xs text-text-secondary">AI schedules and creates content automatically</p>
              </div>
              <div className="w-12 h-6 bg-accent-purple rounded-full relative cursor-pointer">
                <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
              </div>
            </div>

            <div className="space-y-4 pt-4 border-t border-white/10">
              <div className="space-y-2">
                <label className="text-xs font-semibold text-text-muted uppercase tracking-wider">Frequency</label>
                <select className="w-full bg-bg-secondary border border-white/10 rounded-xl px-4 py-3 text-sm focus:border-accent-purple outline-none">
                  <option>Daily (1 Post/Day)</option>
                  <option>Twice Daily</option>
                  <option>Weekly (3 Posts/Week)</option>
                </select>
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-text-muted uppercase tracking-wider">Preferred Content Categories</label>
                <div className="flex flex-wrap gap-2">
                  {['Lifestyle', 'Fashion', 'Fitness', 'Travel', 'Nightlife', 'Professional'].map((cat) => (
                    <span key={cat} className="bg-white/10 hover:bg-accent-purple/30 px-3 py-1.5 rounded-lg text-xs font-medium cursor-pointer transition-colors border border-white/5">
                      {cat}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="glass-card rounded-2xl p-8 space-y-6">
            <h2 className="text-xl font-bold flex items-center gap-2"><Share2 size={20} className="text-accent-purple"/> Approval & Publishing</h2>
            
            <div className="flex items-center justify-between p-4 bg-bg-secondary rounded-xl border border-white/5">
              <div>
                <h4 className="font-bold">Require Approval</h4>
                <p className="text-xs text-text-secondary">Send completed clips to dashboard for review</p>
              </div>
              <div className="w-12 h-6 bg-white/20 rounded-full relative cursor-pointer">
                <div className="absolute left-1 top-1 w-4 h-4 bg-white rounded-full"></div>
              </div>
            </div>

            <div className="flex items-center justify-between p-4 bg-bg-secondary rounded-xl border border-white/5">
              <div>
                <h4 className="font-bold text-accent-purple">Auto Publish</h4>
                <p className="text-xs text-text-secondary">Publish immediately if quality score {'>'}= 90</p>
              </div>
              <div className="w-12 h-6 bg-accent-purple rounded-full relative cursor-pointer">
                <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
              </div>
            </div>

            <div className="p-4 bg-accent-purple/10 border border-accent-purple/20 rounded-xl">
              <p className="text-xs text-text-secondary leading-relaxed">
                <strong className="text-white">Note:</strong> The AI Quality Agent will inspect every frame for physical impossibilities, waxy skin, and malformed hands. If the score falls below your 90/100 threshold, the specific shot will be regenerated before publishing.
              </p>
            </div>
          </div>
        </motion.div>
      )}

      {/* ── SECTION 5: CONTENT CALENDAR ── */}
      {activeTab === 'calendar' && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="glass-card rounded-2xl p-8">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-xl font-bold flex items-center gap-2"><Calendar size={20} className="text-accent-purple"/> August 2026</h2>
            <div className="flex gap-2">
              <button className="px-3 py-1 bg-white/10 rounded text-sm hover:bg-white/20">&lt;</button>
              <button className="px-3 py-1 bg-white/10 rounded text-sm hover:bg-white/20">Today</button>
              <button className="px-3 py-1 bg-white/10 rounded text-sm hover:bg-white/20">&gt;</button>
            </div>
          </div>
          
          <div className="grid grid-cols-7 gap-4">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
              <div key={day} className="text-center text-xs font-semibold text-text-muted mb-2 uppercase">{day}</div>
            ))}
            
            {/* Example Calendar Grid */}
            {Array.from({length: 31}).map((_, i) => (
              <div key={i} className="h-24 bg-bg-secondary border border-white/5 rounded-xl p-2 relative group hover:border-accent-purple/50 transition-colors">
                <span className="text-xs font-bold text-text-secondary">{i + 1}</span>
                {i === 9 && (
                  <div className="absolute bottom-2 left-2 right-2 bg-accent-purple/20 border border-accent-purple/30 text-accent-purple text-[10px] font-bold p-1 rounded">
                    2 Posts
                  </div>
                )}
                {i === 12 && (
                  <div className="absolute bottom-2 left-2 right-2 bg-white/10 border border-white/20 text-white text-[10px] font-bold p-1 rounded">
                    Scheduled
                  </div>
                )}
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}
